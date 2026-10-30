#!/usr/bin/env python3
"""Rename screenshot files using the text between the first and last underscore."""

import argparse
import sys
from pathlib import Path


def get_new_name(file_name: str) -> str | None:
    first = file_name.find("_")
    last = file_name.rfind("_")
    if first == -1 or first == last:
        return None
    return f"{file_name[first + 1:last]}.png"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="directory containing screenshot files")
    directory = parser.parse_args().directory

    if not directory.is_dir():
        parser.error(f"not a directory: {directory}")

    files = sorted(path for path in directory.iterdir() if path.is_file())
    renames = []
    for source in files:
        new_name = get_new_name(source.name)
        if new_name is None:
            print(f"Skipping (expected at least two underscores): {source.name}")
            continue
        destination = source.with_name(new_name)
        if destination != source:
            renames.append((source, destination))

    destinations = [destination for _, destination in renames]
    if len(destinations) != len(set(destinations)):
        print("Error: multiple files would have the same destination; no files renamed.", file=sys.stderr)
        return 1

    conflicts = [destination for source, destination in renames if destination.exists()]
    if conflicts:
        print(
            "Error: destination already exists; no files renamed: "
            + ", ".join(str(path) for path in conflicts),
            file=sys.stderr,
        )
        return 1

    for source, destination in renames:
        source.rename(destination)
        print(f"{source.name} -> {destination.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
