# 🔑 Key Rotation Complete - Checklist

**Date**: October 13, 2025  
**New Key Generated**: Key #4 (Production Oct 2025/4)  
**Status**: ✅ Local files updated, GitHub Secret pending

---

## ✅ Completed Steps

1. ✅ **Generated new API key** (Key #4)
2. ✅ **Updated `.azure-secrets.local.txt`** (gitignored)
3. ✅ **Updated `backend/.env`** (gitignored)
4. ✅ **Verified files not tracked by Git**

---

## ⏳ Remaining Steps

### 1. Update GitHub Secret

**Go to**: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/settings/secrets/actions

**Update secret**:
- Name: `GEMINI_API_KEY`
- Click "Update secret" (not create new)
- Paste your new key
- Click "Update secret"

### 2. Revoke Old Keys at Google AI Studio

**Go to**: https://aistudio.google.com/app/apikeys

**Revoke these 3 keys**:
1. ❌ Key ending in `...O5E4` (Incident #1)
2. ❌ Key ending in `...NOg` (Incident #2)  
3. ❌ Key ending in `...I-tA` (Incident #3)

**How to revoke**:
- Find each key by description or last characters
- Click the trash/delete icon
- Confirm deletion

### 3. Test New Key Locally

```powershell
# Restart backend with new key
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

**Test at**: http://localhost:8000/docs
- Try the `/api/v1/chat` endpoint
- Verify no authentication errors

### 4. Close GitHub Secret Scanning Alerts

**Go to**: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/security/secret-scanning

**For each open alert**:
1. Click "Close as"
2. Select "Revoked"
3. Confirm closure

### 5. Trigger Azure Redeployment

**Option A**: Push any change to trigger workflow
```powershell
git add DEPLOYMENT-STATUS.md SECURITY-INCIDENT-3.md KEY-ROTATION-CHECKLIST.md
git commit -m "docs: Add deployment and security incident documentation"
git push origin main
```

**Option B**: Manual trigger
1. Go to: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/actions
2. Click "Deploy to Azure Container Apps"
3. Click "Run workflow"
4. Select "production"
5. Click "Run workflow"

### 6. Update Azure Container App (After Deployment)

**Only if needed** (workflow should auto-update):
```powershell
az containerapp update \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer \
  --set-env-vars GEMINI_API_KEY=secretref:gemini-api-key
```

---

## 📊 Key Rotation Summary

| Key | Status | Location | Notes |
|-----|--------|----------|-------|
| Key #1 | ⏳ To revoke | Google | Exposed in incident #1 |
| Key #2 | ⏳ To revoke | Google | Exposed in incident #2 |
| Key #3 | ⏳ To revoke | Google | Exposed in incident #3 |
| **Key #4** | ✅ **Active** | Local files | **Current production key** |

---

## 🔐 Security Verification

After completing all steps, verify:

- [ ] ✅ New key works locally
- [ ] ✅ Old keys revoked at Google
- [ ] ✅ GitHub Secret updated
- [ ] ✅ Secret Scanning alerts closed
- [ ] ✅ Azure deployment uses new key
- [ ] ✅ No exposed keys in repository
- [ ] ✅ Application works in production

---

## 📝 Notes

**Key Security**:
- ✅ New key stored ONLY in gitignored files
- ✅ Not included in any documentation
- ✅ Not echoed in any commit messages
- ✅ Following AI-ASSISTANT-INSTRUCTIONS.md guidelines

**Lessons Applied**:
- Created permanent AI instruction files
- Updated README with security warnings
- Documented all past incidents
- Established secure key management workflow

---

## 🎯 Next Action

**Do this NOW**:
1. Update GitHub Secret (link above)
2. Revoke 3 old keys at Google
3. Test locally
4. Close GitHub alerts

**Then you're done!** ✅

---

## 📞 Support

If you encounter issues:
- Check `.azure-secrets.local.txt` for reference
- See `SECURITY-INCIDENT-3.md` for detailed history
- Review `.github/AI-ASSISTANT-INSTRUCTIONS.md` for guidelines

---

**Current Status**: 🟡 Partial - Waiting for GitHub Secret update and old key revocation
