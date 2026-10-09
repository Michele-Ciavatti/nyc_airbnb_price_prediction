.PHONY: help setup install lint test format clean docs-serve docs-build

# Shell environment configuration
PYTHON := python
PIP := pip
MKDOCS := mkdocs

help: ## Show this help message
	@$(PYTHON) scripts/make_help.py

setup: ## Install editable package and development dependencies
	$(PIP) install -e ".[dev]"

install: ## Install core project dependencies only
	$(PIP) install -e .

data: ## Download the dataset from Kaggle
	$(PYTHON) src/retrieve_data.py

lint: ## Run code formatting checks and linting
	ruff check src/ tests/
	black --check src/ tests/

format: ## Automatically format code using black and ruff
	ruff check --fix src/ tests/ scripts/
	black src/ tests/ scripts/

test: ## Run unit tests with pytest
	pytest --cov=src tests/

clean: ## Remove bytecode, build artifacts, and MkDocs site
	$(PYTHON) scripts/clean.py

docs-serve: ## Launch local MkDocs server with live-reloading on src/
	$(MKDOCS) serve --watch src

docs-build: ## Build static HTML documentation site
	$(MKDOCS) build