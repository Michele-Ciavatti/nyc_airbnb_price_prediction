.PHONY: help setup install data lint test format clean docs-serve docs-build

# Shell environment configuration
PYTHON := python
PIP := pip
MKDOCS := mkdocs

help: ## Show this help message
	@$(PYTHON) scripts/make_help.py

setup: ## Install editable package and development dependencies
	$(PIP) install -e ".[dev]"
	pre-commit install

install: ## Install core project dependencies only
	$(PIP) install -e .

data: ## Download the dataset from Kaggle
	$(PYTHON) src/retrieve_data.py

lint: ## Run code formatting checks and linting
	ruff check src/ tests/ scripts/ notebooks/
	ruff format --check src/ tests/ scripts/ notebooks/

format: ## Automatically format code using ruff
	ruff check --fix src/ tests/ scripts/ notebooks/
	ruff format src/ tests/ scripts/ notebooks/

test: ## Run unit tests with pytest
	pytest --cov=src tests/

clean: ## Remove bytecode, build artifacts, and MkDocs site
	$(PYTHON) scripts/clean.py

docs-serve: ## Launch local MkDocs server with live-reloading on src/
	$(MKDOCS) serve --watch src

docs-build: ## Build static HTML documentation site
	$(MKDOCS) build
