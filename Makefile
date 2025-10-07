# Makefile for Code Review Automation Tool

.PHONY: help install install-dev test lint format type-check clean run-example

# Default target
help:
	@echo "Code Review Automation Tool - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install      Install package and dependencies"
	@echo "  install-dev  Install package in development mode with dev dependencies"
	@echo "  test         Run tests with pytest"
	@echo "  lint         Run linting with flake8"
	@echo "  format       Format code with black"
	@echo "  type-check   Run type checking with mypy"
	@echo "  clean        Clean build artifacts"
	@echo "  run-example  Run example analysis"
	@echo "  help         Show this help message"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements.txt

# Testing and Quality
test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ --max-line-length=88 --extend-ignore=E203,W503

format:
	black src/ tests/ --line-length=88

type-check:
	mypy src/ --ignore-missing-imports

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Examples
run-example:
	@echo "Running example analysis on this project..."
	python src/main.py --files src/main.py --format terminal --verbose

run-example-git:
	@echo "Running git diff analysis..."
	@if [ -d .git ]; then \
		python src/main.py --git-diff HEAD~1..HEAD --format markdown --output example_report.md; \
		echo "Report saved to example_report.md"; \
	else \
		echo "This is not a git repository. Initialize git first."; \
	fi

# Development helpers
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify installation"

check-all: format lint type-check test
	@echo "All checks passed!"