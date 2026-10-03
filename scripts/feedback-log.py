#!/usr/bin/env python3
"""Validate, append, and audit Agent Orchestrator feedback journals."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

CATEGORIES = {
    "verifier_rejection",
    "user_correction",
    "routing",
    "spec_defect",
    "blocked",
    "pattern",
    "deterministic_extraction",
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
OPTIONAL_FIELDS = {"rule", "session_id"}
ISSUE_KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
DEFAULT_LOG = Path(__file__).resolve().parents[1] / "feedback" / "log.jsonl"
SUSPICIOUS_DATE_REGRESSION = timedelta(days=30)


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
    if "session_id" in value and (
        not isinstance(value["session_id"], str) or not value["session_id"].strip()
    ):
        raise ValueError("session_id must be a non-empty string when present")

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
    if "session_id" in value:
        ordered_fields.append("session_id")
    ordered_fields.append("status")
    return {field: value[field] for field in ordered_fields}


def record_fingerprint(record: dict[str, str]) -> str:
    """Canonical fingerprint used only for exact duplicate detection."""
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def existing_fingerprints(handle: Any) -> dict[str, int]:
    handle.seek(0)
    found: dict[str, int] = {}
    for line_number, raw in enumerate(handle, 1):
        try:
            value = json.loads(raw.decode("utf-8"))
            record = validate_record(value)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            continue
        found.setdefault(record_fingerprint(record), line_number)
    return found


def append_record(log_path: Path, record: dict[str, str]) -> None:
    payload = (
        json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        duplicate_line = existing_fingerprints(handle).get(record_fingerprint(record))
        if duplicate_line is not None:
            raise ValueError(f"exact duplicate of existing line {duplicate_line}")

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


def audit_log(log_path: Path) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    seen: dict[str, int] = {}
    latest_date: date | None = None
    record_count = 0

    if not log_path.exists():
        return errors, warnings, 0

    with log_path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                record = validate_record(json.loads(raw))
            except (json.JSONDecodeError, ValueError) as exc:
                errors.append(f"line {line_number}: {exc}")
                continue

            record_count += 1
            fingerprint = record_fingerprint(record)
            if fingerprint in seen:
                errors.append(
                    f"line {line_number}: exact duplicate of line {seen[fingerprint]}"
                )
            else:
                seen[fingerprint] = line_number

            current_date = date.fromisoformat(record["date"])
            if latest_date is not None and current_date < latest_date - SUSPICIOUS_DATE_REGRESSION:
                warnings.append(
                    f"line {line_number}: date {current_date.isoformat()} regresses more than "
                    f"30 days behind prior maximum {latest_date.isoformat()}; verify provenance"
                )
            if latest_date is None or current_date > latest_date:
                latest_date = current_date

    return errors, warnings, record_count


def archived_fingerprints(archive_path: Path) -> set[str]:
    """Fingerprints of archived records with their status reset to "new"."""
    found: set[str] = set()
    if not archive_path.exists():
        return found
    with archive_path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            try:
                value = json.loads(raw)
                value["status"] = "new"
                found.add(record_fingerprint(validate_record(value)))
            except (json.JSONDecodeError, TypeError, ValueError):
                continue
    return found


def archive_records(log_path: Path, archive_path: Path, dispositions: Any) -> int:
    """Move dispositioned records to the archive under the append lock.

    `dispositions` is a JSON list of {"record": <journal record>,
    "disposition": "applied@<version>" | "rejected(<reason>)"}. Records are
    matched by canonical fingerprint, so events appended after the caller's
    snapshot stay in the journal. Nothing is written unless every disposition
    matches exactly one journal line.
    """
    if not isinstance(dispositions, list) or not dispositions:
        raise ValueError("dispositions must be a non-empty JSON list")
    wanted: dict[str, str] = {}
    for item in dispositions:
        if not isinstance(item, dict) or set(item) != {"record", "disposition"}:
            raise ValueError('each disposition needs exactly "record" and "disposition"')
        label = item["disposition"]
        if not isinstance(label, str) or not re.fullmatch(
            r"applied@\d+\.\d+\.\d+|rejected\(.+\)", label, re.S
        ):
            raise ValueError(f"bad disposition label: {label!r}")
        fingerprint = record_fingerprint(validate_record(item["record"]))
        if fingerprint in wanted:
            raise ValueError("the same record is dispositioned twice")
        wanted[fingerprint] = label

    with log_path.open("r+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        already = archived_fingerprints(archive_path)
        raw_lines = handle.read().decode("utf-8").splitlines(keepends=True)
        kept: list[str] = []
        moved: list[str] = []
        matched: set[str] = set()
        for raw in raw_lines:
            if not raw.strip():
                continue
            record = validate_record(json.loads(raw))
            fingerprint = record_fingerprint(record)
            if fingerprint in wanted and fingerprint not in matched:
                matched.add(fingerprint)
                if fingerprint in already:
                    continue  # moved by an interrupted earlier run; drop the copy
                record["status"] = wanted[fingerprint]
                moved.append(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
            else:
                kept.append(raw if raw.endswith("\n") else raw + "\n")
        missing = len(wanted) - len(matched)
        if missing:
            raise ValueError(f"{missing} disposition(s) match no journal line; nothing moved")
        if len(kept) + len(matched) != sum(1 for raw in raw_lines if raw.strip()):
            raise OSError("record count mismatch; nothing moved")

        with archive_path.open("a+b") as archive:
            archive.seek(0, os.SEEK_END)
            if archive.tell():
                archive.seek(-1, os.SEEK_END)
                if archive.read(1) != b"\n":
                    archive.write(b"\n")
            archive.write("".join(moved).encode("utf-8"))
            archive.flush()
            os.fsync(archive.fileno())

        handle.seek(0)
        handle.write("".join(kept).encode("utf-8"))
        handle.truncate()
        handle.flush()
        os.fsync(handle.fileno())
    return len(matched)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    append_parser = subparsers.add_parser("append", help="validate and append one event")
    append_parser.add_argument("--record-json", required=True)
    append_parser.add_argument(
        "--log", type=Path, default=DEFAULT_LOG, help=argparse.SUPPRESS
    )

    audit_parser = subparsers.add_parser(
        "audit", help="validate the journal and detect duplicates/date anomalies"
    )
    audit_parser.add_argument(
        "--log", type=Path, default=DEFAULT_LOG, help=argparse.SUPPRESS
    )

    archive_parser = subparsers.add_parser(
        "archive", help="move dispositioned records to archive.jsonl under the lock"
    )
    archive_parser.add_argument("--dispositions", type=Path, required=True)
    archive_parser.add_argument(
        "--log", type=Path, default=DEFAULT_LOG, help=argparse.SUPPRESS
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "archive":
        try:
            dispositions = json.loads(args.dispositions.read_text(encoding="utf-8"))
            moved = archive_records(
                args.log, args.log.with_name("archive.jsonl"), dispositions
            )
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            print(f"feedback-log: {exc}", file=sys.stderr)
            return 1
        print(f"feedback-log: archived {moved} record(s)")
        return 0

    if args.command == "audit":
        errors, warnings, record_count = audit_log(args.log)
        for warning in warnings:
            print(f"feedback-log: warning: {warning}", file=sys.stderr)
        for error in errors:
            print(f"feedback-log: error: {error}", file=sys.stderr)
        if errors:
            return 1
        print(
            f"feedback-log: audit OK ({record_count} records, {len(warnings)} warning(s))"
        )
        return 0

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
