# LGBTQ+ Sexual Fluidity Analysis Tool - Production Makefile
# ============================================================

.PHONY: help install test build up down clean logs deploy k8s-deploy k8s-delete

# Default target
.DEFAULT_GOAL := help

# Variables
COMPOSE_FILE := docker-compose.yml
BACKEND_IMAGE := lgbtq-backend
FRONTEND_IMAGE := lgbtq-frontend
VERSION := $(shell git describe --tags --always --dirty)
REGISTRY := # Set your container registry here (e.g., docker.io/username)

## help: Show this help message
help:
	@echo "LGBTQ+ Analysis Tool - Production Commands"
	@echo "==========================================="
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev-backend   - Run backend in development mode"
	@echo "  make dev-frontend  - Run frontend in development mode"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run all tests"
	@echo "  make test-backend  - Run backend tests only"
	@echo "  make test-frontend - Run frontend tests only"
	@echo "  make test-e2e      - Run Cypress E2E tests"
	@echo ""
	@echo "Docker:"
	@echo "  make build         - Build Docker images"
	@echo "  make up            - Start services with docker-compose"
	@echo "  make down          - Stop services"
	@echo "  make restart       - Restart all services"
	@echo "  make logs          - Show service logs"
	@echo "  make ps            - Show running containers"
	@echo ""
	@echo "Kubernetes:"
	@echo "  make k8s-deploy    - Deploy to Kubernetes"
	@echo "  make k8s-delete    - Delete from Kubernetes"
	@echo "  make k8s-status    - Show K8s deployment status"
	@echo "  make k8s-logs      - Show K8s pod logs"
	@echo ""
	@echo "Production:"
	@echo "  make prod-build    - Build production images"
	@echo "  make prod-push     - Push images to registry"
	@echo "  make prod-deploy   - Full production deployment"
	@echo ""
	@echo "CI/CD Maintenance:"
	@echo "  make fix-eslint-env     - Patch Node.js globals in .cjs files"
	@echo "  make sync-frontend-lock - Sync package-lock.json"
	@echo "  make frontend-ci-check  - Validate CI install (dry-run)"
	@echo "  make audit-fix          - Auto-fix npm audit issues"
	@echo "  make ci-fix-all         - Run all CI fixes (one-shot)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Remove containers and volumes"
	@echo "  make clean-all     - Remove everything including images"

## install: Install all dependencies
install:
	@echo "📦 Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm ci
	@echo "✅ Dependencies installed!"

## dev-backend: Run backend in development mode
dev-backend:
	@echo "🚀 Starting backend development server..."
	cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## dev-frontend: Run frontend in development mode
dev-frontend:
	@echo "🚀 Starting frontend development server..."
	cd frontend && npm run dev

## test: Run all tests
test: test-backend test-frontend
	@echo "✅ All tests passed!"

## test-backend: Run backend tests
test-backend:
	@echo "🧪 Running backend tests..."
	cd backend && pytest tests/ -v --tb=short
	@echo "✅ Backend tests passed!"

## test-frontend: Run frontend tests
test-frontend:
	@echo "🧪 Running frontend tests..."
	cd frontend && npm run test -- --run
	@echo "✅ Frontend tests passed!"

## test-e2e: Run Cypress E2E tests
test-e2e:
	@echo "🧪 Running E2E tests with docker-compose..."
	docker-compose --profile test up --abort-on-container-exit cypress
	@echo "✅ E2E tests completed!"

## build: Build Docker images
build:
	@echo "🔨 Building Docker images..."
	docker-compose build
	@echo "✅ Images built successfully!"

## up: Start services with docker-compose
up:
	@echo "🚀 Starting services..."
	docker-compose up -d
	@echo "⏳ Waiting for health checks..."
	@sleep 10
	@echo "✅ Services started!"
	@echo "🌐 Frontend: http://localhost:3000"
	@echo "🔧 Backend: http://localhost:8000"
	@echo "📊 API Docs: http://localhost:8000/docs"

## down: Stop services
down:
	@echo "🛑 Stopping services..."
	docker-compose down
	@echo "✅ Services stopped!"

## restart: Restart all services
restart: down up

## logs: Show service logs
logs:
	docker-compose logs -f

## ps: Show running containers
ps:
	docker-compose ps

## clean: Remove containers and volumes
clean:
	@echo "🧹 Cleaning up containers and volumes..."
	docker-compose down -v
	@echo "✅ Cleanup complete!"

## clean-all: Remove everything including images
clean-all: clean
	@echo "🧹 Removing Docker images..."
	docker rmi $(BACKEND_IMAGE):latest $(FRONTEND_IMAGE):latest 2>/dev/null || true
	@echo "✅ Full cleanup complete!"

## prod-build: Build production images with version tags
prod-build:
	@echo "🔨 Building production images (version: $(VERSION))..."
	docker build -t $(BACKEND_IMAGE):$(VERSION) -t $(BACKEND_IMAGE):latest ./backend
	docker build -t $(FRONTEND_IMAGE):$(VERSION) -t $(FRONTEND_IMAGE):latest ./frontend
	@echo "✅ Production images built!"

## prod-push: Push images to registry
prod-push:
	@if [ -z "$(REGISTRY)" ]; then \
		echo "❌ Error: REGISTRY variable not set!"; \
		echo "   Set it in Makefile or run: make prod-push REGISTRY=your-registry"; \
		exit 1; \
	fi
	@echo "📤 Pushing images to $(REGISTRY)..."
	docker tag $(BACKEND_IMAGE):$(VERSION) $(REGISTRY)/$(BACKEND_IMAGE):$(VERSION)
	docker tag $(BACKEND_IMAGE):latest $(REGISTRY)/$(BACKEND_IMAGE):latest
	docker tag $(FRONTEND_IMAGE):$(VERSION) $(REGISTRY)/$(FRONTEND_IMAGE):$(VERSION)
	docker tag $(FRONTEND_IMAGE):latest $(REGISTRY)/$(FRONTEND_IMAGE):latest
	docker push $(REGISTRY)/$(BACKEND_IMAGE):$(VERSION)
	docker push $(REGISTRY)/$(BACKEND_IMAGE):latest
	docker push $(REGISTRY)/$(FRONTEND_IMAGE):$(VERSION)
	docker push $(REGISTRY)/$(FRONTEND_IMAGE):latest
	@echo "✅ Images pushed to registry!"

## k8s-deploy: Deploy to Kubernetes
k8s-deploy:
	@echo "☸️  Deploying to Kubernetes..."
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/configmap.yaml
	@echo "⚠️  Creating secrets (you may need to update with real values)..."
	kubectl create secret generic ai-api-keys -n lgbtq-analysis \
		--from-literal=GEMINI_API_KEY=${GEMINI_API_KEY} \
		--from-literal=OPENAI_API_KEY=${OPENAI_API_KEY:-""} \
		--dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -f k8s/backend-deployment.yaml
	kubectl apply -f k8s/frontend-deployment.yaml
	kubectl apply -f k8s/ingress.yaml
	kubectl apply -f k8s/hpa.yaml
	@echo "⏳ Waiting for deployments..."
	kubectl wait --for=condition=available --timeout=300s deployment/backend-deployment -n lgbtq-analysis
	kubectl wait --for=condition=available --timeout=300s deployment/frontend-deployment -n lgbtq-analysis
	@echo "✅ Deployed to Kubernetes!"

## k8s-delete: Delete from Kubernetes
k8s-delete:
	@echo "🗑️  Deleting Kubernetes resources..."
	kubectl delete -f k8s/ --ignore-not-found=true
	@echo "✅ Resources deleted!"

## k8s-status: Show Kubernetes deployment status
k8s-status:
	@echo "☸️  Kubernetes Status:"
	@echo "===================="
	kubectl get all -n lgbtq-analysis
	@echo ""
	@echo "📊 Pod Status:"
	kubectl get pods -n lgbtq-analysis -o wide

## k8s-logs: Show Kubernetes pod logs
k8s-logs:
	@echo "📝 Recent logs from backend:"
	kubectl logs -n lgbtq-analysis -l app=lgbtq-backend --tail=50
	@echo ""
	@echo "📝 Recent logs from frontend:"
	kubectl logs -n lgbtq-analysis -l app=lgbtq-frontend --tail=50

## prod-deploy: Full production deployment (build, test, push, deploy)
prod-deploy: test prod-build prod-push k8s-deploy
	@echo "🎉 Production deployment complete!"
	@echo "🌐 Check your ingress URL for the application"

# ============================================================
# CI/CD Maintenance Commands
# ============================================================

FRONTEND := frontend
CJS_FILES := $(FRONTEND)/.eslintrc.cjs $(FRONTEND)/postcss.config.cjs $(FRONTEND)/tailwind.config.cjs

## fix-eslint-env: Patch Node.js globals in config .cjs files
fix-eslint-env:
	@echo "🔧 Patching ESLint environment in .cjs files..."
	@node -e "const fs=require('fs'); const files=process.argv.slice(1); files.forEach(f=>{ if(fs.existsSync(f)){ const s=fs.readFileSync(f,'utf8'); if(!s.startsWith('/* eslint-env node */')){ fs.writeFileSync(f, '/* eslint-env node */\\n'+s); console.log('✓ Patched', f); } else { console.log('✓ OK', f); } } else { console.log('⚠ Missing', f); }});" $(CJS_FILES)
	@git add $(CJS_FILES) || true

## sync-frontend-lock: Sync lockfile so npm ci passes in CI
sync-frontend-lock:
	@echo "🔄 Syncing frontend lockfile..."
	cd $(FRONTEND) && npm install
	git add $(FRONTEND)/package-lock.json
	@echo "✓ Lockfile synced"

## frontend-ci-check: Validate CI install locally without changing files
frontend-ci-check:
	@echo "🧪 Validating CI install (dry-run)..."
	cd $(FRONTEND) && npm ci --dry-run
	@echo "✓ CI validation passed"

## audit-fix: Try to auto-remediate npm audit issues
audit-fix:
	@echo "🔒 Attempting to fix npm audit issues..."
	cd $(FRONTEND) && npm audit fix || true
	@echo "✓ Audit fix completed"

## ci-fix-all: One-shot fixer for common CI failures
ci-fix-all: fix-eslint-env sync-frontend-lock frontend-ci-check audit-fix
	@echo "🎉 All CI fixes applied!"
	@echo "💡 Review changes with: git status"
	@echo "💡 Commit with: git commit -m 'chore: fix CI issues'"
