# 🚀 Quick Start Guide - Production Deployment

## ✅ Tests Passed

- **Backend**: 12/12 tests passed ✅
- **Frontend**: 1/1 test passed ✅

## 🐳 Docker Quick Start

### Build & Run Locally

```powershell
# Build images
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Access the app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs

# Stop services
docker-compose down
```

### Using Makefile (Linux/Mac/WSL)

```bash
# Run tests
make test

# Build images
make build

# Start services
make up

# View logs
make logs

# Stop services
make down
```

## ☸️ Kubernetes Deployment

### Prerequisites

1. **Start Kubernetes cluster** (choose one):
   - Docker Desktop → Settings → Kubernetes → Enable
   - Minikube: `minikube start`
   - K3s, GKE, EKS, or AKS

2. **Verify kubectl works**:
   ```powershell
   kubectl version --client
   kubectl cluster-info
   ```

3. **Set your API key**:
   ```powershell
   $env:GEMINI_API_KEY = "AIzaSyA_lnw5V8kjKTtpmOv9gj4_bhasknyXNOg"
   ```

### Deploy to Kubernetes

```powershell
# 1. Create namespace
kubectl apply -f k8s/namespace.yaml

# 2. Create ConfigMap
kubectl apply -f k8s/configmap.yaml

# 3. Create secrets
kubectl create secret generic ai-api-keys `
  -n lgbtq-analysis `
  --from-literal=GEMINI_API_KEY="$env:GEMINI_API_KEY" `
  --from-literal=OPENAI_API_KEY=""

# 4. Deploy backend
kubectl apply -f k8s/backend-deployment.yaml

# 5. Deploy frontend
kubectl apply -f k8s/frontend-deployment.yaml

# 6. Apply ingress
kubectl apply -f k8s/ingress.yaml

# 7. Apply autoscaling
kubectl apply -f k8s/hpa.yaml

# 8. Check status
kubectl get all -n lgbtq-analysis

# 9. Watch pods come up
kubectl get pods -n lgbtq-analysis -w
```

### Using Makefile (Linux/Mac/WSL)

```bash
export GEMINI_API_KEY="your_key_here"

# Full deployment
make k8s-deploy

# Check status
make k8s-status

# View logs
make k8s-logs

# Delete everything
make k8s-delete
```

## 📊 Verify Deployment

### Docker Compose

```powershell
# Check container health
docker-compose ps

# Should show "healthy" for backend and frontend

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

### Kubernetes

```powershell
# Check pods
kubectl get pods -n lgbtq-analysis

# Should show all Running (2/2 or 1/1 READY)

# Check services
kubectl get svc -n lgbtq-analysis

# Get backend logs
kubectl logs -n lgbtq-analysis -l app=lgbtq-backend --tail=50

# Get frontend logs
kubectl logs -n lgbtq-analysis -l app=lgbtq-frontend --tail=50

# Port forward to test locally
kubectl port-forward -n lgbtq-analysis svc/backend-service 8000:8000
kubectl port-forward -n lgbtq-analysis svc/frontend-service 3000:80

# Then access:
# http://localhost:8000/health
# http://localhost:3000
```

## 🔧 Common Commands

### Docker

```powershell
# Rebuild single service
docker-compose build backend
docker-compose build frontend

# Restart single service
docker-compose restart backend
docker-compose restart frontend

# View logs of specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute command in container
docker-compose exec backend python -c "print('Hello')"

# Clean everything
docker-compose down -v
docker system prune -a
```

### Kubernetes

```powershell
# Scale manually
kubectl scale deployment/backend-deployment -n lgbtq-analysis --replicas=5

# Update image
kubectl set image deployment/backend-deployment backend=lgbtq-backend:v2 -n lgbtq-analysis

# Rollback deployment
kubectl rollout undo deployment/backend-deployment -n lgbtq-analysis

# Check rollout status
kubectl rollout status deployment/backend-deployment -n lgbtq-analysis

# Get pod shell
kubectl exec -it -n lgbtq-analysis <pod-name> -- /bin/sh

# View resource usage
kubectl top pods -n lgbtq-analysis
kubectl top nodes

# Delete specific resources
kubectl delete deployment backend-deployment -n lgbtq-analysis
kubectl delete svc backend-service -n lgbtq-analysis

# Delete everything in namespace
kubectl delete all --all -n lgbtq-analysis
```

## 📝 Environment Variables

### Required

- `GEMINI_API_KEY` - Google Gemini API key (required)

### Optional

- `OPENAI_API_KEY` - OpenAI API key (if using OpenAI)
- `AI_PROVIDER` - "gemini" (default) or "openai"
- `ENVIRONMENT` - "production" (default)
- `LOG_LEVEL` - "info" (default), "debug", "warning", "error"

## 🎯 Next Steps

1. ✅ **Tests passed** - Ready for deployment
2. 🐳 **Choose deployment method**:
   - Docker Compose for local/simple deployments
   - Kubernetes for production/scalable deployments
3. 🔑 **Configure secrets** properly
4. 🚀 **Deploy and test**
5. 📊 **Monitor logs and metrics**

## 📚 Full Documentation

- **Production Deployment**: `docs/PRODUCTION-DEPLOYMENT.md`
- **Security Guide**: `SECURITY-INCIDENT-REPORT.md`
- **API Documentation**: http://localhost:8000/docs (after starting)

## 🆘 Need Help?

Check the troubleshooting section in `docs/PRODUCTION-DEPLOYMENT.md`

---

**Ready to deploy!** 🎉
