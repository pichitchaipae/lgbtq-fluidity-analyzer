# GitHub Secrets Setup for Azure Deployment

## 🔐 Required Secrets

You need to add **2 secrets** to your GitHub repository for Azure deployment to work.

### 📍 Where to Add Secrets

Go to: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/settings/secrets/actions

Click **"New repository secret"** for each one below.

---

## Secret 1: AZURE_CREDENTIALS

**Name:** `AZURE_CREDENTIALS`

**Value:** (Copy the entire JSON block below, replacing values from `.azure-secrets.local.txt`)

```json
{
  "clientId": "YOUR_AZURE_CLIENT_ID",
  "clientSecret": "YOUR_AZURE_CLIENT_SECRET",
  "subscriptionId": "YOUR_AZURE_SUBSCRIPTION_ID",
  "tenantId": "YOUR_AZURE_TENANT_ID"
}
```

### 🔧 How to Create This Secret

1. Open `.azure-secrets.local.txt` (in your project root, gitignored)
2. Copy this template and replace with YOUR values from `.azure-secrets.local.txt`:

```json
{
  "clientId": "[YOUR_AZURE_CLIENT_ID]",
  "clientSecret": "[YOUR_AZURE_CLIENT_SECRET]",
  "subscriptionId": "[YOUR_AZURE_SUBSCRIPTION_ID]",
  "tenantId": "[YOUR_AZURE_TENANT_ID]"
}
```

3. Go to GitHub → Settings → Secrets → Actions
4. Click "New repository secret"
5. Name: `AZURE_CREDENTIALS`
6. Value: Paste the JSON (all one line or formatted, both work)
7. Click "Add secret"

---

## Secret 2: GEMINI_API_KEY

**Name:** `GEMINI_API_KEY`

**Value:** `YOUR_GEMINI_API_KEY_HERE`

### 🔧 How to Create This Secret

1. Open `.azure-secrets.local.txt`
2. Copy the value after `GEMINI_API_KEY=` (Key #4)
3. Go to GitHub → Settings → Secrets → Actions
4. Click "New repository secret"
5. Name: `GEMINI_API_KEY`
6. Value: Paste your API key (starts with `AIzaSy...`)
7. Click "Add secret"

---

## ✅ Verification

After adding both secrets, you should see:

- ✅ AZURE_CREDENTIALS
- ✅ GEMINI_API_KEY

Total: **2 secrets**

---

## 🚀 Next Steps

Once secrets are added:

1. **Push a change** to trigger deployment:
   ```bash
   git add .
   git commit -m "fix: Update Azure workflow authentication"
   git push origin azure-deployment
   ```

2. **Or merge to main**:
   - Create PR from `azure-deployment` to `main`
   - Merge PR → Auto-deploys

3. **Or manually trigger**:
   - Go to Actions → Azure Deploy → Run workflow

4. **Monitor deployment**:
   - https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/actions
   - Takes 10-15 minutes
   - Check logs for deployment URLs

---

## 🔍 Troubleshooting

### Error: "Login failed"
- Check that `AZURE_CREDENTIALS` is valid JSON
- Verify all 4 values are correct (from `.azure-secrets.local.txt`)
- Make sure there are no extra spaces or line breaks

### Error: "AADSTS70025: No federated identity credentials"
- ✅ **Fixed!** Workflow now uses client secret authentication
- Make sure you're using the updated workflow file

### Error: "Invalid API key"
- Check that `GEMINI_API_KEY` matches the key in `.azure-secrets.local.txt`
- Verify the key hasn't been revoked

---

## ⚠️ Security Reminder

**Before going live, revoke the 3 exposed API keys:**

Go to: https://aistudio.google.com/app/apikeys

Revoke keys ending in:
- `...O5E4` (Incident #1)
- `...NOg` (Incident #2)
- `...I-tA` (Incident #3)

Keep active:
- `...m9us` (Key #4 - Current)

---

## 📚 References

- [Azure Login Action](https://github.com/Azure/login)
- [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/)
