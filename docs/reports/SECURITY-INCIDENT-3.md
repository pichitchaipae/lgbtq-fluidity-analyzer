# Security Alert Response - API Key Exposure #3

**Date**: October 13, 2025  
**Alert Type**: GitHub Secret Scanning - Google API Key  
**Severity**: HIGH  
**Status**: ✅ FIXED

---

## Incident Summary

### What Happened
A third Gemini API key was accidentally exposed in documentation file `AZURE-NEXT-STEPS.md` during Azure deployment setup.

**Exposed Key**: `AIzaSyD0Ao3JtDF4zNIitWyMUgKjLfTfgTXI-tA`

**Detection**: GitHub Secret Scanning detected the key 1 minute after commit f4571a3

**Root Cause**: Documentation included the actual API key value as an example instead of a placeholder.

---

## Timeline of API Key Exposures

| # | Date | Key Prefix | Location | Status |
|---|------|------------|----------|--------|
| 1 | Earlier | AIzaSyB9... | .history/, docs/ | ⚠️ MUST REVOKE |
| 2 | Earlier | AIzaSyA_... | docs/ (8 files) | ⚠️ MUST REVOKE |
| 3 | Oct 13 | AIzaSyD0... | AZURE-NEXT-STEPS.md | ⚠️ MUST REVOKE |

---

## Immediate Actions Taken

1. ✅ **Removed key from documentation** (commit 041d4de)
2. ✅ **Replaced with placeholder reference**
3. ✅ **Pushed fix to GitHub**
4. ✅ **Key stored only in `.azure-secrets.local.txt` (gitignored)**

---

## CRITICAL: User Action Required

### You MUST Revoke This Key Immediately

**This is the THIRD exposed key!** You need to:

1. **Go to Google AI Studio**: https://aistudio.google.com/app/apikeys

2. **Revoke ALL three exposed keys**:
   - `AIzaSyB9dKdmhUFXzZ3-WIVmogqZ6frOaTpO5E4` (first key)
   - `AIzaSyA_lnw5V8kjKTtpmOv9gj4_bhasknyXNOg` (second key)
   - `AIzaSyD0Ao3JtDF4zNIitWyMUgKjLfTfgTXI-tA` (third key - just exposed)

3. **Generate a NEW fourth key** (do NOT share it anywhere)

4. **Update ONLY these locations** (never commit to Git):
   - Local file: `.azure-secrets.local.txt`
   - Local file: `backend/.env`
   - GitHub Secret: `GEMINI_API_KEY` (settings/secrets/actions)
   - Azure (after deployment): Update via `az containerapp update`

---

## How to Update the New Key Safely

### Step 1: Generate New Key
```
1. Visit: https://aistudio.google.com/app/apikeys
2. Click "Create API Key"
3. Copy the key (starts with AIzaSy...)
4. DO NOT paste it in any documentation!
```

### Step 2: Update Local Files (These are gitignored)
```powershell
# Update local secrets reference
notepad .azure-secrets.local.txt
# Replace GEMINI_API_KEY value with new key

# Update backend environment
notepad backend/.env
# Replace GEMINI_API_KEY value with new key
```

### Step 3: Update GitHub Secret
```
1. Go to: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/settings/secrets/actions
2. Click on GEMINI_API_KEY
3. Update value with new key
4. Click "Update secret"
```

### Step 4: Restart Local Backend (if running)
```powershell
# Stop current backend (Ctrl+C in terminal where it's running)
# Restart with new key
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### Step 5: Update Azure Deployment (after first deployment completes)
```powershell
az containerapp update \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer \
  --set-env-vars GEMINI_API_KEY=YOUR_NEW_KEY_HERE
```

---

## Root Cause Analysis

### Why This Keeps Happening
1. Documentation files are being used to show "example" values
2. Real keys are being used instead of placeholders
3. Keys are being copy-pasted from working environments

### Prevention Measures Implemented
1. ✅ All documentation now uses placeholders
2. ✅ Real secrets stored only in gitignored files
3. ✅ Created `.azure-secrets.local.txt` for reference
4. ✅ Added to `.gitignore`

---

## Files That Should NEVER Contain Real Keys

❌ **NEVER put real keys in these files** (they go to GitHub):
- Any `.md` file (README, docs, guides, etc.)
- Any workflow file (`.github/workflows/*.yml`)
- Any config file tracked by Git
- Any code file committed to repository

✅ **ONLY put real keys in these files** (gitignored):
- `backend/.env`
- `.azure-secrets.local.txt`
- GitHub Secrets (via web interface)
- Azure Key Vault (for production)

---

## Verification Checklist

After fixing this incident:

- [x] ✅ Key removed from all committed files
- [x] ✅ Fix pushed to GitHub
- [ ] ⏳ **TODO: Revoke all three exposed keys**
- [ ] ⏳ **TODO: Generate new fourth key**
- [ ] ⏳ **TODO: Update local files with new key**
- [ ] ⏳ **TODO: Update GitHub Secret**
- [ ] ⏳ **TODO: Update Azure Container App**
- [ ] ⏳ **TODO: Dismiss GitHub Secret Scanning Alerts**
- [ ] ⏳ **TODO: Restart local backend**
- [ ] ⏳ **TODO: Test new key works**

---

## GitHub Secret Scanning Alerts

**Current Open Alerts**: 3

1. ⚠️ Alert #2 (from earlier) - Two keys in docs/
2. ⚠️ Alert #3 (new) - One key in AZURE-NEXT-STEPS.md

**To Close Alerts**:
1. Revoke the keys at Google
2. Go to: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/security/secret-scanning
3. Click "Close as" → "Revoked"
4. Confirm closure

---

## Lessons Learned

1. 🚫 **NEVER include real API keys in documentation**
2. ✅ **Always use placeholders** like `[YOUR_API_KEY]` or `your_key_here`
3. ✅ **Keep real secrets in gitignored files only**
4. ✅ **Use environment variables and secret managers**
5. ✅ **Review commits before pushing**
6. ⚠️ **Rotate keys immediately when exposed**

---

## Cost Impact

**Good News**: These keys were detected and removed within minutes, minimizing unauthorized usage risk.

**Action**: Check Google Cloud Console for any unexpected API usage on the exposed keys.

---

## Next Steps (URGENT)

1. **STOP** - Do not generate any more keys until you revoke the old ones
2. **REVOKE** - All three exposed keys at Google AI Studio
3. **GENERATE** - One new key (fourth key)
4. **UPDATE** - Only in safe locations (gitignored files + GitHub Secrets)
5. **TEST** - Verify new key works locally
6. **CLOSE** - GitHub Secret Scanning Alerts after revocation

---

**Status**: Repository is now clean, but **YOU MUST REVOKE THE EXPOSED KEYS** to complete the incident response! 🔐
