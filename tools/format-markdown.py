#!/usr/bin/env python3
"""Format Markdown files with mdformat and MkDocs-compatible syntax support."""

import argparse
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_EXTENSIONS = {"gfm", "mkdocs"}

try:
    import mdformat
except ImportError:
    print(
        "Markdown formatter is missing. Install dependencies with: "
        "pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1)


def collect_markdown_files(paths: list[Path]) -> list[Path]:
    files = set()
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"path does not exist: {path}")
        if path.is_file():
            if path.suffix.lower() != ".md":
                raise ValueError(f"not a Markdown file: {path}")
            files.add(path)
        else:
            files.update(child for child in path.rglob("*.md") if child.is_file())
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report files that need formatting without changing them")
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Markdown files or directories (default: README.md and docs/)",
    )
    args = parser.parse_args()

    paths = args.paths or [REPOSITORY_ROOT / "README.md", REPOSITORY_ROOT / "docs"]
    try:
        files = collect_markdown_files(paths)
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))

    unformatted = []
    for path in files:
        if args.check:
            original = path.read_text(encoding="utf-8")
            formatted = mdformat.text(original, extensions=MARKDOWN_EXTENSIONS)
            if original != formatted:
                print(f"Needs formatting: {path}")
                unformatted.append(path)
        else:
            mdformat.file(path, extensions=MARKDOWN_EXTENSIONS)
            print(f"Formatted: {path}")

    if args.check and unformatted:
        print(f"{len(unformatted)} Markdown file(s) need formatting.", file=sys.stderr)
        return 1
    if args.check:
        print(f"Checked {len(files)} Markdown file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
