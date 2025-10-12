#!/usr/bin/env pwsh
# Azure Deployment Setup Script for LGBTQ+ Fluidity Analyzer
# Run this script to set up Azure deployment

Write-Host "🚀 Azure Deployment Setup for LGBTQ+ Fluidity Analyzer" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
Write-Host "Checking Azure CLI installation..." -ForegroundColor Yellow
$azVersion = az --version 2>$null
if (-not $azVersion) {
    Write-Host "❌ Azure CLI is not installed!" -ForegroundColor Red
    Write-Host "Install it with: winget install -e --id Microsoft.AzureCLI" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
Write-Host ""

# Login to Azure
Write-Host "Logging in to Azure..." -ForegroundColor Yellow
az login
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to login to Azure" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Successfully logged in to Azure" -ForegroundColor Green
Write-Host ""

# Get subscription ID
Write-Host "Getting your Azure subscription..." -ForegroundColor Yellow
$subscriptionId = az account show --query id -o tsv
Write-Host "✅ Subscription ID: $subscriptionId" -ForegroundColor Green
Write-Host ""

# Prompt for GitHub username
Write-Host "Please enter your GitHub username:" -ForegroundColor Yellow
$githubUsername = Read-Host
Write-Host ""

# Create Service Principal for GitHub Actions
Write-Host "Creating Service Principal for GitHub Actions..." -ForegroundColor Yellow
Write-Host "⚠️  IMPORTANT: Save this output - you'll need it for GitHub Secrets!" -ForegroundColor Magenta
Write-Host ""

$spOutput = az ad sp create-for-rbac `
    --name "github-actions-lgbtq-app" `
    --role contributor `
    --scopes "/subscriptions/$subscriptionId" `
    --json-auth

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create service principal" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Service Principal created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "📋 GitHub Secrets Configuration" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Parse the JSON output
$sp = $spOutput | ConvertFrom-Json

Write-Host "Add these secrets to your GitHub repository:" -ForegroundColor Yellow
Write-Host "https://github.com/$githubUsername/lgbtq-fluidity-analyzer/settings/secrets/actions" -ForegroundColor Blue
Write-Host ""

Write-Host "Secret Name: AZURE_CLIENT_ID" -ForegroundColor Green
Write-Host "Value: $($sp.clientId)" -ForegroundColor White
Write-Host ""

Write-Host "Secret Name: AZURE_TENANT_ID" -ForegroundColor Green
Write-Host "Value: $($sp.tenantId)" -ForegroundColor White
Write-Host ""

Write-Host "Secret Name: AZURE_SUBSCRIPTION_ID" -ForegroundColor Green
Write-Host "Value: $($sp.subscriptionId)" -ForegroundColor White
Write-Host ""

Write-Host "Secret Name: AZURE_CLIENT_SECRET" -ForegroundColor Green
Write-Host "Value: $($sp.clientSecret)" -ForegroundColor White
Write-Host ""

Write-Host "Secret Name: GEMINI_API_KEY" -ForegroundColor Green
Write-Host "Value: [Your Gemini API Key]" -ForegroundColor Yellow
Write-Host ""

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to create resources now
Write-Host "Do you want to create Azure resources now? (y/n)" -ForegroundColor Yellow
$createNow = Read-Host
Write-Host ""

if ($createNow -eq 'y' -or $createNow -eq 'Y') {
    $resourceGroup = "lgbtq-fluidity-analyzer"
    $location = "southeastasia"
    
    Write-Host "Creating resource group: $resourceGroup" -ForegroundColor Yellow
    az group create --name $resourceGroup --location $location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Resource group created successfully!" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "Creating Container Apps environment..." -ForegroundColor Yellow
        az containerapp env create `
            --name lgbtq-env `
            --resource-group $resourceGroup `
            --location $location
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Container Apps environment created!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🎉 Azure setup complete!" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "Next steps:" -ForegroundColor Yellow
            Write-Host "1. Add the GitHub secrets shown above" -ForegroundColor White
            Write-Host "2. Push your code to GitHub (or trigger the workflow manually)" -ForegroundColor White
            Write-Host "3. Monitor deployment in GitHub Actions tab" -ForegroundColor White
            Write-Host ""
        } else {
            Write-Host "❌ Failed to create Container Apps environment" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Failed to create resource group" -ForegroundColor Red
    }
} else {
    Write-Host "Skipping resource creation." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To create resources later, run:" -ForegroundColor Yellow
    Write-Host "az group create --name lgbtq-fluidity-analyzer --location southeastasia" -ForegroundColor White
    Write-Host "az containerapp env create --name lgbtq-env --resource-group lgbtq-fluidity-analyzer --location southeastasia" -ForegroundColor White
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "📚 Documentation" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Full deployment guide: docs/deployment/AZURE-DEPLOYMENT.md" -ForegroundColor White
Write-Host ""
