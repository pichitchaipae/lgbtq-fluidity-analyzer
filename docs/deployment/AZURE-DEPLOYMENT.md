# Azure Deployment Guide for LGBTQ+ Fluidity Analyzer

This guide walks you through deploying the LGBTQ+ Fluidity Analyzer to **Azure Container Apps** using your **GitHub Education** benefits.

---

## Prerequisites

### 1. Activate GitHub Student Developer Pack

1. Visit: https://education.github.com/pack
2. Verify your student status (takes 1-3 days)
3. Once approved, claim your Azure for Students benefit

### 2. Activate Azure for Students

1. Visit: https://azure.microsoft.com/en-us/free/students/
2. Sign in with your school email
3. No credit card required
4. Get **$100 credit** (renews annually while you're a student)

### 3. Install Azure CLI (if deploying manually)

**Windows (PowerShell):**
```powershell
winget install -e --id Microsoft.AzureCLI
```

**macOS:**
```bash
brew install azure-cli
```

**Linux:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Verify installation:
```bash
az --version
```

---

## Deployment Options

### Option 1: Automated GitHub Actions (Recommended)

This uses the workflow at `.github/workflows/azure-deploy.yml` for automatic deployments.

#### Step 1: Set Up Azure Service Principal

```powershell
# Login to Azure
az login

# Get your subscription ID
az account show --query id -o tsv

# Create service principal (save the output!)
az ad sp create-for-rbac \
  --name "github-actions-lgbtq-app" \
  --role contributor \
  --scopes /subscriptions/{SUBSCRIPTION_ID} \
  --sdk-auth
```

**Save the JSON output** - you'll need these values:
- `clientId`
- `clientSecret` 
- `subscriptionId`
- `tenantId`

#### Step 2: Add GitHub Secrets

Go to: `https://github.com/{YOUR_USERNAME}/lgbtq-fluidity-analyzer/settings/secrets/actions`

Add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `AZURE_CLIENT_ID` | From `clientId` | Service Principal ID |
| `AZURE_TENANT_ID` | From `tenantId` | Azure AD Tenant ID |
| `AZURE_SUBSCRIPTION_ID` | From `subscriptionId` | Azure Subscription ID |
| `AZURE_CLIENT_SECRET` | From `clientSecret` | Service Principal Secret |
| `GEMINI_API_KEY` | Your Gemini API key | AI Provider Key |
| `OPENAI_API_KEY` | Your OpenAI key (optional) | Alternative AI Provider |

#### Step 3: Trigger Deployment

**Option A: Push to main branch**
```bash
git push origin main
```

**Option B: Manual trigger**
1. Go to: Actions → Deploy to Azure Container Apps
2. Click "Run workflow"
3. Select "production" environment
4. Click "Run workflow"

#### Step 4: Access Your Application

After deployment completes (5-10 minutes), check the workflow logs for URLs:

```
🚀 Deployment Complete!
Backend URL: https://lgbtq-backend.{random}.azurecontainerapps.io
Frontend URL: https://lgbtq-frontend.{random}.azurecontainerapps.io
API Docs: https://lgbtq-backend.{random}.azurecontainerapps.io/docs
```

---

### Option 2: Manual Deployment via CLI

If you prefer manual control:

#### Step 1: Login and Set Subscription

```powershell
# Login
az login

# List subscriptions
az account list --output table

# Set active subscription
az account set --subscription "{SUBSCRIPTION_ID}"
```

#### Step 2: Create Resource Group

```powershell
az group create \
  --name lgbtq-fluidity-analyzer \
  --location southeastasia
```

#### Step 3: Create Container Apps Environment

```powershell
# Create environment
az containerapp env create \
  --name lgbtq-env \
  --resource-group lgbtq-fluidity-analyzer \
  --location southeastasia
```

#### Step 4: Deploy Backend

```powershell
az containerapp create \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer \
  --environment lgbtq-env \
  --image ghcr.io/pichitchaipae/lgbtq-backend:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server ghcr.io \
  --registry-username pichitchaipae \
  --registry-password {GITHUB_PAT} \
  --env-vars \
    AI_PROVIDER=gemini \
    GEMINI_API_KEY={YOUR_KEY} \
  --cpu 0.5 \
  --memory 1.0Gi \
  --min-replicas 1 \
  --max-replicas 3
```

#### Step 5: Deploy Frontend

```powershell
# Get backend URL
$BACKEND_URL = az containerapp show \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer \
  --query properties.configuration.ingress.fqdn \
  -o tsv

# Deploy frontend
az containerapp create \
  --name lgbtq-frontend \
  --resource-group lgbtq-fluidity-analyzer \
  --environment lgbtq-env \
  --image ghcr.io/pichitchaipae/lgbtq-frontend:latest \
  --target-port 80 \
  --ingress external \
  --registry-server ghcr.io \
  --registry-username pichitchaipae \
  --registry-password {GITHUB_PAT} \
  --env-vars \
    REACT_APP_API_URL=https://$BACKEND_URL \
  --cpu 0.25 \
  --memory 0.5Gi \
  --min-replicas 1 \
  --max-replicas 2
```

---

## Cost Estimation

With Azure for Students ($100/month credit):

| Resource | Cost | Your Cost |
|----------|------|-----------|
| Container Apps Environment | ~$0 (shared) | **$0** |
| Backend (0.5 vCPU, 1GB RAM) | ~$15/month | **$15** |
| Frontend (0.25 vCPU, 0.5GB RAM) | ~$8/month | **$8** |
| Bandwidth (first 5GB free) | ~$2/month | **$2** |
| **Total** | **~$25/month** | **$25/month** |

**✅ Result:** You can run this 24/7 for **FREE** with your $100 credit for 4 months!

---

## Monitoring & Management

### View Logs

```powershell
# Backend logs
az containerapp logs show \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer \
  --follow

# Frontend logs
az containerapp logs show \
  --name lgbtq-frontend \
  --resource-group lgbtq-fluidity-analyzer \
  --follow
```

### Update Environment Variables

```powershell
# Update backend API key
az containerapp update \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer \
  --set-env-vars GEMINI_API_KEY={NEW_KEY}
```

### Scale Application

```powershell
# Manual scaling
az containerapp update \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer \
  --min-replicas 2 \
  --max-replicas 5
```

### Check Application Status

```powershell
az containerapp show \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer \
  --query "{Name:name, Status:properties.provisioningState, URL:properties.configuration.ingress.fqdn}"
```

---

## Custom Domain (Optional)

### Step 1: Add Custom Domain

```powershell
az containerapp hostname add \
  --name lgbtq-frontend \
  --resource-group lgbtq-fluidity-analyzer \
  --hostname your-domain.com
```

### Step 2: Configure DNS

Add CNAME record:
```
your-domain.com → lgbtq-frontend.{random}.azurecontainerapps.io
```

### Step 3: Enable HTTPS

```powershell
az containerapp hostname bind \
  --name lgbtq-frontend \
  --resource-group lgbtq-fluidity-analyzer \
  --hostname your-domain.com \
  --validation-method CNAME
```

---

## Cleanup (When Testing)

To avoid using credits during development:

```powershell
# Stop apps (doesn't delete data)
az containerapp revision deactivate \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer

# Or delete everything
az group delete \
  --name lgbtq-fluidity-analyzer \
  --yes
```

---

## Troubleshooting

### Issue: Container won't start

**Check logs:**
```powershell
az containerapp logs show --name lgbtq-backend --resource-group lgbtq-fluidity-analyzer --tail 50
```

**Common causes:**
- Missing environment variables
- Wrong port configuration
- Image pull failures

### Issue: Cannot access application

**Check ingress configuration:**
```powershell
az containerapp ingress show \
  --name lgbtq-backend \
  --resource-group lgbtq-fluidity-analyzer
```

### Issue: Out of credits

**Check spending:**
```powershell
az consumption usage list --output table
```

---

## Security Best Practices

1. **Never commit secrets** - Always use Azure Key Vault or GitHub Secrets
2. **Use managed identities** - Enable for production deployments
3. **Enable HTTPS only** - Container Apps provides free SSL
4. **Monitor costs** - Set up billing alerts in Azure Portal
5. **Rotate API keys** - Update keys monthly

---

## Next Steps

1. ✅ Deploy to Azure Container Apps
2. ✅ Set up custom domain (optional)
3. ✅ Configure monitoring and alerts
4. ✅ Set up CI/CD pipeline
5. ✅ Enable auto-scaling based on traffic

---

## Support Resources

- **Azure Container Apps Docs:** https://learn.microsoft.com/en-us/azure/container-apps/
- **GitHub Actions for Azure:** https://github.com/Azure/actions
- **Azure for Students:** https://azure.microsoft.com/en-us/free/students/
- **Project Issues:** https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/issues

---

## Estimated Timeline

- **Setup Azure Account:** 5-10 minutes
- **Configure GitHub Secrets:** 5 minutes
- **First Deployment:** 10-15 minutes
- **Testing & Verification:** 10 minutes
- **Total:** ~30-45 minutes

**Ready to deploy?** Follow Option 1 (GitHub Actions) for the smoothest experience! 🚀
