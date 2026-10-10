"""Print the targets in the Makefile that have a `## description` comment.

Used by `make help`. Usage: python scripts/make_help.py
"""

import re
from pathlib import Path

for line in Path("Makefile").read_text().splitlines():
    m = re.match(r"^([a-zA-Z0-9_-]+):.*?## (.*)$", line)
    if m:
        print(f"  {m[1]:<15} {m[2]}")
