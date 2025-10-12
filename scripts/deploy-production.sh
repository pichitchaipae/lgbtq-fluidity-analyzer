#!/usr/bin/env bash
# ============================================================
# Production Deployment Script
# ============================================================
# This script automates the complete production deployment
# process including testing, building, and deploying to K8s
# ============================================================

set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGISTRY="${DOCKER_REGISTRY:-}"
VERSION="${VERSION:-$(git describe --tags --always --dirty)}"
BACKEND_IMAGE="lgbtq-backend"
FRONTEND_IMAGE="lgbtq-frontend"
NAMESPACE="lgbtq-analysis"

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing=()
    
    command -v docker >/dev/null 2>&1 || missing+=("docker")
    command -v docker-compose >/dev/null 2>&1 || missing+=("docker-compose")
    command -v kubectl >/dev/null 2>&1 || missing+=("kubectl")
    command -v git >/dev/null 2>&1 || missing+=("git")
    
    if [ ${#missing[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing[*]}"
        exit 1
    fi
    
    log_success "All prerequisites installed"
}

check_env_vars() {
    log_info "Checking environment variables..."
    
    if [ -z "${GEMINI_API_KEY:-}" ]; then
        log_error "GEMINI_API_KEY is not set!"
        echo "Please export GEMINI_API_KEY before deploying"
        exit 1
    fi
    
    if [ -z "$REGISTRY" ]; then
        log_warning "DOCKER_REGISTRY not set. Images won't be pushed to remote registry."
        log_info "To push to a registry, set: export DOCKER_REGISTRY=your-registry"
    fi
    
    log_success "Environment variables OK"
}

run_tests() {
    log_info "Running test suite..."
    
    # Backend tests
    log_info "Running backend tests..."
    cd backend
    python -m pytest tests/ -v --tb=short || {
        log_error "Backend tests failed!"
        exit 1
    }
    cd ..
    log_success "Backend tests passed"
    
    # Frontend tests
    log_info "Running frontend tests..."
    cd frontend
    npm run test -- --run || {
        log_error "Frontend tests failed!"
        exit 1
    }
    cd ..
    log_success "Frontend tests passed"
    
    log_success "All tests passed!"
}

build_images() {
    log_info "Building Docker images (version: $VERSION)..."
    
    # Build backend
    log_info "Building backend image..."
    docker build -t ${BACKEND_IMAGE}:${VERSION} -t ${BACKEND_IMAGE}:latest ./backend
    
    # Build frontend
    log_info "Building frontend image..."
    docker build -t ${FRONTEND_IMAGE}:${VERSION} -t ${FRONTEND_IMAGE}:latest ./frontend
    
    log_success "Images built successfully!"
}

push_images() {
    if [ -z "$REGISTRY" ]; then
        log_warning "Skipping image push (no registry configured)"
        return 0
    fi
    
    log_info "Pushing images to $REGISTRY..."
    
    # Tag and push backend
    docker tag ${BACKEND_IMAGE}:${VERSION} ${REGISTRY}/${BACKEND_IMAGE}:${VERSION}
    docker tag ${BACKEND_IMAGE}:latest ${REGISTRY}/${BACKEND_IMAGE}:latest
    docker push ${REGISTRY}/${BACKEND_IMAGE}:${VERSION}
    docker push ${REGISTRY}/${BACKEND_IMAGE}:latest
    
    # Tag and push frontend
    docker tag ${FRONTEND_IMAGE}:${VERSION} ${REGISTRY}/${FRONTEND_IMAGE}:${VERSION}
    docker tag ${FRONTEND_IMAGE}:latest ${REGISTRY}/${FRONTEND_IMAGE}:latest
    docker push ${REGISTRY}/${FRONTEND_IMAGE}:${VERSION}
    docker push ${REGISTRY}/${FRONTEND_IMAGE}:latest
    
    log_success "Images pushed to registry!"
}

deploy_to_kubernetes() {
    log_info "Deploying to Kubernetes..."
    
    # Create namespace
    log_info "Creating namespace..."
    kubectl apply -f k8s/namespace.yaml
    
    # Create ConfigMap
    log_info "Creating ConfigMap..."
    kubectl apply -f k8s/configmap.yaml
    
    # Create secrets
    log_info "Creating secrets..."
    kubectl create secret generic ai-api-keys -n ${NAMESPACE} \
        --from-literal=GEMINI_API_KEY=${GEMINI_API_KEY} \
        --from-literal=OPENAI_API_KEY=${OPENAI_API_KEY:-""} \
        --dry-run=client -o yaml | kubectl apply -f -
    
    # Deploy backend
    log_info "Deploying backend..."
    kubectl apply -f k8s/backend-deployment.yaml
    
    # Deploy frontend
    log_info "Deploying frontend..."
    kubectl apply -f k8s/frontend-deployment.yaml
    
    # Apply ingress
    log_info "Applying ingress..."
    kubectl apply -f k8s/ingress.yaml
    
    # Apply HPA
    log_info "Applying horizontal pod autoscaler..."
    kubectl apply -f k8s/hpa.yaml
    
    # Wait for deployments
    log_info "Waiting for deployments to be ready..."
    kubectl wait --for=condition=available --timeout=300s \
        deployment/backend-deployment -n ${NAMESPACE}
    kubectl wait --for=condition=available --timeout=300s \
        deployment/frontend-deployment -n ${NAMESPACE}
    
    log_success "Deployed to Kubernetes!"
}

show_status() {
    log_info "Deployment Status:"
    echo ""
    kubectl get all -n ${NAMESPACE}
    echo ""
    log_info "Pod Details:"
    kubectl get pods -n ${NAMESPACE} -o wide
    echo ""
    log_info "Ingress:"
    kubectl get ingress -n ${NAMESPACE}
}

# Main execution
main() {
    echo ""
    log_info "🚀 LGBTQ+ Analysis Tool - Production Deployment"
    log_info "================================================"
    echo ""
    
    check_prerequisites
    check_env_vars
    
    log_info "Version: $VERSION"
    log_info "Registry: ${REGISTRY:-none (local only)}"
    log_info "Namespace: $NAMESPACE"
    echo ""
    
    read -p "Continue with deployment? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Deployment cancelled"
        exit 0
    fi
    
    run_tests
    build_images
    push_images
    deploy_to_kubernetes
    show_status
    
    echo ""
    log_success "🎉 Production deployment complete!"
    echo ""
    log_info "Next steps:"
    echo "  1. Check ingress URL for external access"
    echo "  2. Monitor logs: kubectl logs -f -n ${NAMESPACE} -l app=lgbtq-backend"
    echo "  3. Check metrics: kubectl top pods -n ${NAMESPACE}"
    echo ""
}

# Run main function
main "$@"
