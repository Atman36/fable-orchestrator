#!/usr/bin/env python3
"""Validate a handoff snapshot and Git provenance, NOT exclusive ownership.

Usage: python3 scripts/handoff-validate.py <taskdir> --phase release|ack
The caller must separately verify old-head/worker termination or enforce
runtime fencing. Exit 0 means snapshot integrity only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


class Invalid(Exception):
    pass


def require_dict(source: Path) -> dict:
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise Invalid(f"cannot read valid JSON from {source.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise Invalid(f"{source.name} must be a JSON object")
    return value


def require_string(data: dict, key: str, source: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise Invalid(f"{source}.{key} must be a nonempty string")
    return value


def git_value(root: str, *args: str) -> str:
    try:
        proc = subprocess.run(["git", "-C", root, *args], capture_output=True,
                              text=True, check=False, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Invalid(f"git unavailable: {exc}") from exc
    if proc.returncode:
        raise Invalid(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def validate(taskdir: Path, phase: str) -> str:
    state_file = taskdir / "STATE.json"
    state = require_dict(state_file)
    if state.get("schema_version") != 1:
        raise Invalid("STATE.json.schema_version must be 1")
    hid = require_string(state, "handoff_id", "STATE")
    generation = state.get("generation")
    if not isinstance(generation, int) or isinstance(generation, bool) or generation < 0:
        raise Invalid("STATE.json.generation must be a nonnegative integer")
    require_string(state, "outgoing_head", "STATE")
    require_string(state, "next_task", "STATE")
    for key in ("checks", "blockers", "workers"):
        if not isinstance(state.get(key), list):
            raise Invalid(f"STATE.json.{key} must be an array")
    git = state.get("git")
    if not isinstance(git, dict):
        raise Invalid("STATE.json.git must be an object")
    root = require_string(git, "repo_root", "STATE.git")
    branch = require_string(git, "branch", "STATE.git")
    head = require_string(git, "head_sha", "STATE.git")
    require_string(git, "checked_at", "STATE.git")
    if not os.path.isabs(root):
        raise Invalid("STATE.git.repo_root must be absolute")
    if len(head) not in (40, 64) or any(c not in "0123456789abcdef" for c in head):
        raise Invalid("STATE.git.head_sha must be a full lowercase hex Git hash")
    if os.path.realpath(git_value(root, "rev-parse", "--show-toplevel")) != os.path.realpath(root):
        raise Invalid("observed git root differs from STATE.git.repo_root")
    actual_branch = git_value(root, "symbolic-ref", "--quiet", "--short", "HEAD") if branch != "HEAD" else "HEAD"
    actual_sha = git_value(root, "rev-parse", "HEAD")
    if actual_branch != branch or actual_sha != head:
        raise Invalid(f"stale Git snapshot: expected {branch}@{head}, observed {actual_branch}@{actual_sha}")
    next_file = taskdir / "NEXT-SESSION.md"
    try:
        next_content = next_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise Invalid(f"NEXT-SESSION.md unavailable: {exc}") from exc
    for heading in ("## Done", "## Remaining", "## Branch", "## Next command"):
        if not any(line.startswith(heading) for line in next_content.splitlines()):
            raise Invalid(f"NEXT-SESSION.md missing {heading}")
    digest = hashlib.sha256(state_file.read_bytes()).hexdigest()
    next_digest = hashlib.sha256(next_content.encode("utf-8")).hexdigest()
    release = require_dict(taskdir / "RELEASE.json")
    if release.get("status") != "RELEASED":
        raise Invalid("RELEASE.json status must be RELEASED")
    if release.get("handoff_id") != hid or release.get("generation") != generation:
        raise Invalid("RELEASE.json does not match STATE handoff_id/generation")
    if release.get("state_sha256") != digest:
        raise Invalid("RELEASE.json state_sha256 does not match STATE bytes")
    if release.get("next_sha256") != next_digest:
        raise Invalid("RELEASE.json next_sha256 does not match NEXT-SESSION bytes")
    require_string(release, "released_by", "RELEASE")
    require_string(release, "released_at", "RELEASE")
    if phase == "ack":
        ack = require_dict(taskdir / "ACK.json")
        if ack.get("status") != "ACCEPTED":
            raise Invalid("ACK.json status must be ACCEPTED")
        if (ack.get("handoff_id") != hid or ack.get("generation") != generation or
                ack.get("state_sha256") != digest or
                ack.get("next_sha256") != next_digest):
            raise Invalid("ACK.json does not match frozen STATE / RELEASE")
        if ack.get("observed_branch") != branch or ack.get("observed_head_sha") != head:
            raise Invalid("ACK.json observed Git state does not match live and frozen HEAD")
        require_string(ack, "accepted_by", "ACK")
        require_string(ack, "accepted_at", "ACK")
        if not isinstance(ack.get("remaining_workers"), list):
            raise Invalid("ACK.json.remaining_workers must be an array")
    return f"SNAPSHOT_VALIDATED ({phase}); no proof of exclusive ownership or worker liveness"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("taskdir", type=Path)
    parser.add_argument("--phase", choices=("release", "ack"), required=True)
    args = parser.parse_args()
    try:
        print(validate(args.taskdir, args.phase))
    except Invalid as exc:
        print(f"BLOCK handoff: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
