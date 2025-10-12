# 🏳️‍🌈 LGBTQ+ Sexual Fluidity Analysis Platform

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](docker-compose.yml)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?logo=kubernetes&logoColor=white)](k8s/)
[![Tests](https://img.shields.io/badge/Cypress-19%20E2E%20Tests-17202C?logo=cypress&logoColor=white)](cypress/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](backend/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](frontend/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi&logoColor=white)](backend/)

**A production-ready, privacy-first platform for LGBTQ+ sexual fluidity analysis**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🌟 Features

### 🔒 **Privacy-First Architecture**
- **Zero Data Persistence** - All analysis happens in-memory only
- **No Tracking** - Absolutely no analytics or third-party scripts
- **No PII Collection** - Complete anonymity guaranteed
- **Open Source** - Full transparency in code and data handling

### 🌐 **Inclusive Design**
- **Bilingual Support** - Full Thai/English language support
- **Accessibility** - WCAG AA compliant
- **SDG Aligned** - UN Goals 3, 5, 10 (Health, Gender Equality, Reduced Inequalities)
- **Mobile Responsive** - Works seamlessly on all devices

### 🚀 **Production-Ready Infrastructure**
- **Docker Containerized** - Easy deployment anywhere
- **Kubernetes Ready** - Horizontal auto-scaling included
- **CI/CD Pipeline** - Automated testing and deployment
- **Comprehensive Testing** - 19 E2E Cypress tests

### 📊 **Advanced Analysis**
- Statistical fluidity scoring
- Confidence intervals
- Pattern recognition
- Visual data representation

---

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** (recommended) OR
- **Python 3.12+** and **Node.js 20+** (for local development)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/pichitchaipae/lgbtq-fluidity-analyzer.git
cd lgbtq-fluidity-analyzer

# Start the application
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

That's it! 🎉

## 📚 Documentation

| Guide | Description |
|-------|-------------|
| **[📖 Documentation Index](docs/)** | Complete documentation catalog |
| **[🚀 Quick Start](docs/deployment/QUICK-START.md)** | Get started in 5 minutes |
| **[🐙 GitHub Upload](docs/github/UPLOAD-INSTRUCTIONS.txt)** | Push to GitHub guide |
| **[🐳 Docker & K8s](docs/deployment/DOCKER-K8S-SETUP.md)** | Container deployment |
| **[📦 Full Deployment](docs/deployment/DEPLOYMENT.md)** | Complete deployment guide |
| **[🤝 Contributing](CONTRIBUTING.md)** | How to contribute |
| **[🔒 Security](SECURITY.md)** | Security policy |

## Contents

- [🏳️‍🌈 LGBTQ+ Sexual Fluidity Analysis Platform](#️-lgbtq-sexual-fluidity-analysis-platform)
  - [🌟 Features](#-features)
    - [🔒 **Privacy-First Architecture**](#-privacy-first-architecture)
    - [🌐 **Inclusive Design**](#-inclusive-design)
    - [🚀 **Production-Ready Infrastructure**](#-production-ready-infrastructure)
    - [📊 **Advanced Analysis**](#-advanced-analysis)
  - [🚀 Quick Start](#-quick-start)
    - [Prerequisites](#prerequisites)
    - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [📚 Documentation](#-documentation)
  - [Contents](#contents)
  - [Architecture](#architecture)
    - [Backend Service](#backend-service)
    - [Frontend App](#frontend-app)
    - [Cypress E2E Testing](#cypress-e2e-testing)
    - [Docker \& Kubernetes](#docker--kubernetes)
    - [Dev Experience](#dev-experience)
  - [Local Development](#local-development)
    - [🚀 Quick Start (Docker Compose - Recommended)](#-quick-start-docker-compose---recommended)
    - [🎯 Interactive Deployment](#-interactive-deployment)
    - [📦 Manual Setup](#-manual-setup)
    - [Prerequisites](#prerequisites-1)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Testing](#testing)
  - [Deployment](#deployment)
  - [Customization](#customization)
  - [🆕 What's New in v2.0](#-whats-new-in-v20)
    - [Advanced Two-Way ANOVA Analysis](#advanced-two-way-anova-analysis)
    - [AI-Powered Insights (Optional)](#ai-powered-insights-optional)
    - [Dual Analysis Modes](#dual-analysis-modes)
  - [Ethics \& Privacy](#ethics--privacy)
  - [API Documentation](#api-documentation)
    - [POST /api/v2/analysis](#post-apiv2analysis)
  - [📧 Contact \& Support](#-contact--support)
    - [Get Help](#get-help)
    - [Maintainer](#maintainer)
    - [Security Issues](#security-issues)

## Architecture

```text
.
├── backend/                # FastAPI service
│   ├── app/
│   │   ├── api/            # HTTP routes
│   │   ├── core/           # Settings & config
│   │   ├── schemas/        # Pydantic models
│   │   └── services/       # Business logic (LGBTQAnalyzer)
│   ├── tests/              # Pytest test-suite
│   ├── Dockerfile          # Production container
│   └── requirements.txt
├── frontend/               # React + Vite + Tailwind application
│   ├── src/
│   │   ├── App.tsx         # Survey experience (Thai/English)
│   │   ├── api.ts          # REST client
│   │   └── __tests__/      # Vitest/RTL specs
│   ├── Dockerfile          # Nginx production container
│   ├── nginx.conf          # Nginx configuration
│   └── package.json
├── k8s/                    # Kubernetes manifests
│   ├── namespace.yaml      # Dedicated namespace
│   ├── configmap.yaml      # Environment configs
│   ├── backend-deployment.yaml    # 3-replica backend
│   ├── frontend-deployment.yaml   # 2-replica frontend
│   ├── hpa.yaml            # Horizontal autoscaling
│   ├── cypress-job.yaml    # E2E testing job
│   └── ingress.yaml        # NGINX ingress + TLS
├── cypress/                # E2E test suite
│   ├── e2e/
│   │   └── lgbtq-analysis.cy.js  # 19 automated tests
│   ├── support/            # Custom commands
│   └── cypress.config.js
├── scripts/                # Automation scripts
│   ├── deploy.ps1          # Windows deployment script
│   ├── deploy-production.sh # Linux/Mac deployment
│   ├── fix-ci.ps1          # CI maintenance tool
│   └── test-docker.sh      # Docker testing
├── .github/workflows/ci.yml   # CI/CD pipeline
├── docker-compose.yml      # Local development
└── README.md
```

### Backend Service

- **Framework**: FastAPI + Uvicorn (4 workers in production)
- **Logic**: `LGBTQAnalyzer` encapsulates weighted scoring, interpretation, and insight generation.
- **Schemas**: Pydantic models handle request validation and rich responses.
- **API Surface**:
  - `GET /health` – readiness probe (Kubernetes health checks)
  - `POST /api/v1/analysis` – accepts 12 integer responses (0-4) and returns aggregate scoring with insights
- **Testing**: Pytest unit + API integration coverage.
- **Container**: Multi-stage Python 3.12 image with non-root user and health checks.
- **Scaling**: 3-10 replicas via HPA (70% CPU threshold).

### Frontend App

- **Stack**: React 18, TypeScript, Vite, TailwindCSS, React Query.
- **Languages**: Full Thai/English bilingual support (toggle in header).
- **UX**: Accessible form, colorful gradient layout, live validation, result visualization with emojis.
- **Data Flow**: Declarative mutation orchestrated via React Query calling the FastAPI endpoint.
- **Testing**: Vitest + Testing Library + Cypress E2E (19 automated tests).
- **Container**: Multi-stage build (Node → Nginx) with gzip, security headers, health checks.
- **Scaling**: 2-5 replicas via HPA (75% CPU threshold).

### Cypress E2E Testing

- **Coverage**: 19 comprehensive tests covering:
  - Language toggle (Thai ⇄ English)
  - Survey form interaction (all 6 question groups)
  - Results display and translation
  - API integration
  - Responsive design (mobile/tablet/desktop)
- **Execution**: Docker container or Kubernetes Job
- **Artifacts**: Video recordings and screenshots on failure
- **CI/CD**: Automated in GitHub Actions pipeline

### Docker & Kubernetes

- **Orchestration**: Kubernetes with namespaces, ConfigMaps, HPA, Ingress
- **Networking**: ClusterIP (backend) + LoadBalancer (frontend)
- **Security**: Non-root containers, resource limits, network policies
- **Privacy**: No persistent volumes (in-memory processing only)
- **Monitoring**: Health checks, readiness/liveness probes
- **Scaling**: Automatic based on CPU/memory metrics

### Dev Experience

- `.editorconfig` and Prettier-compatible ESLint configuration.
- Optional pre-commit hooks for formatting and linting (`.pre-commit-config.yaml`).
- Renovate-ready dependency definitions (configure in your org if desired).

## Local Development

### 🚀 Quick Start (Docker Compose - Recommended)

```bash
# Start all services
docker-compose up -d

# Access:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs

# Run with Cypress tests
docker-compose --profile test up

# Stop services
docker-compose down
```

### 🎯 Interactive Deployment

```powershell
# Run interactive deployment script (Windows)
.\scripts\deploy.ps1

# Or for Linux/Mac
./scripts/deploy-production.sh

# Choose from:
# 1. Docker Compose (Local Development)
# 2. Docker Compose with Cypress Tests
# 3. Kubernetes Deployment
# 4. Kubernetes with Cypress Tests
# 5. Build Docker Images Only
# 6. Install Cypress Locally
```

### 📦 Manual Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- npm or pnpm

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables can be defined via `.env` (see `.env.example`).

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` in `.env` (default assumes `http://localhost:8000/api/v1`).

## Testing

- **Backend**: `cd backend && pytest`
- **Frontend**: `cd frontend && npm test`
- GitHub Actions (`.github/workflows/ci.yml`) runs both suites, lints, and builds Docker images.

## Deployment

- Build backend container: `docker build -t lgbtq-analyzer-api backend`
- Deploy to any container platform (Azure App Service, AWS ECS, GCP Cloud Run, etc.)
- Frontend `npm run build` generates static assets deployable on Netlify, Vercel, Azure Static Web Apps, or S3 + CloudFront.
- Adjust workflow secrets (`REGISTRY_USERNAME`, `REGISTRY_PASSWORD`, `REGISTRY_URL`, etc.) before enabling image publishing.

## Customization

- Update weights and interpretation ranges in `backend/app/services/analyzer.py`.
- Extend request/response schemas in `backend/app/schemas/analysis.py`.
- Add new questions by modifying `questionGroups` in `frontend/src/App.tsx` and backend schema definitions.
- Tailwind theme colors are in `frontend/tailwind.config.js`.

## 🆕 What's New in v2.0

### Advanced Two-Way ANOVA Analysis
- Analyze interaction effects between Media and Social factors
- Understand how factors combine to influence identity exploration

### AI-Powered Insights (Optional)
- Get plain-language explanations of statistical results
- Bilingual support (Thai/English)
- Privacy-preserved: only aggregated statistics are shared

### Dual Analysis Modes
- 🔒 **Local Mode**: 100% private, browser-only calculation
- 🤖 **AI Mode**: Enhanced insights with anonymous statistics

## Ethics & Privacy

**v2.0 maintains our zero-data-collection policy:**
- Local mode: No data leaves your device
- AI mode: Only statistical summaries (F-values, p-values) sent
- No individual responses stored or transmitted
- No user identification possible

- No personally identifiable information is collected or persisted.
- All computations rely on in-memory data supplied per request.
- Output is suited for educational and research purposes only; it is **not** a clinical diagnosis.

## API Documentation

### POST /api/v2/analysis

**Request:**
```
{
  "dataset": [
    {
      "media1": 3,
      "media2": 2,
      // ... other questions
    }
  ],
  "options": {
    "ai_insights": true,
    "language": "th"
  }
}
```

**Response:**
```
{
  "anova_results": {
    "media_effect": {...},
    "social_effect": {...},
    "interaction_effect": {...}
  },
  "visualizations": {
    "interaction_plot": "base64...",
    "group_means": [...]
  },
  "ai_interpretation": {
    "th": "คำอธิบายภาษาไทย...",
    "en": "English explanation..."
  }
}
```

---

## 📧 Contact & Support

### Get Help

- 💬 **Discussions**: [GitHub Discussions](https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/discussions) - Ask questions, share ideas
- 🐛 **Issues**: [Report bugs or request features](https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/issues)
- 📖 **Documentation**: [Full documentation](docs/README.md)

### Maintainer

- **Email**: [jao.pichitchai@gmail.com](mailto:jao.pichitchai@gmail.com)
- **GitHub**: [@pichitchaipae](https://github.com/pichitchaipae)

### Security Issues

For security vulnerabilities, please email [jao.pichitchai@gmail.com](mailto:jao.pichitchai@gmail.com) directly or see our [Security Policy](SECURITY.md).

---

> "การยอมรับความแตกต่างคือจุดเริ่มต้นของสังคมที่เท่าเทียม"

<!-- Configuration complete - 2025-10-12 02:30:45 -->
