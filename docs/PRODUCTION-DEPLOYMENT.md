# Production Deployment Guide
# ===========================

## 🎯 Overview

This guide covers professional production deployment of the LGBTQ+ Sexual Fluidity Analysis Tool using Docker and Kubernetes.

---

## 📋 Prerequisites

### Required Tools

- **Docker** (v20.10+): Container runtime
- **Docker Compose** (v2.0+): Multi-container orchestration
- **Kubernetes** (v1.24+): Production orchestration
- **kubectl**: Kubernetes CLI
- **Git**: Version control
- **Make** (optional): Task automation

### Install Tools

```bash
# Docker Desktop (Windows/Mac)
# Download from: https://www.docker.com/products/docker-desktop

# Kubernetes (various options)
# - Docker Desktop (includes K8s)
# - Minikube: https://minikube.sigs.k8s.io/
# - K3s: https://k3s.io/
# - Cloud providers: GKE, EKS, AKS

# kubectl
# Windows (PowerShell):
choco install kubernetes-cli

# Mac:
brew install kubectl

# Linux:
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

---

## 🔑 Environment Setup

### 1. Create Environment File

```bash
# Backend environment
cd backend
cp .env.example .env  # If exists, or create new

# Required variables:
cat > .env <<EOF
GEMINI_API_KEY=your_actual_api_key_here
OPENAI_API_KEY=optional_openai_key
ENVIRONMENT=production
LOG_LEVEL=info
AI_PROVIDER=gemini
EOF
```

### 2. Set Environment Variables

```bash
# Export for scripts
export GEMINI_API_KEY="your_actual_api_key_here"
export DOCKER_REGISTRY="docker.io/yourusername"  # Optional
```

---

## 🐳 Docker Deployment

### Option 1: Using Makefile (Recommended)

```bash
# 1. Run all tests
make test

# 2. Build Docker images
make build

# 3. Start services
make up

# 4. View logs
make logs

# 5. Check status
make ps

# 6. Stop services
make down
```

### Option 2: Using Docker Compose Directly

```bash
# 1. Build images
docker-compose build

# 2. Start services
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Check health
docker-compose ps

# 5. Stop services
docker-compose down
```

### Option 3: Using Test Script

```bash
# Run automated test script
chmod +x scripts/test-docker.sh
./scripts/test-docker.sh
```

### Access Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

---

## ☸️ Kubernetes Deployment

### Option 1: Using Makefile (Recommended)

```bash
# Full production deployment (tests, builds, deploys)
make prod-deploy

# Or step by step:
make test              # Run tests
make prod-build        # Build images
make prod-push         # Push to registry (optional)
make k8s-deploy        # Deploy to K8s

# Check status
make k8s-status

# View logs
make k8s-logs

# Delete deployment
make k8s-delete
```

### Option 2: Using Deployment Script

```bash
# Make script executable
chmod +x scripts/deploy-production.sh

# Run deployment
./scripts/deploy-production.sh
```

### Option 3: Manual kubectl Commands

```bash
# 1. Create namespace
kubectl apply -f k8s/namespace.yaml

# 2. Create ConfigMap
kubectl apply -f k8s/configmap.yaml

# 3. Create secrets
kubectl create secret generic ai-api-keys \
  -n lgbtq-analysis \
  --from-literal=GEMINI_API_KEY="your_api_key_here" \
  --from-literal=OPENAI_API_KEY=""

# 4. Deploy backend
kubectl apply -f k8s/backend-deployment.yaml

# 5. Deploy frontend
kubectl apply -f k8s/frontend-deployment.yaml

# 6. Apply ingress
kubectl apply -f k8s/ingress.yaml

# 7. Apply HPA (autoscaling)
kubectl apply -f k8s/hpa.yaml

# 8. Check status
kubectl get all -n lgbtq-analysis

# 9. Wait for ready
kubectl wait --for=condition=available --timeout=300s \
  deployment/backend-deployment -n lgbtq-analysis
kubectl wait --for=condition=available --timeout=300s \
  deployment/frontend-deployment -n lgbtq-analysis
```

---

## 🧪 Testing

### Backend Tests

```bash
# Using Make
make test-backend

# Direct pytest
cd backend
pytest tests/ -v --tb=short

# With coverage
pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests

```bash
# Using Make
make test-frontend

# Direct vitest
cd frontend
npm run test

# Watch mode
npm run test -- --watch
```

### End-to-End Tests

```bash
# Using Make
make test-e2e

# Using docker-compose
docker-compose --profile test up --abort-on-container-exit cypress

# Interactive mode
cd frontend
npx cypress open
```

### Full Test Suite

```bash
# Run everything
make test
```

---

## 📊 Monitoring & Operations

### View Logs

```bash
# Docker Compose
docker-compose logs -f [service_name]
docker-compose logs -f backend
docker-compose logs -f frontend

# Kubernetes
kubectl logs -f -n lgbtq-analysis -l app=lgbtq-backend
kubectl logs -f -n lgbtq-analysis -l app=lgbtq-frontend

# Specific pod
kubectl logs -f -n lgbtq-analysis pod/backend-deployment-xxx
```

### Check Health

```bash
# Docker Compose
docker-compose ps
curl http://localhost:8000/health

# Kubernetes
kubectl get pods -n lgbtq-analysis
kubectl describe pod -n lgbtq-analysis backend-deployment-xxx
```

### Scale Services

```bash
# Kubernetes manual scaling
kubectl scale deployment/backend-deployment \
  -n lgbtq-analysis --replicas=5

# HPA will auto-scale based on CPU/memory
kubectl get hpa -n lgbtq-analysis
```

### Update Deployment

```bash
# Zero-downtime rolling update
kubectl set image deployment/backend-deployment \
  backend=lgbtq-backend:new-version \
  -n lgbtq-analysis

# Check rollout status
kubectl rollout status deployment/backend-deployment -n lgbtq-analysis

# Rollback if needed
kubectl rollout undo deployment/backend-deployment -n lgbtq-analysis
```

---

## 🔒 Security Best Practices

### 1. Secrets Management

```bash
# Never commit secrets to Git!
# Use Kubernetes secrets or external secret managers

# Kubernetes secrets
kubectl create secret generic ai-api-keys \
  -n lgbtq-analysis \
  --from-literal=GEMINI_API_KEY="xxx"

# External secret managers (production)
# - AWS Secrets Manager
# - Azure Key Vault
# - Google Secret Manager
# - HashiCorp Vault
```

### 2. Image Security

```bash
# Scan images for vulnerabilities
docker scan lgbtq-backend:latest
docker scan lgbtq-frontend:latest

# Use specific versions, not :latest in production
# Update base images regularly
```

### 3. Network Security

- Use Ingress with TLS/SSL certificates
- Enable Network Policies in Kubernetes
- Restrict pod-to-pod communication
- Use private container registry

---

## 🚀 Production Checklist

### Before Deployment

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Secrets properly managed
- [ ] Images scanned for vulnerabilities
- [ ] Resource limits set
- [ ] Health checks configured
- [ ] Monitoring setup
- [ ] Backup strategy defined
- [ ] Rollback plan ready

### After Deployment

- [ ] Verify all pods running
- [ ] Check health endpoints
- [ ] Test frontend access
- [ ] Test API endpoints
- [ ] Verify SSL/TLS
- [ ] Check logs for errors
- [ ] Monitor resource usage
- [ ] Test auto-scaling
- [ ] Verify data persistence

---

## 📈 Performance Tuning

### Backend Optimization

```yaml
# In k8s/backend-deployment.yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# Adjust based on load testing
```

### Frontend Optimization

- Enable gzip compression in nginx
- Configure caching headers
- Use CDN for static assets
- Optimize images

### Database (Future)

- Connection pooling
- Read replicas
- Caching layer (Redis)

---

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n lgbtq-analysis

# Describe pod for events
kubectl describe pod -n lgbtq-analysis pod-name

# Check logs
kubectl logs -n lgbtq-analysis pod-name

# Common issues:
# - Image pull errors
# - Missing secrets
# - Resource limits too low
# - Health check failures
```

### Service Not Accessible

```bash
# Check service
kubectl get svc -n lgbtq-analysis

# Check ingress
kubectl get ingress -n lgbtq-analysis
kubectl describe ingress -n lgbtq-analysis

# Test internal connectivity
kubectl run -it --rm debug --image=busybox -n lgbtq-analysis -- sh
wget -O- http://backend-service:8000/health
```

### High Memory/CPU Usage

```bash
# Check resource usage
kubectl top pods -n lgbtq-analysis

# Scale up if needed
kubectl scale deployment/backend-deployment --replicas=5 -n lgbtq-analysis

# Adjust resource limits
# Edit deployment YAML and apply
```

---

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run tests
        run: make test
      
      - name: Build images
        run: make prod-build
      
      - name: Push to registry
        run: make prod-push
        env:
          DOCKER_REGISTRY: ${{ secrets.DOCKER_REGISTRY }}
      
      - name: Deploy to K8s
        run: make k8s-deploy
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          KUBECONFIG: ${{ secrets.KUBECONFIG }}
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

---

## 🆘 Support

For issues or questions:
1. Check logs first
2. Review troubleshooting section
3. Open GitHub issue with logs
4. Contact development team

---

**Last Updated**: October 2025  
**Version**: 2.0  
**Status**: Production Ready ✅
