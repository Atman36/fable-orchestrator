#!/usr/bin/env python3
"""Validate and append one Fable feedback event without replacing peer data."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

CATEGORIES = {
    "verifier_rejection",
    "user_correction",
    "routing",
    "spec_defect",
    "blocked",
    "pattern",
}
REQUIRED_FIELDS = {
    "date",
    "project",
    "task",
    "category",
    "issue_key",
    "observation",
    "lesson",
    "status",
}
OPTIONAL_FIELDS = {"rule"}
ISSUE_KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
DEFAULT_LOG = Path(__file__).resolve().parents[1] / "feedback" / "log.jsonl"


def validate_record(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValueError("record must be a JSON object")

    keys = set(value)
    missing = sorted(REQUIRED_FIELDS - keys)
    unknown = sorted(keys - REQUIRED_FIELDS - OPTIONAL_FIELDS)
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    if unknown:
        raise ValueError(f"unknown fields: {', '.join(unknown)}")

    for field in REQUIRED_FIELDS:
        if not isinstance(value[field], str) or not value[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    if "rule" in value and not isinstance(value["rule"], str):
        raise ValueError("rule must be a string when present")

    try:
        date.fromisoformat(value["date"])
    except ValueError as exc:
        raise ValueError("date must be an ISO-8601 calendar date") from exc
    if value["category"] not in CATEGORIES:
        allowed = ", ".join(sorted(CATEGORIES))
        raise ValueError(f"category must be one of: {allowed}")
    if not ISSUE_KEY.fullmatch(value["issue_key"]):
        raise ValueError("issue_key must be lowercase kebab-case")
    if value["status"] != "new":
        raise ValueError('status must be "new"')

    ordered_fields = [
        "date",
        "project",
        "task",
        "category",
        "issue_key",
        "observation",
        "lesson",
    ]
    if "rule" in value:
        ordered_fields.append("rule")
    ordered_fields.append("status")
    return {field: value[field] for field in ordered_fields}


def append_record(log_path: Path, record: dict[str, str]) -> None:
    payload = (
        json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0, os.SEEK_END)
        size = handle.tell()
        if size:
            handle.seek(-1, os.SEEK_END)
            if handle.read(1) != b"\n":
                handle.write(b"\n")
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
        handle.seek(-len(payload), os.SEEK_END)
        if handle.read(len(payload)) != payload:
            raise OSError("feedback append verification failed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    append_parser = subparsers.add_parser("append", help="validate and append one event")
    append_parser.add_argument("--record-json", required=True)
    append_parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help=argparse.SUPPRESS)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        record = validate_record(json.loads(args.record_json))
        append_record(args.log, record)
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"feedback-log: {exc}", file=sys.stderr)
        return 1
    print(f"feedback-log: appended {record['issue_key']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
