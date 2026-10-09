"""Remove build artifacts, caches, and generated docs.

Cross-platform replacement for `rm -rf` / `find`, used by `make clean`.
Usage: python scripts/clean.py
"""

import shutil
from pathlib import Path

for d in ["build", "dist", ".pytest_cache", "htmlcov", "site"]:
    shutil.rmtree(d, ignore_errors=True)

for p in Path(".").glob("*.egg-info"):
    shutil.rmtree(p, ignore_errors=True)

Path(".coverage").unlink(missing_ok=True)

for p in Path(".").rglob("__pycache__"):
    if ".venv" not in p.parts:
        shutil.rmtree(p, ignore_errors=True)