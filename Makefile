# Makefile for Notion Template Maker
# A Streamlit application for generating customized Notion templates using AI

.PHONY: help install run test lint format clean all dev setup

# Default target
help:
	@echo "Notion Template Maker - Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make install    - Install Python dependencies"
	@echo "  make run        - Run the Streamlit application"
	@echo "  make dev        - Install dependencies and run the app"
	@echo "  make setup      - Complete setup (install + format)"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test       - Run all tests"
	@echo "  make test-unit  - Run unit tests only"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code with black"
	@echo "  make check      - Run linting and tests"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean      - Clean up cache files"
	@echo "  make all        - Install, format, test, and run"
	@echo ""
	@echo "Quick start: make dev"

# Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

# Run the Streamlit application
run:
	@echo "Starting Notion Template Maker..."
	streamlit run app.py

# Development setup (install + run)
dev: install run

# Complete setup (install + format)
setup: install format

# Run all tests
test:
	@echo "Running all tests..."
	pytest tests/ -v

# Run unit tests only
test-unit:
	@echo "Running unit tests..."
	pytest tests/unit/ -v

# Run linting checks
lint:
	@echo "Running linting checks..."
	flake8 src/ tests/ app.py
	@echo "Linting complete!"

# Format code with black
format:
	@echo "Formatting code with black..."
	black src/ tests/ app.py
	@echo "Code formatting complete!"

# Run both linting and tests
check: lint test

# Clean up cache files
clean:
	@echo "Cleaning up cache files..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "Cleanup complete!"

# Install, format, test, and run
all: install format test run

# Create requirements.txt if it doesn't exist
requirements.txt:
	@echo "Creating requirements.txt..."
	@echo "# Notion Template Maker Dependencies" > requirements.txt
	@echo "streamlit>=1.28.0" >> requirements.txt
	@echo "requests>=2.31.0" >> requirements.txt
	@echo "python-dotenv>=1.0.0" >> requirements.txt
	@echo "cryptography>=41.0.0" >> requirements.txt
	@echo "pydantic>=2.0.0" >> requirements.txt
	@echo "jinja2>=3.1.0" >> requirements.txt
	@echo "pytest>=7.4.0" >> requirements.txt
	@echo "black>=23.0.0" >> requirements.txt
	@echo "flake8>=6.0.0" >> requirements.txt
	@echo "pytest-mock>=3.10.0" >> requirements.txt
	@echo "pytest-asyncio>=0.21.0" >> requirements.txt
	@echo "requirements.txt created!"

# Show project info
info:
	@echo "Notion Template Maker"
	@echo "===================="
	@echo "A beautiful, simple app for generating customized Notion templates using AI."
	@echo ""
	@echo "Project Structure:"
	@echo "  app.py              - Main Streamlit application"
	@echo "  src/                - Source code"
	@echo "    ├── models/       - Data models"
	@echo "    ├── services/     - Business logic"
	@echo "    ├── api/          - API clients"
	@echo "    └── ui/           - UI components"
	@echo "  tests/              - Test suite"
	@echo "  specs/              - Documentation and specs"
	@echo ""
	@echo "Quick start: make dev"
