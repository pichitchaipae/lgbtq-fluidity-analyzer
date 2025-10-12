# Azure Deployment - Quick Start Steps

You've completed: ✅ Azure for Students activation

## Next Steps:

### Step 1: Restart PowerShell Terminal ⚠️
Azure CLI was just installed. You need to restart your PowerShell terminal to use it.

**How to restart:**
1. Close all PowerShell terminals in VS Code
2. Open a new terminal (Ctrl + `)
3. Continue with Step 2 below

---

### Step 2: Run Azure Setup Script

Open a **new PowerShell terminal** and run:

```powershell
cd "c:\Users\ASUS\Downloads\LGBTQ+ Sexual Fluidity Analysis Tool"
.\scripts\azure-setup.ps1
```

**What this script does:**
- Logs you into Azure
- Creates a Service Principal for GitHub Actions
- Shows you the exact secrets to add to GitHub
- Optionally creates Azure resources

**Follow the prompts:**
1. It will open a browser for Azure login
2. Enter your GitHub username when asked (pichitchaipae)
3. Save the secrets it shows you (you'll need them for GitHub)
4. Choose 'y' when asked to create resources

---

### Step 3: Add GitHub Secrets

After running the script, you'll have values in `.azure-secrets.local.txt` (gitignored).

**You need to add 2 secrets to GitHub:**

#### Secret 1: AZURE_CREDENTIALS

**Format**: JSON (combine the 4 Azure values into one)

```json
{
  "clientId": "[YOUR_AZURE_CLIENT_ID]",
  "clientSecret": "[YOUR_AZURE_CLIENT_SECRET]",
  "subscriptionId": "[YOUR_AZURE_SUBSCRIPTION_ID]",
  "tenantId": "[YOUR_AZURE_TENANT_ID]"
}
```

#### Secret 2: GEMINI_API_KEY

```
[YOUR_GEMINI_API_KEY]
```

**Add these to GitHub:**

1. Go to: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/settings/secrets/actions

2. Click "New repository secret"

3. For `AZURE_CREDENTIALS`: Paste the entire JSON block (with your actual values from `.azure-secrets.local.txt`)

4. For `GEMINI_API_KEY`: Paste your API key (from `.azure-secrets.local.txt` or `backend/.env`)

> **📚 Need Help?** See detailed guide: `docs/deployment/GITHUB-SECRETS-SETUP.md`

---

### Step 4: Push Code to GitHub

```powershell
git add .
git commit -m "feat: Add Azure Container Apps deployment configuration"
git push origin main
```

---

### Step 5: Monitor Deployment

1. Go to: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/actions

2. You should see "Deploy to Azure Container Apps" workflow running

3. Click on it to see progress (takes 10-15 minutes)

4. When complete, check the logs for your application URLs:
   ```
   🚀 Deployment Complete!
   Backend URL: https://lgbtq-backend.{random}.azurecontainerapps.io
   Frontend URL: https://lgbtq-frontend.{random}.azurecontainerapps.io
   API Docs: https://lgbtq-backend.{random}.azurecontainerapps.io/docs
   ```

---

## Alternative: Manual Trigger (if you don't want to push)

Instead of pushing code, you can manually trigger deployment:

1. Go to: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/actions
2. Click "Deploy to Azure Container Apps"
3. Click "Run workflow" button
4. Select "production" environment
5. Click "Run workflow"

---

## Troubleshooting

### If Azure CLI still not recognized after restart:
Close VS Code completely and reopen it.

### If login fails:
Make sure you're using the same email for Azure that you used for GitHub Education.

### If deployment fails:
Check that all 5 GitHub secrets are added correctly (no extra spaces or quotes).

---

## Current Status Checklist

- [x] ✅ Azure for Students activated
- [x] ✅ Azure CLI installed
- [ ] ⏳ PowerShell terminal restarted
- [ ] ⏳ Azure setup script executed
- [ ] ⏳ GitHub secrets added
- [ ] ⏳ Code pushed to GitHub
- [ ] ⏳ Deployment monitored
- [ ] ⏳ Application URL accessed

---

## 💰 Cost Reminder

With your $100 Azure credit:
- App costs ~$25/month to run 24/7
- You can run it FREE for 4 months!
- Credit renews annually while you're a student

---

## Need Help?

Full documentation: `docs/deployment/AZURE-DEPLOYMENT.md`
