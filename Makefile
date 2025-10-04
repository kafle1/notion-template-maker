# Makefile for Notion Template Maker
# FastAPI + React application for generating customized Notion templates using AI

.PHONY: help install install-backend install-frontend dev dev-backend dev-frontend build clean docker-up docker-down

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m

help: ## Show this help message
	@echo "$(BLUE)Notion Template Maker - Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Quick Start:$(NC)"
	@echo "  make install    - Install all dependencies"
	@echo "  make dev        - Run full application (backend + frontend)"
	@echo ""
	@echo "$(YELLOW)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-18s$(NC) %s\n", $$1, $$2}'

install: install-backend install-frontend ## Install all dependencies (backend + frontend)
	@echo "$(GREEN)✓ All dependencies installed$(NC)"

install-backend: ## Install Python backend dependencies
	@echo "$(BLUE)Installing backend dependencies...$(NC)"
	pip install --upgrade pip
	pip install -r requirements-backend.txt
	@echo "$(GREEN)✓ Backend dependencies installed$(NC)"

install-frontend: ## Install Node.js frontend dependencies
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	cd frontend && npm install
	@echo "$(GREEN)✓ Frontend dependencies installed$(NC)"

dev: ## Run full stack application (backend + frontend)
	@echo "$(GREEN)🚀 Starting Notion Template Maker...$(NC)"
	@echo "$(BLUE)Backend: http://localhost:8000$(NC)"
	@echo "$(BLUE)Frontend: http://localhost:5173$(NC)"
	@echo "$(BLUE)API Docs: http://localhost:8000/api/docs$(NC)"
	@echo ""
	@trap 'kill 0' EXIT; \
	(cd backend && python main.py) & \
	(cd frontend && npm run dev)

dev-backend: ## Run only backend server
	@echo "$(BLUE)Starting backend server...$(NC)"
	cd backend && python main.py

dev-frontend: ## Run only frontend development server
	@echo "$(BLUE)Starting frontend dev server...$(NC)"
	cd frontend && npm run dev

build: ## Build frontend for production
	@echo "$(BLUE)Building frontend...$(NC)"
	cd frontend && npm run build
	@echo "$(GREEN)✓ Build complete - output in frontend/dist$(NC)"

lint: ## Run code linters
	@echo "$(BLUE)Running linters...$(NC)"
	black src/ backend/ --check
	flake8 src/ backend/ --max-line-length=88
	cd frontend && npm run lint
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format code
	@echo "$(BLUE)Formatting code...$(NC)"
	black src/ backend/
	cd frontend && npm run format || true
	@echo "$(GREEN)✓ Code formatted$(NC)"

check: lint ## Run linting checks
	@echo "$(GREEN)✓ All checks passed$(NC)"

clean: ## Clean build artifacts and cache
	@echo "$(RED)Cleaning build artifacts...$(NC)"
	rm -rf __pycache__
	rm -rf backend/__pycache__ backend/*/__pycache__ backend/*/*/__pycache__
	rm -rf frontend/dist frontend/node_modules/.cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

docker-build: ## Build Docker containers
	@echo "$(BLUE)Building Docker containers...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Docker build complete$(NC)"

docker-up: ## Start application with Docker
	@echo "$(GREEN)🚀 Starting with Docker...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Application running at http://localhost:5173$(NC)"

docker-down: ## Stop Docker containers
	@echo "$(RED)Stopping Docker containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Containers stopped$(NC)"

docker-logs: ## View Docker logs
	docker-compose logs -f

production: build ## Prepare for production deployment
	@echo "$(BLUE)Preparing production build...$(NC)"
	@echo "$(GREEN)✓ Ready for deployment$(NC)"
	@echo "$(YELLOW)Deploy backend: cd backend && uvicorn main:app --host 0.0.0.0 --port 8000$(NC)"
	@echo "$(YELLOW)Deploy frontend: Serve frontend/dist with nginx or static hosting$(NC)"

setup: install ## Initial setup for new developers
	@echo "$(GREEN)🎉 Setup complete! Run 'make dev' to start$(NC)"

all: clean install build ## Clean, install, and build everything
	@echo "$(GREEN)✓ Full build pipeline complete$(NC)"
	@echo "Notion Template Maker"
	@echo "===================="
	@echo "A beautiful, simple app for generating customized Notion templates using AI."
	@echo ""
	@echo "Project Structure:"
	@echo "  backend/            - FastAPI backend"
	@echo "    ├── api/          - API routes"
	@echo "    ├── models/       - Data models"
	@echo "    ├── services/     - Business logic"
	@echo "    └── clients/      - External API clients"
	@echo "  frontend/           - React frontend"
	@echo "    ├── components/   - UI components"
	@echo "    ├── pages/        - Page components"
	@echo "    └── services/     - API client & state"
	@echo ""
	@echo "Quick start: make dev"
