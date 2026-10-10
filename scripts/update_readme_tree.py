"""Regenerate the project tree in README.md between the TREEVIEW markers.

Usage:
    python scripts/update_readme_tree.py          # rewrite the tree
    python scripts/update_readme_tree.py --check  # exit 1 if README is out of date
"""

import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import tomllib

_ROOT = Path(__file__).resolve().parent.parent
_README = _ROOT / "README.md"
_START, _END = "<!-- TREEVIEW START -->", "<!-- TREEVIEW END -->"

# Tracked paths (any path component) that should not appear in the tree.
_HIDE = {"scripts"}

# Comments keyed by posix path relative to the root (directories without trailing slash).
_COMMENTS = {
    "docs": "MkDocs documentation sources",
    "notebooks": "Analysis notebooks, run in order",
    "src": "Reusable project code, imported by the notebooks",
    "src/dataset.py": "Dataset download (kagglehub) and loading",
    "src/plots.py": "Plotting helpers",
    ".env.example": "Template for Kaggle credentials (copy to .env)",
    "pyproject.toml": "Package metadata, dependencies and tool configuration",
    "tasks.py": "Invoke tasks (see `invoke --list`)",
    ".secrets.baseline": "detect-secrets baseline (accepted findings)",
}


def _project_name() -> str:
    """Repo name from [project.urls].Repository, falling back to [project].name."""
    with (_ROOT / "pyproject.toml").open("rb") as f:
        project = tomllib.load(f)["project"]
    repo = project.get("urls", {}).get("Repository")
    if repo:
        return repo.rstrip("/").removesuffix(".git").rsplit("/", 1)[-1]
    return project["name"]


def _tracked_files() -> list[Path]:
    """Files git tracks or would track (untracked but not ignored)."""
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    paths = (Path(p) for p in out.split("\0") if p)
    # --cached also lists files deleted from disk but still in the index
    return [p for p in paths if (_ROOT / p).exists() and not _HIDE & set(p.parts)]


def _build_nested(paths: list[Path]) -> dict:
    tree: dict = {}
    for path in paths:
        node = tree
        for part in path.parts:
            node = node.setdefault(part, {})
    return tree  # only files are tracked, so an empty dict is a file


def _rows(node: dict, prefix: str = "", parent: str = "") -> Iterator[tuple[str, str]]:
    """Yield (display text, relative path) for each entry, folders first."""
    items = sorted(node.items(), key=lambda kv: (not kv[1], kv[0].casefold()))
    for i, (name, child) in enumerate(items):
        last = i == len(items) - 1
        rel = f"{parent}{name}"
        yield f"{prefix}{'└── ' if last else '├── '}{name}{'/' if child else ''}", rel
        if child:
            yield from _rows(child, prefix + ("    " if last else "│   "), rel + "/")


def _render() -> str:
    lines = list(_rows(_build_nested(_tracked_files())))
    stale = set(_COMMENTS) - {rel for _, rel in lines}
    if stale:
        sys.exit(f"COMMENTS refer to paths not in the tree: {sorted(stale)}")
    width = max(len(text) for text, _ in lines) + 2
    out = [f"{_project_name()}/"]
    for text, rel in lines:
        comment = _COMMENTS.get(rel)
        out.append(f"{text:<{width}}# {comment}" if comment else text)
    return "\n".join(out)


def main(check: bool = False) -> None:
    text = _README.read_text(encoding="utf-8")
    try:
        head, rest = text.split(_START, 1)
        _, tail = rest.split(_END, 1)
    except ValueError:
        sys.exit(f"Markers {_START} / {_END} not found in {_README.name}")

    new = f"{head}{_START}\n```text\n{_render()}\n```\n{_END}{tail}"
    if check:
        if new != text:
            sys.exit("README tree is out of date; run `invoke tree`")
        return
    if new != text:
        _README.write_text(new, encoding="utf-8", newline="\n")
        print("Updated file tree in README.md")


if __name__ == "__main__":
    main(check="--check" in sys.argv)
