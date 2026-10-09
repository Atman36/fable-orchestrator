#!/usr/bin/env python3
"""Check literal quotes at exact local file:line pointers from a JSON manifest."""

import json
from pathlib import Path
import sys
import unicodedata


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("nonfinite number")


def load_manifest(manifest_path):
    records = json.loads(
        Path(manifest_path).read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    if not isinstance(records, list) or not records:
        raise ValueError("nonempty array required")
    for record in records:
        if not isinstance(record, dict) or set(record) != {"path", "line", "quote"}:
            raise ValueError("invalid fields")
        source_path = record["path"]
        if (
            not isinstance(source_path, str)
            or not source_path
            or "\\" in source_path
            or any(unicodedata.category(char) == "Cc" for char in source_path)
            or any(part in {"", ".", ".."} for part in source_path.split("/"))
        ):
            raise ValueError("invalid path")
        line = record["line"]
        if type(line) is not int or line < 1:
            raise ValueError("invalid line")
        quote = record["quote"]
        if (
            not isinstance(quote, str)
            or not quote.strip()
            or "\n" in quote
            or "\r" in quote
        ):
            raise ValueError("invalid quote")
    return records


def check(records, source_root):
    root = Path(source_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("invalid root")
    files = {}
    for record in records:
        source = (root / record["path"]).resolve(strict=True)
        source.relative_to(root)
        if not source.is_file():
            raise ValueError("not a regular file")
        if source not in files:
            # Only LF and CRLF delimit physical lines; Unicode remains literal.
            files[source] = source.read_bytes().decode("utf-8").split("\n")
        lines = files[source]
        index = record["line"] - 1
        if index >= len(lines):
            raise ValueError("line outside source")
        line = lines[index]
        if line.endswith("\r"):
            line = line[:-1]
        if record["quote"] not in line:
            raise ValueError("quote absent at pointer")
    return {"checked": len(records), "files": len(files)}


def main():
    try:
        args = sys.argv[1:]
        if len(args) != 3 or args[1] != "--root":
            raise ValueError("invalid arguments")
        records = load_manifest(args[0])
        summary = check(records, args[2])
    except (OSError, UnicodeError, ValueError, RuntimeError):
        print("check-citations: invalid input or citation", file=sys.stderr)
        return 1
    print(json.dumps(summary, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
