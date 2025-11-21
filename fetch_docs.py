#!/usr/bin/env python3
"""
Context7 Documentation Fetcher
Fetches up-to-date library documentation from Context7 API
"""

import json
import sys
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import quote

# Context7 API configuration
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://context7.com/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def search_library(query: str) -> Optional[Dict[str, Any]]:
    """
    Search for a library in Context7 database.
    
    Args:
        query: Library name to search for (e.g., "react hook form", "next.js")
    
    Returns:
        Dict with library info including ID, or None if not found
    """
    try:
        # Clean and encode query
        query = query.strip().replace(" ", "+")
        url = f"{BASE_URL}/search?query={query}"
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            return None
        
        # Return the top result (highest trust score)
        top_result = results[0]
        return {
            "id": top_result.get("id"),
            "title": top_result.get("title"),
            "description": top_result.get("description", ""),
            "trustScore": top_result.get("trustScore", 0),
            "totalSnippets": top_result.get("totalSnippets", 0)
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error searching library: {str(e)}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        return None


def get_library_docs(
    library_id: str,
    topic: Optional[str] = None,
    tokens: int = 5000
) -> Optional[str]:
    """
    Fetch documentation for a specific library.
    
    Args:
        library_id: Context7 library ID (e.g., "/vercel/next.js")
        topic: Optional topic to filter docs (e.g., "routing", "authentication")
        tokens: Maximum tokens to retrieve (default: 5000)
    
    Returns:
        Documentation as plain text string, or None if fetch fails
    """
    try:
        # Remove leading slash if present
        library_id = library_id.lstrip("/")
        
        # Build URL with parameters
        url = f"{BASE_URL}/{library_id}"
        params = {
            "tokens": tokens
        }
        
        # Add topic if provided
        if topic:
            params["topic"] = topic
        
        print(f"   Fetching from: {url}", file=sys.stderr)
        print(f"   Params: {params}", file=sys.stderr)
        
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        
        print(f"   Status code: {response.status_code}", file=sys.stderr)
        
        # Check if response is successful
        if response.status_code == 404:
            print(f"   Library not found or no docs available", file=sys.stderr)
            return None
        
        if response.status_code != 200:
            print(f"   Response body: {response.text[:200]}", file=sys.stderr)
            response.raise_for_status()
        
        # Context7 returns plain text by default
        docs_text = response.text
        
        if not docs_text or docs_text.strip() == "":
            print(f"   No documentation content returned", file=sys.stderr)
            return None
        
        print(f"   Retrieved {len(docs_text)} characters of documentation", file=sys.stderr)
        return docs_text
        
    except requests.exceptions.RequestException as e:
        print(f"   Error fetching docs: {str(e)}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"   Unexpected error: {str(e)}", file=sys.stderr)
        return None


def format_docs_for_display(docs_text: str, max_chars: int = 2000) -> str:
    """
    Format documentation text for display.
    
    Args:
        docs_text: Raw documentation text from Context7
        max_chars: Maximum characters to display (for preview)
    
    Returns:
        Formatted documentation string
    """
    if not docs_text:
        return "No documentation found."
    
    # If docs are too long, show preview
    if len(docs_text) > max_chars:
        preview = docs_text[:max_chars]
        return f"{preview}\n\n... (truncated - total {len(docs_text)} characters)"
    
    return docs_text


def fetch_and_display(library_query: str, topic: Optional[str] = None) -> None:
    """
    Main function to search and fetch library documentation.
    
    Args:
        library_query: Library name to search for
        topic: Optional topic to filter documentation
    """
    print(f"🔍 Searching for library: {library_query}", file=sys.stderr)
    
    # Step 1: Search for library
    library_info = search_library(library_query)
    
    if not library_info:
        print(f"❌ Library '{library_query}' not found in Context7 database.", file=sys.stderr)
        print("Suggestion: Try alternative names or check https://context7.com", file=sys.stderr)
        return
    
    library_id = library_info["id"]
    library_title = library_info["title"]
    
    print(f"✅ Found: {library_title} (ID: {library_id})", file=sys.stderr)
    print(f"   Trust Score: {library_info['trustScore']}", file=sys.stderr)
    print(f"   Total Snippets: {library_info['totalSnippets']}", file=sys.stderr)
    
    # Step 2: Fetch documentation
    topic_msg = f" with topic '{topic}'" if topic else ""
    print(f"\n📚 Fetching documentation{topic_msg}...", file=sys.stderr)
    
    docs = get_library_docs(library_id, topic=topic)
    
    if not docs:
        print(f"❌ Failed to fetch documentation for {library_title}", file=sys.stderr)
        print(f"   This might be a temporary issue or the library may not have docs available", file=sys.stderr)
        return
    
    print(f"✅ Retrieved documentation successfully", file=sys.stderr)
    
    # Step 3: Format and display
    print("\n" + "="*80, file=sys.stderr)
    print(f"DOCUMENTATION: {library_title}", file=sys.stderr)
    print("="*80, file=sys.stderr)
    
    # Print docs to stdout (for Claude to consume)
    formatted_docs = format_docs_for_display(docs, max_chars=5000)
    print(formatted_docs)


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python fetch_docs.py <library_name> [topic]", file=sys.stderr)
        print("Example: python fetch_docs.py 'react hook form' validation", file=sys.stderr)
        sys.exit(1)
    
    library_query = sys.argv[1]
    topic = sys.argv[2] if len(sys.argv) > 2 else None
    
    fetch_and_display(library_query, topic)