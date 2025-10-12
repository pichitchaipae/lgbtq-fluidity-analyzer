# 🚀 Quick Start Script for Docker + K8s + Cypress

Write-Host "🏳️‍🌈 LGBTQ+ Sexual Fluidity Analysis Tool - Deployment Script" -ForegroundColor Magenta
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command {
    param($Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow
$prerequisites = @("docker", "kubectl", "node")
$missing = @()

foreach ($cmd in $prerequisites) {
    if (Test-Command $cmd) {
        Write-Host "  ✅ $cmd installed" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $cmd not found" -ForegroundColor Red
        $missing += $cmd
    }
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "❌ Missing required tools: $($missing -join ', ')" -ForegroundColor Red
    Write-Host "Please install them before continuing." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🎯 Select deployment option:" -ForegroundColor Cyan
Write-Host "  1. Docker Compose (Local Development)" -ForegroundColor White
Write-Host "  2. Docker Compose with Cypress Tests" -ForegroundColor White
Write-Host "  3. Kubernetes Deployment" -ForegroundColor White
Write-Host "  4. Kubernetes with Cypress Tests" -ForegroundColor White
Write-Host "  5. Build Docker Images Only" -ForegroundColor White
Write-Host "  6. Install Cypress Locally" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🐳 Starting with Docker Compose..." -ForegroundColor Green
        docker-compose up -d
        Write-Host ""
        Write-Host "✅ Services started!" -ForegroundColor Green
        Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Cyan
        Write-Host "   Backend: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📊 View logs: docker-compose logs -f" -ForegroundColor Yellow
        Write-Host "🛑 Stop: docker-compose down" -ForegroundColor Yellow
    }
    
    "2" {
        Write-Host ""
        Write-Host "🧪 Starting with Cypress Tests..." -ForegroundColor Green
        docker-compose up -d backend frontend
        Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        docker-compose --profile test up cypress
        Write-Host ""
        Write-Host "✅ Tests completed!" -ForegroundColor Green
        Write-Host "📹 Videos: cypress/videos/" -ForegroundColor Cyan
        Write-Host "📸 Screenshots: cypress/screenshots/" -ForegroundColor Cyan
    }
    
    "3" {
        Write-Host ""
        Write-Host "☸️ Deploying to Kubernetes..." -ForegroundColor Green
        
        # Check if kubectl can connect
        $null = kubectl cluster-info 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Cannot connect to Kubernetes cluster" -ForegroundColor Red
            Write-Host "Make sure Kubernetes is enabled in Docker Desktop or Minikube is running" -ForegroundColor Yellow
            exit 1
        }
        
        Write-Host "📦 Building images..." -ForegroundColor Yellow
        docker build -t lgbtq-backend:latest ./backend
        docker build -t lgbtq-frontend:latest ./frontend
        
        Write-Host "🚀 Applying Kubernetes manifests..." -ForegroundColor Yellow
        kubectl apply -f k8s/namespace.yaml
        kubectl apply -f k8s/configmap.yaml
        kubectl apply -f k8s/backend-deployment.yaml
        kubectl apply -f k8s/frontend-deployment.yaml
        kubectl apply -f k8s/hpa.yaml
        
        Write-Host ""
        Write-Host "✅ Deployed to Kubernetes!" -ForegroundColor Green
        Write-Host "📊 Check status: kubectl get all -n lgbtq-analysis" -ForegroundColor Cyan
        Write-Host "🔍 View logs: kubectl logs -f deployment/backend-deployment -n lgbtq-analysis" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🌐 Access application:" -ForegroundColor Yellow
        Write-Host "   kubectl port-forward svc/frontend-service 3000:80 -n lgbtq-analysis" -ForegroundColor White
        Write-Host "   kubectl port-forward svc/backend-service 8000:8000 -n lgbtq-analysis" -ForegroundColor White
    }
    
    "4" {
        Write-Host ""
        Write-Host "☸️🧪 Deploying with Cypress Tests..." -ForegroundColor Green
        
        # Deploy application first
        kubectl apply -f k8s/namespace.yaml
        kubectl apply -f k8s/configmap.yaml
        kubectl apply -f k8s/backend-deployment.yaml
        kubectl apply -f k8s/frontend-deployment.yaml
        
        Write-Host "⏳ Waiting for pods to be ready..." -ForegroundColor Yellow
        kubectl wait --for=condition=ready pod -l app=lgbtq-backend -n lgbtq-analysis --timeout=120s
        kubectl wait --for=condition=ready pod -l app=lgbtq-frontend -n lgbtq-analysis --timeout=120s
        
        Write-Host "🧪 Running Cypress tests..." -ForegroundColor Yellow
        kubectl apply -f k8s/cypress-job.yaml
        
        Write-Host ""
        Write-Host "✅ Cypress job started!" -ForegroundColor Green
        Write-Host "📊 Watch progress: kubectl get jobs -n lgbtq-analysis -w" -ForegroundColor Cyan
        Write-Host "📋 View logs: kubectl logs job/cypress-e2e-tests -n lgbtq-analysis" -ForegroundColor Cyan
    }
    
    "5" {
        Write-Host ""
        Write-Host "🔨 Building Docker images..." -ForegroundColor Green
        docker build -t lgbtq-backend:latest ./backend
        docker build -t lgbtq-frontend:latest ./frontend
        Write-Host ""
        Write-Host "✅ Images built successfully!" -ForegroundColor Green
        Write-Host "📦 Images:" -ForegroundColor Cyan
        docker images | Select-String "lgbtq"
    }
    
    "6" {
        Write-Host ""
        Write-Host "📦 Installing Cypress..." -ForegroundColor Green
        Set-Location frontend
        npm install cypress --save-dev
        Write-Host ""
        Write-Host "✅ Cypress installed!" -ForegroundColor Green
        Write-Host "🧪 Run tests:" -ForegroundColor Cyan
        Write-Host "   npm run cy:open    # Interactive mode" -ForegroundColor White
        Write-Host "   npm run cy:run     # Headless mode" -ForegroundColor White
        Set-Location ..
    }
    
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "✨ Deployment complete! Happy testing! 🏳️‍🌈" -ForegroundColor Magenta
