# 🎉 Azure Setup Complete!

## ✅ What We've Done

1. ✅ Installed Azure CLI
2. ✅ Logged into Azure (Azure for Students subscription)
3. ✅ Created Service Principal for GitHub Actions
4. ✅ Created Resource Group: `lgbtq-fluidity-analyzer`
5. ✅ Created Container Apps Environment: `lgbtq-env`

---

## 📋 IMPORTANT: Add These GitHub Secrets

Go to: **https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/settings/secrets/actions**

Click **"New repository secret"** and add each of these **2 secrets**:

### 1. AZURE_CREDENTIALS

**Format**: JSON (paste the entire block below with your values)

```json
{
  "clientId": "[YOUR_CLIENT_ID]",
  "clientSecret": "[YOUR_CLIENT_SECRET]",
  "subscriptionId": "[YOUR_SUBSCRIPTION_ID]",
  "tenantId": "[YOUR_TENANT_ID]"
}
```

**Where to find values**: `.azure-secrets.local.txt` (gitignored) or output from `azure-setup.ps1`

### 2. GEMINI_API_KEY

```
[YOUR_GEMINI_API_KEY]
```

**Where to find value**: `.azure-secrets.local.txt` or `backend/.env`

> **📚 Detailed Instructions**: See `docs/deployment/GITHUB-SECRETS-SETUP.md` for step-by-step guide.

---

## 🚀 Next Step: Deploy to Azure

### Option 1: Automatic Deployment (Recommended)

Push the new Azure deployment configuration to GitHub:

```powershell
git add .
git commit -m "feat: Add Azure Container Apps deployment configuration"
git push origin main
```

The GitHub Actions workflow will automatically:
1. Build Docker images
2. Push to GitHub Container Registry
3. Deploy to Azure Container Apps
4. Show you the application URLs

### Option 2: Manual Trigger

If you don't want to push code yet:

1. First, add all the GitHub secrets above
2. Go to: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/actions
3. Click "Deploy to Azure Container Apps"
4. Click "Run workflow"
5. Select "production"
6. Click "Run workflow"

---

## 📊 Monitor Deployment

1. Go to: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/actions
2. Click on the running workflow
3. Watch the deployment progress (takes 10-15 minutes)
4. When complete, you'll see output like:

```
🚀 Deployment Complete!
Backend URL: https://lgbtq-backend.redhill-721b7e91.southeastasia.azurecontainerapps.io
Frontend URL: https://lgbtq-frontend.redhill-721b7e91.southeastasia.azurecontainerapps.io
API Docs: https://lgbtq-backend.redhill-721b7e91.southeastasia.azurecontainerapps.io/docs
```

---

## 💰 Cost Tracking

Your Azure for Students account:
- **Credit**: $100 (renews annually)
- **Estimated cost**: ~$25/month
- **Free runtime**: ~4 months

To check your spending:
```powershell
az consumption usage list --output table
```

Or visit: https://portal.azure.com → Cost Management

---

## 🔍 Azure Resources Created

| Resource Type | Name | Location |
|---------------|------|----------|
| Resource Group | lgbtq-fluidity-analyzer | Southeast Asia |
| Container Apps Environment | lgbtq-env | Southeast Asia |
| Log Analytics Workspace | workspace-lgbtqfluidityanalyzernAC2 | Southeast Asia |

**Azure Portal**: https://portal.azure.com/#@MahidolUniversity/resource/subscriptions/b70ccc25-8e0d-4eba-8830-f6bfc1393abe/resourceGroups/lgbtq-fluidity-analyzer/overview

---

## ⚠️ Security Notes

1. **Keep secrets safe** - Never commit the values above to GitHub
2. **Rotate secrets** - Consider rotating the Service Principal secret periodically
3. **Revoke old API keys** - Don't forget to revoke your exposed Gemini keys:
   - AIzaSyB9dKdmhUFXzZ3-WIVmogqZ6frOaTpO5E4
   - AIzaSyA_lnw5V8kjKTtpmOv9gj4_bhasknyXNOg

Revoke at: https://aistudio.google.com/app/apikeys

---

## 🛠️ Useful Commands

### View Container App Status
```powershell
az containerapp list --resource-group lgbtq-fluidity-analyzer --output table
```

### View Logs
```powershell
# Backend logs
az containerapp logs show --name lgbtq-backend --resource-group lgbtq-fluidity-analyzer --follow

# Frontend logs
az containerapp logs show --name lgbtq-frontend --resource-group lgbtq-fluidity-analyzer --follow
```

### Update Environment Variable
```powershell
az containerapp update \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer \
  --set-env-vars GEMINI_API_KEY=your_new_key
```

### Delete Everything (for testing)
```powershell
az group delete --name lgbtq-fluidity-analyzer --yes
```

---

## 📚 Documentation

- Full guide: `docs/deployment/AZURE-DEPLOYMENT.md`
- Azure Container Apps: https://learn.microsoft.com/en-us/azure/container-apps/
- Azure Portal: https://portal.azure.com

---

## ✅ Checklist

- [x] Azure CLI installed
- [x] Azure login successful
- [x] Service Principal created
- [x] Resource Group created
- [x] Container Apps Environment created
- [ ] **TODO: Add GitHub Secrets** ⬅️ DO THIS NOW
- [ ] TODO: Push code to GitHub
- [ ] TODO: Monitor deployment
- [ ] TODO: Access deployed application

---

**Ready to deploy?** Add the GitHub secrets, then push your code! 🚀
