#!/usr/bin/env python3
"""Inspect JSON shape without echoing scalar values; not a schema validator."""
import argparse
import itertools
import json
import math
from pathlib import Path
import re
import sys


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError("nonfinite number")


def finite_float(text):
    value = float(text)
    if not math.isfinite(value):
        raise ValueError("nonfinite number")
    return value


def select(value, pointer):
    if pointer == "":
        return value
    if not pointer.startswith("/") or re.search(r"~(?![01])", pointer):
        raise ValueError("invalid pointer")
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            value = value[token]
        elif isinstance(value, list) and re.fullmatch(r"0|[1-9][0-9]*", token):
            value = value[int(token)]
        else:
            raise ValueError("missing pointer")
    return value


def describe(value, pointer):
    if value is None:
        kind = "null"
    elif isinstance(value, bool):
        kind = "boolean"
    elif isinstance(value, dict):
        kind = "object"
    elif isinstance(value, list):
        kind = "array"
    elif isinstance(value, str):
        kind = "string"
    else:
        kind = "number"
    result = {"pointer": pointer, "type": kind}
    if isinstance(value, (dict, list)):
        result["container_size"] = len(value)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--pointer", default="", help="RFC6901 pointer; default root")
    args = parser.parse_args()
    try:
        value = json.loads(args.file.read_text(encoding="utf-8"),
                           object_pairs_hook=object_pairs,
                           parse_constant=reject_constant, parse_float=finite_float)
        value = select(value, args.pointer)
        result = describe(value, args.pointer)
        if isinstance(value, (dict, list)):
            entries = value.items() if isinstance(value, dict) else enumerate(value)
            children = []
            for key, child in itertools.islice(entries, 100):
                token = str(key).replace("~", "~0").replace("/", "~1")
                children.append(describe(child, args.pointer + "/" + token))
            result.update(children=children, total=len(value),
                          unshown_count=len(value) - len(children))
    except (OSError, UnicodeError, ValueError, KeyError, IndexError, RecursionError):
        print("inspect-json: invalid input or unresolved pointer", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
