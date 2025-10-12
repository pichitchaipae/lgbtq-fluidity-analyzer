# Copilot Instructions

This file provides context and instructions for GitHub Copilot and other AI assistants working on this project.

## 🚨 CRITICAL SECURITY RULE

**NEVER put real API keys, tokens, passwords, or secrets in any files tracked by Git!**

See detailed instructions: `.github/AI-ASSISTANT-INSTRUCTIONS.md`

## Project Context

This is the **LGBTQ+ Sexual Fluidity Analysis Tool** - a web application that:
- Provides AI-powered chatbot for LGBTQ+ support
- Analyzes sexual fluidity survey data
- Deployed on Azure Container Apps
- Uses FastAPI backend + React frontend

## Security History

**This project has had 3 API key exposure incidents** (all caught within minutes):
1. Keys in `.history/` directory
2. Replacement keys in documentation
3. Third key in Azure setup docs

**All exposed keys were revoked immediately.**

## AI Assistant Rules

When user provides secrets:
1. ✅ Store ONLY in `.env` files (gitignored)
2. ✅ Use placeholders in all documentation
3. ✅ Never echo back the actual secret
4. ✅ Remind user about security best practices

Example placeholders:
```bash
API_KEY=[YOUR_API_KEY_HERE]
API_KEY=your_key_here
API_KEY=${YOUR_KEY}
```

## Safe Locations for Secrets

Gitignored (safe):
- `backend/.env`
- `.azure-secrets.local.txt`
- Any `*.local.*` files

External (safe):
- GitHub Secrets (via web UI)
- Azure Key Vault

Never (unsafe):
- Any `.md` files
- Any tracked configuration files
- Commit messages
- Code comments

## Quick Checks Before Suggesting Code

- [ ] No hardcoded secrets?
- [ ] Using environment variables?
- [ ] Documentation uses placeholders?
- [ ] User reminded about `.env` setup?

## More Information

Full security guidelines: `.github/AI-ASSISTANT-INSTRUCTIONS.md`

---

**Remember**: Prevention is better than detection! 🔐
