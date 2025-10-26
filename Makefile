.PHONY: help install test coverage lint format typecheck clean all

help:
	@echo "Jarvis AI Assistant - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install dependencies"
	@echo "  make setup        Run full setup script"
	@echo ""
	@echo "Testing:"
	@echo "  make test         Run all tests"
	@echo "  make coverage     Run tests with coverage report"
	@echo "  make test-unit    Run unit tests only"
	@echo "  make test-int     Run integration tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         Run all linters"
	@echo "  make format       Format code with black and isort"
	@echo "  make typecheck    Run mypy type checking"
	@echo "  make check        Run all checks (lint + typecheck + test)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        Remove generated files"
	@echo ""
	@echo "All:"
	@echo "  make all          Format, lint, typecheck, and test"

install:
	pip install -r requirements-dev.txt

setup:
	bash scripts/setup.sh

test:
	pytest -v

coverage:
	pytest --cov=jarvis --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-unit:
	pytest tests/test_jarvis_unit.py -v

test-int:
	pytest tests/test_jarvis_integration.py -v

lint:
	@echo "Running ruff..."
	ruff check .
	@echo "Checking black formatting..."
	black --check .
	@echo "Checking isort..."
	isort --check-only .

format:
	@echo "Formatting with black..."
	black .
	@echo "Sorting imports with isort..."
	isort .
	@echo "Fixing linting issues..."
	ruff check --fix .

typecheck:
	mypy jarvis.py

check: lint typecheck test
	@echo "All checks passed! ✅"

clean:
	@echo "Cleaning up..."
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"

all: format lint typecheck test
	@echo "All tasks completed successfully! 🎉"
