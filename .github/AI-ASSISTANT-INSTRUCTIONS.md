# AI Assistant Instructions - Security & Secrets Management

**Purpose**: This file contains critical instructions for AI assistants (GitHub Copilot, ChatGPT, etc.) working on this project.

**Priority**: HIGHEST - Security Critical

---

## 🚨 CRITICAL RULE: NEVER PUT SECRETS IN DOCUMENTATION

### Absolute Prohibitions

**NEVER** include real API keys, passwords, tokens, or any secrets in:

1. ❌ Any `.md` files (README, docs, guides, tutorials, etc.)
2. ❌ Any files tracked by Git
3. ❌ Any configuration examples
4. ❌ Any code comments as examples
5. ❌ Any commit messages
6. ❌ Any workflow files (`.github/workflows/*.yml`)
7. ❌ Any deployment scripts committed to repo

### Why This Rule Exists

**Historical Context**: This project has had **3 API key exposure incidents**:
- Incident #1: Keys in `.history/` and multiple docs
- Incident #2: Replacement keys exposed in 8 documentation files
- Incident #3: Third key exposed in `AZURE-NEXT-STEPS.md`

All were detected by GitHub Secret Scanning within minutes, requiring immediate key revocation.

---

## ✅ CORRECT Way to Handle Secrets

### When User Provides API Keys

**User says**: "Here's my API key: AIzaSy..."

**AI MUST**:

1. ✅ **Store ONLY in gitignored files**:
   - `backend/.env`
   - `.azure-secrets.local.txt`
   - Any file matching `.gitignore` patterns

2. ✅ **Use placeholders in documentation**:
   ```markdown
   GEMINI_API_KEY=[YOUR_API_KEY_HERE]
   OPENAI_API_KEY=[Get from OpenAI Dashboard]
   AZURE_CLIENT_SECRET=[From azure-setup.ps1 output]
   ```

3. ✅ **Reference secret locations**:
   ```markdown
   Your API key is stored in:
   - Local: backend/.env (gitignored)
   - GitHub: Settings → Secrets → GEMINI_API_KEY
   ```

4. ✅ **Never echo back the actual key** in responses

### When Creating Documentation

**Always use these patterns**:

```markdown
# Bad (NEVER DO THIS):
GEMINI_API_KEY=AIzaSyD0Ao3JtDF4zNIitWyMUgKjLfTfgTXI-tA

# Good (ALWAYS DO THIS):
GEMINI_API_KEY=your_api_key_here
GEMINI_API_KEY=[YOUR_GEMINI_API_KEY]
GEMINI_API_KEY=<paste your key>
GEMINI_API_KEY=${GEMINI_API_KEY}
```

---

## � Consistency Rules

**CRITICAL**: Every change must maintain consistency across the entire project.

### When to Check for Consistency

**ALWAYS after**:
- Creating ANY new file (.md, .py, .js, .ts, etc.)
- Modifying ANY existing file
- Moving or renaming files
- Changing API endpoints
- Updating environment variables
- Modifying workflows
- Changing function signatures
- Adding new features

### What to Check

#### 1. Documentation Consistency

**After creating/modifying docs:**
- [ ] Check ALL related documentation files
- [ ] Update outdated instructions in other docs
- [ ] Verify cross-references are still valid
- [ ] Ensure terminology is consistent
- [ ] Update README if feature visibility changes

**Example**:
```
Created: docs/deployment/GITHUB-SECRETS-SETUP.md
Must check:
- docs/deployment/AZURE-DEPLOYMENT.md (mentions secrets?)
- docs/deployment/AZURE-SETUP-COMPLETE.md (secret instructions?)
- README.md (quick start mentions secrets?)
- .github/workflows/azure-deploy.yml (uses same secret names?)
```

#### 2. Code Consistency

**After creating/modifying code:**
- [ ] Check similar files use same patterns
- [ ] Verify naming conventions match existing code
- [ ] Ensure import styles are consistent
- [ ] Check error handling follows project patterns
- [ ] Update all call sites if signature changed
- [ ] Update tests to match changes

**Example**:
```
Changed: backend/app/api/v1/chat.py - new endpoint
Must check:
- frontend/src/api/chat.ts (calling endpoint?)
- backend/app/tests/test_chat.py (tests updated?)
- docs/api/endpoints.md (documented?)
- README.md (example usage?)
```

#### 3. Configuration Consistency

**After modifying config:**
- [ ] Check all environments use same variables
- [ ] Update .env.example if real .env changed
- [ ] Verify Docker configs match
- [ ] Check workflow files use same names
- [ ] Update setup guides

**Example**:
```
Changed: backend/.env (added NEW_API_KEY)
Must check:
- backend/.env.example (add NEW_API_KEY=placeholder)
- docker-compose.yml (pass NEW_API_KEY?)
- .github/workflows/*.yml (needs in secrets?)
- docs/deployment/*.md (setup instructions?)
```

### How to Find Related Files

**Use these commands**:

```bash
# Find all files mentioning a specific term
grep -r "old_endpoint_name" . --exclude-dir={node_modules,.git,.venv,venv}

# Find all documentation files
find docs -name "*.md"

# Find all Python files with similar names
find . -name "*chat*.py"

# Find all files modified in same feature area
git log --name-only --pretty=format: -- backend/app/api/ | sort -u
```

### Consistency Checklist

**Before ANY commit:**

1. [ ] **Documentation**: All docs referencing changed items updated?
2. [ ] **Code**: All similar code files follow same patterns?
3. [ ] **Tests**: Tests updated to match code changes?
4. [ ] **Config**: All config files consistent?
5. [ ] **Frontend**: If backend changed, frontend updated?
6. [ ] **Backend**: If frontend changed, backend handles it?
7. [ ] **Workflows**: CI/CD updated if deployment changed?
8. [ ] **README**: Quick start still accurate?
9. [ ] **Examples**: Code examples still work?
10. [ ] **Comments**: Code comments still accurate?

### Common Inconsistencies to Avoid

❌ **Bad Examples**:
- README says "run npm start", but package.json has "npm run dev"
- Docs mention old secret name, but workflow uses new name
- Frontend calls `/api/chat`, but backend has `/api/v1/chat`
- Some files use `camelCase`, others use `snake_case`
- One doc says "Azure for Students", another says "Azure Free Tier"
- Function renamed but old name still in comments/docs

✅ **Good Practice**:
- All docs use exact same command syntax
- Secret names match across docs, workflows, .env.example
- API endpoints match frontend calls exactly
- Consistent naming across all files of same type
- Terminology consistent across all documentation
- Comments and docs updated when code changes

---

## �📁 File Organization Rules

### Documentation File Structure

**CRITICAL**: Keep documentation organized! Random .md files in root cause clutter.

**Correct Locations for .md files**:

| File Type | Correct Location | Examples |
|-----------|------------------|----------|
| GitHub standards | Root directory | README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, LICENSE.md |
| Deployment guides | `docs/deployment/` | AZURE-DEPLOYMENT.md, K8S-DEPLOYMENT.md |
| How-to guides | `docs/guides/` | SETUP-GUIDE.md, API-GUIDE.md |
| Reports & summaries | `docs/reports/` | SECURITY-INCIDENT-REPORT.md, RELEASE-NOTES.md |
| Architecture docs | `docs/` | ARCHITECTURE.md, DATABASE-SCHEMA.md |
| GitHub workflows | `.github/` | PULL_REQUEST_TEMPLATE.md, ISSUE_TEMPLATE.md |
| Temporary/working | Root (move later) | Only during active work, must be moved |

**Wrong Locations** (avoid these):
- ❌ `AZURE-SETUP-COMPLETE.md` in root → Move to `docs/deployment/`
- ❌ `DEPLOYMENT-STATUS.md` in root → Move to `docs/deployment/`
- ❌ `SECURITY-INCIDENT-3.md` in root → Move to `docs/reports/`
- ❌ `KEY-ROTATION-CHECKLIST.md` in root → Move to `docs/deployment/`

### When Creating New .md Files

**AI Assistant MUST**:

1. ✅ **Determine correct location FIRST**
   - Is it a deployment guide? → `docs/deployment/`
   - Is it a how-to guide? → `docs/guides/`
   - Is it a report/summary? → `docs/reports/`
   - Is it general docs? → `docs/`
   - Is it a GitHub standard? → Root (only 5 allowed)

2. ✅ **Create in the correct location immediately**
   ```python
   # Good:
   create_file("docs/deployment/azure-setup.md")
   
   # Bad:
   create_file("AZURE-SETUP.md")  # Root is wrong!
   ```

3. ✅ **If unsure, ask the user**
   ```
   "I'm creating a deployment guide. Should I place it in:
   - docs/deployment/ (recommended)
   - docs/guides/
   - Or another location?"
   ```

4. ✅ **Update all references after moving**
   - Check README.md links
   - Check other documentation cross-references
   - Update relative paths

### When Organizing Existing Files

**If root directory has .md files that shouldn't be there**:

1. List the files and their suggested locations
2. Ask user: "Should I move these to docs/?"
3. After moving, update all references
4. Commit with clear message: "docs: Organize documentation files"

### Exception: Temporary Working Files

**Only these can temporarily stay in root**:
- Files being actively edited/reviewed
- Files user explicitly requests in root
- Must be moved to docs/ when work is complete

---

## 📁 Safe Locations for Real Secrets

### Gitignored Files (Check `.gitignore` first!)

These files are safe for real secrets:

1. ✅ `backend/.env` - Backend environment variables
2. ✅ `.azure-secrets.local.txt` - Azure credentials reference
3. ✅ `.env.local` - Local development overrides
4. ✅ `*.local.*` - Any file with `.local.` in name
5. ✅ `.secrets/` - Directory (if added to .gitignore)

### External Secret Managers (Best Practice)

For production:
1. ✅ GitHub Secrets (via web UI only)
2. ✅ Azure Key Vault
3. ✅ AWS Secrets Manager
4. ✅ Google Secret Manager
5. ✅ HashiCorp Vault

---

## 🔍 Pre-Commit Checklist for AI Assistants

Before suggesting any commit, verify:

### Security Checks:
- [ ] No API keys in changed files
- [ ] No passwords or tokens visible
- [ ] All examples use placeholders
- [ ] Documentation references safe locations
- [ ] `.gitignore` includes secret file patterns
- [ ] User reminded to keep secrets safe

### File Organization Checks:
- [ ] **New .md files created in correct docs/ subdirectory**
- [ ] **No random .md files left in root directory**
- [ ] **All documentation cross-references updated**

### Consistency Checks:
- [ ] **All related documentation reviewed for consistency**
- [ ] **Outdated references updated across project**
- [ ] **Code patterns consistent across similar files**
- [ ] **Naming conventions consistent everywhere**
- [ ] **Related files that reference changes are updated**

**Examples of consistency checks:**
- New deployment guide? → Check all deployment docs match
- Changed API endpoint? → Update docs + frontend + backend
- New secret added? → Update all setup guides + README
- Modified workflow? → Update deployment guides + troubleshooting
- Changed function signature? → Update all call sites + tests + docs
- New component added? → Ensure consistent naming with existing components

**Command to check**:
```bash
# Search for potential secrets before commit
git diff --cached | grep -i "api[_-]key\|secret\|password\|token" | grep -v "placeholder\|example\|\[YOUR"

# Check for .md files in root that should be moved
git ls-files "*.md" | grep -v "README\|CONTRIBUTING\|CODE_OF_CONDUCT\|SECURITY\|LICENSE"

# Find all files that might reference what you changed
grep -r "pattern_you_changed" . --exclude-dir={node_modules,.git,.venv,venv}
```

---

## 📋 Documentation Templates

### When Documenting Environment Variables

```markdown
## Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
# AI Provider Configuration
AI_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Azure Configuration (from azure-setup.ps1)
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
```

**To get your keys**:
- Gemini: https://aistudio.google.com/app/apikeys
- OpenAI: https://platform.openai.com/api-keys
- Azure: Run `.\scripts\azure-setup.ps1`
```

### When Documenting GitHub Secrets

```markdown
## GitHub Secrets Setup

Add these secrets at: `Settings → Secrets and variables → Actions`

| Secret Name | How to Get |
|-------------|------------|
| `GEMINI_API_KEY` | Get from Google AI Studio |
| `AZURE_CLIENT_ID` | Output from azure-setup.ps1 |
| `AZURE_CLIENT_SECRET` | Output from azure-setup.ps1 |

**Never paste actual values in documentation!**
```

---

## 🎯 AI Assistant Response Patterns

### When User Shares a Secret

**User**: "My API key is AIzaSyABC123..."

**AI Response Template**:
```
✅ I've updated your API key in backend/.env (gitignored)
⚠️ Never sharing the key back to you for security
📝 The key is NOT in any committed files
🔐 Remember to also add it to GitHub Secrets

Next steps: [continue with task]
```

### When Detecting a Secret in Code

**If AI notices a secret during code review**:
```
⚠️ SECURITY WARNING: I detected what looks like an API key in [file]

This file is tracked by Git and will be committed. 
I recommend:
1. Move the secret to backend/.env
2. Use environment variables in the code
3. Add placeholder in the tracked file

Would you like me to fix this?
```

---

## 🛡️ Security Principles

### Defense in Depth

1. **Prevention**: Never put secrets in tracked files
2. **Detection**: GitHub Secret Scanning alerts
3. **Response**: Immediate key revocation
4. **Recovery**: Generate new keys, update safely

### Least Privilege

- Local development: `.env` files
- CI/CD: GitHub Secrets (read-only by workflows)
- Production: Azure Key Vault with managed identities

### Assume Breach

- Treat any exposed key as compromised immediately
- Rotate keys regularly (monthly)
- Monitor API usage for anomalies
- Set up billing alerts

---

## 📚 Education: Why This Matters

### Real Impact of Key Exposure

1. **Unauthorized Usage**: Anyone can use your API quota
2. **Cost**: Attacker can rack up charges on your account
3. **Data Breach**: Access to your AI model responses
4. **Reputation**: Security incident affects project credibility

### This Project's Incidents

| Incident | Keys Exposed | Detection Time | Cost |
|----------|--------------|----------------|------|
| #1 | 1 key in multiple files | <5 minutes | $0 (caught early) |
| #2 | 2 keys in 8 files | <5 minutes | $0 (caught early) |
| #3 | 1 key in 1 file | 1 minute | $0 (caught early) |

**Total**: 3 incidents, 4 unique keys revoked, all caught by automation.

**Lesson**: Even with fast detection, prevention is better!

---

## 🤖 AI Assistant Self-Check

Before every response involving configuration/setup, ask yourself:

1. "Am I about to include a real secret in my response?"
2. "Will this file be committed to Git?"
3. "Should I use a placeholder instead?"
4. "Did I remind the user about security?"

**If in doubt**: Use a placeholder!

---

## 🔄 Key Rotation Workflow

When helping user rotate keys:

```markdown
### Safe Key Rotation Steps

1. Generate new key at provider
2. Update local .env file (gitignored)
3. Test locally
4. Update GitHub Secrets (via web UI)
5. Update production (Azure Key Vault or az containerapp update)
6. Revoke old key
7. Verify new key works everywhere
8. Close GitHub Secret Scanning alerts
```

---

## 📖 Reference

- GitHub Secret Scanning: https://docs.github.com/code-security/secret-scanning
- Azure Key Vault: https://learn.microsoft.com/azure/key-vault/
- OWASP Secrets Management: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

---

## ⚡ Quick Reference

```
DO:
✅ Use placeholders: [YOUR_KEY], your_key_here, ${VAR}
✅ Store in .env files (gitignored)
✅ Reference locations, not values
✅ Remind users about security

DON'T:
❌ Include real keys in .md files
❌ Echo back secrets user shared
❌ Commit secrets to Git
❌ Put secrets in code comments
```

---

**Last Updated**: October 13, 2025  
**Incidents Prevented by Following This**: TBD (start from incident #4)  
**AI Assistants**: If you're reading this, FOLLOW THESE RULES STRICTLY! 🔐
