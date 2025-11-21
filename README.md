# Context7 Documentation Fetcher Skill

Custom skill for Claude.ai that automatically fetches up-to-date library documentation from Context7.

## 📦 What's Included

```
context7-docs-skill/
├── SKILL.md          # Skill metadata and instructions for Claude
├── fetch_docs.py     # Python script to fetch docs from Context7 API
├── README.md         # This file
└── test_skill.py     # Test script to verify functionality
```

## 🚀 Quick Start

### 1. Test the Skill Locally (Optional)

Before uploading, you can test if the script works:

```bash
# Install dependencies
pip install requests

# Test searching and fetching docs
python test_skill.py

# Or manually test specific libraries
python fetch_docs.py "next.js" "app router"
python fetch_docs.py "react hook form" "validation"
python fetch_docs.py "supabase" "authentication"
```

### 2. Package the Skill

Create a ZIP file with the skill folder:

```bash
# From the parent directory
zip -r context7-docs-skill.zip context7-docs-skill/
```

**Important**: The ZIP should contain the `context7-docs-skill` folder as the root, not individual files.

✅ **Correct structure:**
```
context7-docs-skill.zip
└── context7-docs-skill/
    ├── SKILL.md
    ├── fetch_docs.py
    ├── README.md
    └── test_skill.py
```

❌ **Incorrect structure:**
```
context7-docs-skill.zip
├── SKILL.md
├── fetch_docs.py
└── ...
```

### 3. Upload to Claude.ai

1. Go to https://claude.ai/settings/capabilities
2. Scroll to **Skills** section
3. Click **"Upload Custom Skill"**
4. Select `context7-docs-skill.zip`
5. Enable the skill

### 4. Start Using

Once enabled, just ask Claude questions naturally:

- "Create a form with React Hook Form and Zod"
- "How do I setup Next.js 15 app router?"
- "Show me Supabase authentication examples"
- "Setup TanStack Query with TypeScript"

Claude will automatically fetch the latest docs and generate accurate code!

## 🔧 How It Works

1. **Trigger Detection**: Claude detects when you mention libraries or need docs
2. **Search Library**: Skill searches Context7 for the library ID
3. **Fetch Docs**: Retrieves up-to-date documentation with code examples
4. **Generate Code**: Claude uses fresh docs to provide accurate answers

## 📚 Supported Libraries

The skill can fetch docs for any library in Context7, including:

**Frontend**
- Next.js, React, Vue, Nuxt, Svelte, Astro, Remix

**State Management**
- Zustand, Redux, TanStack Query, Jotai, Recoil

**Forms & Validation**
- React Hook Form, Formik, Zod, Yup

**UI Libraries**
- Tailwind CSS, shadcn/ui, Radix UI, Mantine, Chakra UI

**Backend**
- Express, Fastify, Hono, tRPC, NestJS

**Database & ORM**
- Supabase, Prisma, Drizzle, MongoDB, Mongoose

**And many more!** Check https://context7.com for the full library list.

## 💡 Usage Examples

### Example 1: Form with Validation
```
You: "Create a registration form with React Hook Form and Zod validation"

Claude will:
1. Fetch React Hook Form docs (topic: "validation")
2. Fetch Zod docs (topic: "schema")
3. Generate accurate code using current API methods
```

### Example 2: Next.js Setup
```
You: "Setup Next.js 15 with server actions and form handling"

Claude will:
1. Fetch Next.js docs (topic: "server actions")
2. Generate proper Next.js 15 code with app router patterns
```

### Example 3: Database Integration
```
You: "How do I setup Supabase realtime subscriptions?"

Claude will:
1. Fetch Supabase docs (topic: "realtime")
2. Show current subscription API and examples
```

## 🔐 Security Notes

- API key is embedded in `fetch_docs.py`
- The key is for Context7's free tier (generous limits)
- If you need to rotate the key:
  1. Get new key from https://context7.com/dashboard
  2. Replace `API_KEY` in `fetch_docs.py`
  3. Re-zip and re-upload the skill

## 🐛 Troubleshooting

### "Library not found"
- Try alternative names: "nextjs" vs "next.js"
- Check if library exists: https://context7.com
- Some libraries might not be indexed yet

### "Failed to fetch documentation"
- Check internet connection
- Verify API key is valid
- Context7 might be rate limiting (wait a few minutes)

### Skill not triggering
- Be explicit: mention library names clearly
- Try saying "use context7" or "fetch latest docs"
- Check if skill is enabled in settings

## 📖 Resources

- **Context7 Website**: https://context7.com
- **Add Libraries**: https://context7.com/add-library
- **GitHub**: https://github.com/upstash/context7
- **Claude Skills Guide**: https://support.claude.com/articles/12512198-how-to-create-custom-skills

## 🤝 Contributing

Found a bug or want to improve this skill?
1. Test your changes locally
2. Update version in SKILL.md
3. Share your improvements!

## 📝 Version History

- **v1.0.0** (2024-11-21): Initial release
  - Search library by name
  - Fetch documentation with topic filtering
  - Format docs for LLM consumption
  - Pre-configured with API key

---

Made with ❤️ for better AI-powered coding
