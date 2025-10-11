# 🐳 Docker & Kubernetes Deployment Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Why Kubernetes + Cypress?](#why-kubernetes--cypress)
- [Prerequisites](#prerequisites)
- [Docker Setup](#docker-setup)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Cypress E2E Testing](#cypress-e2e-testing)
- [CI/CD Integration](#cicd-integration)
- [Monitoring & Scaling](#monitoring--scaling)

---

## 🎯 Overview

This project uses **Docker** for containerization and **Kubernetes (K8s)** for orchestration, with **Cypress** for comprehensive end-to-end testing. The architecture supports:

- 🔒 **Privacy-first design** - No data persistence
- ♿ **Accessibility** - Bilingual support (Thai/English)
- 🌍 **SDG alignment** - SDG 3, 5, 10 compliance
- 📈 **Scalability** - Horizontal pod autoscaling
- 🧪 **Quality assurance** - Automated E2E testing

---

## 🤔 Why Kubernetes + Cypress?

### **Why Kubernetes?**

1. **High Availability** 🚀
   - Multi-replica deployments ensure zero downtime
   - Automatic failover and self-healing
   - Load balancing across pods

2. **Scalability** 📊
   - Horizontal Pod Autoscaler (HPA) adjusts replicas based on CPU/memory
   - Handles traffic spikes during research campaigns
   - Cost-effective resource utilization

3. **Privacy & Security** 🔐
   - Network policies isolate services
   - No persistent storage (in-memory processing only)
   - Security contexts prevent privilege escalation
   - RunAsNonRoot ensures container security

4. **Multi-Language Support** 🌐
   - ConfigMaps manage bilingual configurations
   - Easy updates without rebuilding images
   - Environment-specific settings (dev/staging/prod)

5. **SDG Compliance** 🎯
   - **SDG 3 (Health)**: High availability ensures students can access mental health resources
   - **SDG 5 (Gender Equality)**: Inclusive design accessible to all identities
   - **SDG 10 (Reduced Inequalities)**: Bilingual support reduces language barriers

### **Why Cypress?**

1. **Comprehensive E2E Testing** 🧪
   - Tests real user workflows (survey completion → results display)
   - Validates bilingual functionality (Thai ⇄ English toggle)
   - Ensures privacy compliance (no data persistence checks)

2. **Developer Experience** 👩‍💻
   - Time-travel debugging with snapshots
   - Real-time reloading during test development
   - Clear error messages and stack traces

3. **CI/CD Integration** ⚙️
   - Runs in Docker containers (consistent across environments)
   - Kubernetes Job executes tests in cluster
   - Video recordings and screenshots for debugging

4. **Cross-Browser Testing** 🌐
   - Chrome, Firefox, Edge support
   - Mobile viewport testing (responsive design validation)
   - Network throttling for performance testing

---

## 📦 Prerequisites

### Required Software:
- **Docker Desktop** 20.10+ (with Kubernetes enabled) or **Minikube**
- **kubectl** 1.25+
- **Node.js** 20+ (for local Cypress development)
- **Python** 3.12+ (for backend development)

### Optional Tools:
- **k9s** - Kubernetes CLI UI
- **Lens** - Kubernetes IDE
- **Docker Compose** - Local multi-container development

---

## 🐳 Docker Setup

### 1. Build Images

```bash
# Build backend image
cd backend
docker build -t lgbtq-backend:latest .

# Build frontend image
cd ../frontend
docker build -t lgbtq-frontend:latest .
```

### 2. Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Run with Cypress tests
docker-compose --profile test up

# Stop services
docker-compose down
```

**Services:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

### 3. Docker Compose Features

- **Health Checks**: Ensures services are ready before starting dependent containers
- **Networks**: Isolated `lgbtq-network` for inter-service communication
- **Profiles**: `test` profile runs Cypress tests on-demand
- **Restart Policies**: Automatic restart on failure

---

## ☸️ Kubernetes Deployment

### 1. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy configurations
kubectl apply -f k8s/configmap.yaml

# Deploy backend
kubectl apply -f k8s/backend-deployment.yaml

# Deploy frontend
kubectl apply -f k8s/frontend-deployment.yaml

# Deploy autoscaling
kubectl apply -f k8s/hpa.yaml

# Deploy ingress (optional)
kubectl apply -f k8s/ingress.yaml
```

### 2. Verify Deployment

```bash
# Check all resources
kubectl get all -n lgbtq-analysis

# Check pod status
kubectl get pods -n lgbtq-analysis

# Check services
kubectl get svc -n lgbtq-analysis

# View logs
kubectl logs -f deployment/backend-deployment -n lgbtq-analysis
kubectl logs -f deployment/frontend-deployment -n lgbtq-analysis
```

### 3. Access Application

```bash
# Port forward frontend
kubectl port-forward svc/frontend-service 3000:80 -n lgbtq-analysis

# Port forward backend
kubectl port-forward svc/backend-service 8000:8000 -n lgbtq-analysis

# Access via browser
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### 4. Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Ingress Controller                    │
│            (NGINX with rate limiting & TLS)              │
└────────────────┬────────────────────────┬────────────────┘
                 │                        │
         ┌───────▼───────┐        ┌──────▼──────┐
         │   Frontend    │        │   Backend   │
         │   Service     │        │   Service   │
         │  (LoadBalancer)│        │ (ClusterIP) │
         └───────┬───────┘        └──────┬──────┘
                 │                        │
    ┌────────────┼────────────┐  ┌───────┼───────┐
    │            │            │  │       │       │
┌───▼───┐   ┌───▼───┐   ┌───▼──▼──┐ ┌──▼───┐ ┌──▼───┐
│ Nginx │   │ Nginx │   │ Uvicorn│ │Uvicorn││Uvicorn│
│ Pod 1 │   │ Pod 2 │   │  Pod 1 │ │ Pod 2 ││ Pod 3 │
└───────┘   └───────┘   └────────┘ └───────┘└───────┘
    │           │             │         │        │
    └───────────┴─────────────┴─────────┴────────┘
                         │
                 ┌───────▼────────┐
                 │ HPA Controller │
                 │  Auto-scaling  │
                 └────────────────┘
```

---

## 🧪 Cypress E2E Testing

### 1. Run Cypress Locally

```bash
# Install Cypress
npm install cypress --save-dev

# Open Cypress UI
npx cypress open

# Run tests headless
npx cypress run

# Run specific test
npx cypress run --spec "cypress/e2e/lgbtq-analysis.cy.js"
```

### 2. Run Cypress in Docker

```bash
# Using Docker Compose
docker-compose --profile test up cypress

# Using standalone Docker
docker run -it \
  -v $PWD:/e2e \
  -w /e2e \
  --network lgbtq-network \
  -e CYPRESS_baseUrl=http://frontend:80 \
  cypress/included:13.6.0
```

### 3. Run Cypress in Kubernetes

```bash
# Deploy Cypress job
kubectl apply -f k8s/cypress-job.yaml

# Watch job progress
kubectl get jobs -n lgbtq-analysis -w

# View test logs
kubectl logs job/cypress-e2e-tests -n lgbtq-analysis

# Get test results
kubectl describe job cypress-e2e-tests -n lgbtq-analysis
```

### 4. Cypress Test Coverage

Our E2E tests cover:

✅ **Homepage & Language Toggle**
- Page loads successfully
- Privacy badges display
- Thai ⇄ English language switching

✅ **Survey Form**
- All 6 question groups render
- Radio button selection works
- Submit/Reset buttons functional

✅ **Results Display**
- Overall score calculation
- Section scores with emojis
- Disclaimer and references
- Bilingual result translation

✅ **API Integration**
- Backend connectivity
- Request/response validation
- Error handling

✅ **Responsive Design**
- Mobile viewport (iPhone X)
- Tablet viewport (iPad)
- Desktop viewport (1280x720)

---

## ⚙️ CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml (updated with K8s + Cypress)

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Backend tests
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run backend tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  # Frontend tests
  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run frontend tests
        run: |
          cd frontend
          npm ci
          npm run lint
          npm run build

  # Docker build
  docker-build:
    needs: [backend-test, frontend-test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build images
        run: docker-compose build

  # E2E tests with Cypress
  e2e-test:
    needs: docker-build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Start services
        run: docker-compose up -d
      - name: Wait for services
        run: |
          sleep 30
          curl --retry 10 --retry-delay 5 http://localhost:8000/health
      - name: Run Cypress tests
        run: docker-compose --profile test up --exit-code-from cypress
      - name: Upload test artifacts
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: cypress-videos
          path: cypress/videos

  # Deploy to Kubernetes
  deploy:
    needs: e2e-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to K8s
        run: |
          kubectl apply -f k8s/
```

---

## 📈 Monitoring & Scaling

### Horizontal Pod Autoscaling

```bash
# Check HPA status
kubectl get hpa -n lgbtq-analysis

# Example output:
# NAME           REFERENCE                     TARGETS    MINPODS   MAXPODS   REPLICAS
# backend-hpa    Deployment/backend-deployment  45%/70%   3         10        3
# frontend-hpa   Deployment/frontend-deployment 30%/75%   2         5         2
```

### Scaling Scenarios:

1. **Low Traffic** (< 70% CPU)
   - Backend: 3 pods
   - Frontend: 2 pods

2. **Medium Traffic** (70-85% CPU)
   - Backend: 5-7 pods
   - Frontend: 3-4 pods

3. **High Traffic** (> 85% CPU)
   - Backend: 10 pods (max)
   - Frontend: 5 pods (max)

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment backend-deployment --replicas=5 -n lgbtq-analysis

# Scale frontend
kubectl scale deployment frontend-deployment --replicas=3 -n lgbtq-analysis
```

---

## 🔧 Troubleshooting

### Common Issues:

1. **Pods not starting**
```bash
kubectl describe pod <pod-name> -n lgbtq-analysis
kubectl logs <pod-name> -n lgbtq-analysis
```

2. **Service not accessible**
```bash
kubectl get endpoints -n lgbtq-analysis
kubectl get svc -n lgbtq-analysis
```

3. **Cypress tests failing**
```bash
# Check service health
kubectl exec -it <pod-name> -n lgbtq-analysis -- wget -O- http://backend-service:8000/health
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Cypress Documentation](https://docs.cypress.io/)
- [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

---

## 🎯 Quick Start Commands

```bash
# Local development with Docker
docker-compose up -d

# Run E2E tests
docker-compose --profile test up

# Deploy to Kubernetes
kubectl apply -f k8s/

# Run Cypress in K8s
kubectl apply -f k8s/cypress-job.yaml

# Check application health
kubectl get pods -n lgbtq-analysis
```

---

**Built with ❤️ for LGBTQ+ community | SDG 3, 5, 10 Aligned | Privacy-First Design**
