#!/usr/bin/env bash
# ============================================================
# Local Testing with Docker Compose
# ============================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo ""
log_info "🧪 Testing with Docker Compose"
log_info "=============================="
echo ""

# Check if .env exists
if [ ! -f "./backend/.env" ]; then
    log_warning ".env file not found in backend/"
    echo "Creating from template..."
    cat > ./backend/.env <<EOF
GEMINI_API_KEY=${GEMINI_API_KEY:-your_api_key_here}
OPENAI_API_KEY=${OPENAI_API_KEY:-}
ENVIRONMENT=production
LOG_LEVEL=info
AI_PROVIDER=gemini
EOF
    log_info "Please update backend/.env with your API keys"
    exit 1
fi

# Build images
log_info "Building Docker images..."
docker-compose build

# Start services
log_info "Starting services..."
docker-compose up -d

# Wait for health checks
log_info "Waiting for services to be healthy..."
sleep 15

# Check service status
log_info "Checking service status..."
docker-compose ps

# Show logs
log_info "Recent logs:"
docker-compose logs --tail=20

echo ""
log_success "Services are running!"
echo ""
log_info "Access points:"
echo "  🌐 Frontend: http://localhost:3000"
echo "  🔧 Backend: http://localhost:8000"
echo "  📊 API Docs: http://localhost:8000/docs"
echo ""
log_info "Commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop: docker-compose down"
echo "  Restart: docker-compose restart"
echo ""
