# 🚀 Azure Deployment In Progress!

## Current Status

✅ Code pushed to GitHub (commit: f4571a3)
🔄 GitHub Actions workflow should be running now

---

## 📊 Monitor Deployment

### 1. GitHub Actions
**URL**: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/actions

Look for: **"Deploy to Azure Container Apps"** workflow

**Expected Timeline:**
- Build Backend Image: ~3-5 minutes
- Build Frontend Image: ~3-5 minutes
- Azure Login & Setup: ~1 minute
- Deploy Backend: ~2-3 minutes
- Deploy Frontend: ~2-3 minutes
- **Total: ~10-15 minutes**

### 2. Azure Portal
**Resource Group**: https://portal.azure.com/#@MahidolUniversity/resource/subscriptions/b70ccc25-8e0d-4eba-8830-f6bfc1393abe/resourceGroups/lgbtq-fluidity-analyzer/overview

Watch for Container Apps being created:
- `lgbtq-backend`
- `lgbtq-frontend`

---

## 🔍 Check Deployment Status via CLI

### Check if workflow is running
```powershell
# Install GitHub CLI if needed
winget install --id GitHub.cli

# Login
gh auth login

# Check workflow runs
gh run list --repo pichitchaipae/lgbtq-fluidity-analyzer --limit 5
```

### Watch workflow in terminal
```powershell
gh run watch --repo pichitchaipae/lgbtq-fluidity-analyzer
```

### Check Azure Container Apps
```powershell
# List all container apps
az containerapp list --resource-group lgbtq-fluidity-analyzer --output table

# Check specific app status
az containerapp show --name lgbtq-backend --resource-group lgbtq-fluidity-analyzer --query "{Name:name, Status:properties.provisioningState, URL:properties.configuration.ingress.fqdn}"
```

---

## 📝 Deployment Logs

### View GitHub Actions logs
1. Go to Actions tab
2. Click on the running workflow
3. Click on "build-and-deploy" job
4. Expand steps to see detailed logs

### View Azure Container logs
```powershell
# Backend logs
az containerapp logs show --name lgbtq-backend --resource-group lgbtq-fluidity-analyzer --follow

# Frontend logs
az containerapp logs show --name lgbtq-frontend --resource-group lgbtq-fluidity-analyzer --follow
```

---

## ✅ When Deployment Completes

The workflow will output your application URLs at the end:

```
🚀 Deployment Complete!
Backend URL: https://lgbtq-backend.{random}.southeastasia.azurecontainerapps.io
Frontend URL: https://lgbtq-frontend.{random}.southeastasia.azurecontainerapps.io
API Docs: https://lgbtq-backend.{random}.southeastasia.azurecontainerapps.io/docs
```

### Test Your Deployment

1. **Frontend**: Open the Frontend URL in your browser
2. **Backend API Docs**: Visit the API Docs URL to test endpoints
3. **Health Check**: Test the backend health endpoint

---

## ⚠️ If Deployment Fails

### Common Issues and Solutions

#### Issue: "AZURE_CREDENTIALS not found" or "Login failed"
**Solution**: Add the AZURE_CREDENTIALS secret to GitHub in JSON format:
```json
{
  "clientId": "[YOUR_CLIENT_ID]",
  "clientSecret": "[YOUR_CLIENT_SECRET]",
  "subscriptionId": "[YOUR_SUBSCRIPTION_ID]",
  "tenantId": "[YOUR_TENANT_ID]"
}
```

Check values in `.azure-secrets.local.txt` file.

> **📚 Detailed Guide**: See `docs/deployment/GITHUB-SECRETS-SETUP.md`

#### Issue: "Image pull failed"
**Solution**: GitHub Container Registry needs to be public or properly authenticated
```powershell
# Make images public on GitHub
# Go to: https://github.com/users/pichitchaipae/packages
# Click on each package → Package settings → Change visibility → Public
```

#### Issue: "Container failed to start"
**Solution**: Check application logs
```powershell
az containerapp logs show --name lgbtq-backend --resource-group lgbtq-fluidity-analyzer --tail 100
```

#### Issue: "Resource quota exceeded"
**Solution**: Check your Azure credits
```powershell
az consumption usage list --output table
```

### Manual Retry
If deployment fails, you can manually trigger it:
1. Go to Actions → Deploy to Azure Container Apps
2. Click "Run workflow"
3. Select "production"
4. Click "Run workflow"

---

## 🎯 Success Indicators

✅ GitHub Actions workflow shows green checkmark
✅ Container Apps show "Succeeded" status in Azure Portal
✅ Backend URL returns API documentation
✅ Frontend URL loads the application
✅ No errors in container logs

---

## 📋 Your Secrets Reference

**Local file**: `.azure-secrets.local.txt` (NOT committed to Git)

This file contains all your Azure secrets for reference.

**To view secrets**:
```powershell
Get-Content .\.azure-secrets.local.txt
```

---

## 💰 Cost Tracking

**Check spending**:
```powershell
az consumption usage list --start-date 2025-10-01 --end-date 2025-10-31 --output table
```

**View in portal**: https://portal.azure.com/#blade/Microsoft_Azure_CostManagement/Menu/overview

**Set up cost alerts**:
1. Go to Azure Portal → Cost Management + Billing
2. Create a budget: $25/month
3. Set alert at 80% ($20)

---

## 🔄 Next Deployment

After this first deployment, future updates are automatic:

**To deploy changes:**
```powershell
# Make your code changes
git add .
git commit -m "your changes"
git push origin main
```

GitHub Actions will automatically:
1. Build new Docker images
2. Push to registry
3. Update Azure Container Apps
4. Zero-downtime rolling update

---

## 📞 Support

- **Azure Support**: https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade
- **GitHub Actions Docs**: https://docs.github.com/actions
- **Container Apps Docs**: https://learn.microsoft.com/azure/container-apps/

---

**Deployment initiated!** ⏳ Check the GitHub Actions tab for progress!
