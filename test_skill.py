#!/usr/bin/env python3
"""
Test script for Context7 Documentation Fetcher Skill
Run this to verify the skill works before uploading to Claude.ai
"""

import sys
from fetch_docs import search_library, get_library_docs, format_docs_for_display

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def test_search():
    """Test library search functionality"""
    print_section("TEST 1: Search Libraries")
    
    test_queries = [
        "next.js",
        "react hook form",
        "supabase",
        "tailwind"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Searching: {query}")
        result = search_library(query)
        
        if result:
            print(f"   ✅ Found: {result['title']}")
            print(f"   📝 ID: {result['id']}")
            print(f"   ⭐ Trust Score: {result['trustScore']}")
            print(f"   📚 Snippets: {result['totalSnippets']}")
        else:
            print(f"   ❌ Not found")

def test_fetch():
    """Test documentation fetching"""
    print_section("TEST 2: Fetch Documentation")
    
    # Test with Next.js
    print("\n📚 Fetching Next.js documentation (topic: app router)...")
    
    # First search for the library
    library = search_library("next.js")
    if not library:
        print("❌ Could not find Next.js")
        return
    
    print(f"   Found: {library['title']} ({library['id']})")
    
    # Fetch docs
    docs = get_library_docs(library['id'], topic="app router", tokens=3000)
    
    if docs:
        print(f"   ✅ Retrieved {len(docs)} characters of documentation")
        print("\n   Preview of documentation:")
        print("   " + "-"*76)
        
        # Show first 500 characters
        preview = docs[:500] if len(docs) > 500 else docs
        print("   " + preview.replace("\n", "\n   ")[:500])
        print("   " + "-"*76)
    else:
        print("   ❌ Failed to fetch documentation")

def test_format():
    """Test documentation formatting"""
    print_section("TEST 3: Format Documentation")
    
    # Fetch and format React Hook Form docs
    print("\n📝 Testing format with React Hook Form...")
    
    library = search_library("react hook form")
    if not library:
        print("❌ Could not find React Hook Form")
        return
    
    docs = get_library_docs(library['id'], tokens=2000)
    
    if docs:
        formatted = format_docs_for_display(docs, max_chars=500)
        print("\n   Formatted output preview:")
        print("   " + "-"*76)
        # Show formatted output
        preview = formatted[:500]
        print("   " + preview.replace("\n", "\n   "))
        print("   " + "-"*76)
        print(f"   ✅ Full formatted output: {len(formatted)} characters")
    else:
        print("   ❌ No docs to format")

def test_full_workflow():
    """Test complete workflow"""
    print_section("TEST 4: Complete Workflow")
    
    test_cases = [
        ("zustand", "store management"),
        ("supabase", "authentication"),
    ]
    
    for library_name, topic in test_cases:
        print(f"\n🧪 Testing: {library_name} (topic: {topic})")
        
        # Search
        library = search_library(library_name)
        if not library:
            print(f"   ❌ Search failed for {library_name}")
            continue
        
        print(f"   ✅ Found: {library['title']}")
        
        # Fetch
        docs = get_library_docs(library['id'], topic=topic, tokens=2000)
        if not docs:
            print(f"   ❌ Fetch failed")
            continue
        
        print(f"   ✅ Fetched {len(docs)} characters")
        
        # Format
        formatted = format_docs_for_display(docs, max_chars=500)
        print(f"   ✅ Formatted: {len(formatted)} characters")

def main():
    """Run all tests"""
    print("\n" + "🧪 Context7 Documentation Fetcher - Test Suite" + "\n")
    print("This will test the skill's functionality before uploading to Claude.ai\n")
    
    try:
        # Run all tests
        test_search()
        test_fetch()
        test_format()
        test_full_workflow()
        
        # Summary
        print_section("✅ TEST SUMMARY")
        print("\nAll tests completed! If you see ✅ marks above, the skill is working.")
        print("\nNext steps:")
        print("1. Zip the skill folder: zip -r context7-docs-skill.zip context7-docs-skill/")
        print("2. Go to https://claude.ai/settings/capabilities")
        print("3. Upload the ZIP file in the Skills section")
        print("4. Enable the skill and start using it!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("- Make sure you have 'requests' installed: pip install requests")
        print("- Check your internet connection")
        print("- Verify the API key is valid")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())