"""Project tasks. Run `invoke --list` to see them all."""

"""Project tasks. Run `invoke --list` to see them all."""

import shutil
import sys
from pathlib import Path

from invoke.context import Context
from invoke.tasks import task

PYTHON = sys.executable  # same interpreter that runs invoke, no pip/python mismatch
CODE_PATHS = "src/ tests/ notebooks/ tasks.py"
MYPY_PATHS = "src/ tests/ tasks.py"


@task
def setup(c: Context) -> None:
    """Install editable package and development dependencies."""
    c.run(f"{PYTHON} -m pip install -e .[dev]")
    c.run("pre-commit install --install-hooks")


@task
def install(c: Context) -> None:
    """Install core project dependencies only."""
    c.run(f"{PYTHON} -m pip install -e .")


@task
def data(c: Context) -> None:
    """Download the dataset from Kaggle."""
    c.run(f"{PYTHON} src/retrieve_data.py")  # -> -m nyc_airbnb.data after restructure


@task
def lint(c: Context) -> None:
    """Run linting and formatting checks."""
    c.run(f"ruff check {CODE_PATHS}")
    c.run(f"ruff format --check {CODE_PATHS}")


@task(name="format")
def format_(c: Context) -> None:
    """Automatically fix lint issues and format code with ruff."""
    c.run(f"ruff check --fix {CODE_PATHS}")
    c.run(f"ruff format {CODE_PATHS}")


@task
def typecheck(c: Context) -> None:
    """Run mypy."""
    c.run(f"mypy {MYPY_PATHS}")


@task
def test(c: Context) -> None:
    """Run unit tests with pytest."""
    c.run("pytest --cov=src tests/")


@task(pre=[lint, typecheck, test])
def check(c: Context) -> None:
    """Run lint, typecheck and tests (what CI should run)."""


@task
def precommit(c: Context) -> None:
    """Run all pre-commit hooks on every file."""
    c.run("pre-commit run --all-files")


@task
def typos(c: Context, fix: bool = False) -> None:
    """Spell-check the repo; with --fix, apply the corrections."""
    c.run("typos --write-changes" if fix else "typos")


@task
def clean(c: Context) -> None:
    """Remove bytecode, caches, build artifacts and the MkDocs site."""
    for pattern in ("**/__pycache__", "*.egg-info", "src/*.egg-info"):
        for path in Path(".").glob(pattern):
            shutil.rmtree(path, ignore_errors=True)
    for name in (
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "build",
        "dist",
        "site",
    ):
        shutil.rmtree(name, ignore_errors=True)
    Path(".coverage").unlink(missing_ok=True)


@task
def tree(c: Context, check: bool = False) -> None:
    """Regenerate the project tree in the README (--check to only verify)."""
    c.run(f"{PYTHON} scripts/update_readme_tree.py{' --check' if check else ''}")


@task
def docs_serve(c: Context) -> None:
    """Launch local MkDocs server with live reloading on src/."""
    c.run("mkdocs serve --watch src")


@task
def docs_build(c: Context) -> None:
    """Build the static documentation site."""
    c.run("mkdocs build")
