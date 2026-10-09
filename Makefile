.PHONY: help setup install lint test format clean docs-serve docs-build

# Shell environment configuration
SHELL := /bin/bash
PYTHON := python
PIP := pip
MKDOCS := mkdocs

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-R0-9_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Install editable package and development dependencies
	$(PIP) install -e ".[dev]"

install: ## Install core project dependencies only
	$(PIP) install -e .

lint: ## Run code formatting checks and linting
	ruff check src/ tests/
	black --check src/ tests/

format: ## Automatically format code using black and ruff
	ruff check --fix src/ tests/
	black src/ tests/

test: ## Run unit tests with pytest
	pytest --cov=src tests/

clean: ## Remove bytecode, build artifacts, and MkDocs site
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov site/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs-serve: ## Launch local MkDocs server with live-reloading on src/
	$(MKDOCS) serve --watch src

docs-build: ## Build static HTML documentation site
	$(MKDOCS) build