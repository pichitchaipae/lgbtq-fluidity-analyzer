## Security & Secrets Management Rules

**FOR ALL AI ASSISTANTS WORKING ON THIS PROJECT**

### ⚠️ CRITICAL: Never Put Secrets in Git

This project has had **3 API key exposure incidents**. Learn from them.

**NEVER include real secrets in**:
- Documentation files (`.md`)
- Committed config files
- Code examples or comments
- Commit messages

**ALWAYS use placeholders**:
```bash
API_KEY=your_api_key_here
SECRET=[YOUR_SECRET]
TOKEN=${YOUR_TOKEN}
```

**Safe locations for real secrets**:
- `backend/.env` (gitignored)
- `.azure-secrets.local.txt` (gitignored)
- GitHub Secrets (web UI only)
- Azure Key Vault (production)

### Full Guidelines

See: `.github/AI-ASSISTANT-INSTRUCTIONS.md`

### Pre-Commit Check

Before suggesting commits:
```bash
# Check for potential secrets
git diff --cached | grep -E "AIza|sk-proj|xox|ghp_" | grep -v "placeholder"
```

### Remember

🔐 **Prevention > Detection > Response**

When user shares a secret:
1. Store in `.env` (gitignored)
2. Use placeholder in docs
3. Never echo it back
4. Remind about security
