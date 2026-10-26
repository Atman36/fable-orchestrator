#!/usr/bin/env python3
"""Offline tests for handoff snapshot validator."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("handoff-validate.py")
spec = importlib.util.spec_from_file_location("handoff_validate", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        for command in (["git", "init", "-q", str(self.root)],
                        ["git", "-C", str(self.root), "config", "user.email", "test@example.com"],
                        ["git", "-C", str(self.root), "config", "user.name", "test"]):
            subprocess.run(command, check=True, capture_output=True)
        (self.root / "x.txt").write_text("1\n")
        subprocess.run(["git", "-C", str(self.root), "add", "x.txt"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "init"], check=True)
        self.branch = subprocess.check_output(["git", "-C", str(self.root), "branch", "--show-current"], text=True).strip()
        self.sha = subprocess.check_output(["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True).strip()
        self.taskdir = Path(self.tmp.name) / "task"
        self.taskdir.mkdir()
        self.state = {
            "schema_version": 1, "handoff_id": "test-1", "generation": 1,
            "outgoing_head": "old", "next_task": "run test", "blockers": [],
            "checks": [], "workers": [],
            "git": {"repo_root": str(self.root), "branch": self.branch, "head_sha": self.sha,
                    "checked_at": "2026-10-26T08:00:00Z"}
        }
        (self.taskdir / "NEXT-SESSION.md").write_text("## Done\nnone\n## Remaining\nnext\n## Branch\nrepo\n## Next command\ngit status\n")
        self.write_state()
        self.ack()

    def write_json(self, name, data):
        (self.taskdir / name).write_text(json.dumps(data, indent=2) + "\n")

    def write_state(self):
        self.write_json("STATE.json", self.state)
        digest = hashlib.sha256((self.taskdir / "STATE.json").read_bytes()).hexdigest()
        self.release = {"status": "RELEASED", "handoff_id": self.state["handoff_id"],
                        "generation": self.state["generation"], "state_sha256": digest,
                        "next_sha256": hashlib.sha256((self.taskdir / "NEXT-SESSION.md").read_bytes()).hexdigest(),
                        "released_by": "old", "released_at": "2026-10-26T08:02:00Z"}
        self.write_json("RELEASE.json", self.release)

    def ack(self):
        self.write_json("ACK.json", {"status": "ACCEPTED", "handoff_id": self.state["handoff_id"],
                                   "generation": self.state["generation"],
                                   "state_sha256": self.release["state_sha256"],
                                   "next_sha256": self.release["next_sha256"],
                                   "accepted_by": "new", "accepted_at": "2026-10-26T08:03:00Z",
                                   "observed_branch": self.branch, "observed_head_sha": self.sha,
                                   "remaining_workers": []})

    def test_release_valid(self):
        self.assertIn("SNAPSHOT_VALIDATED", module.validate(self.taskdir, "release"))

    def test_ack_valid(self):
        self.assertIn("no proof", module.validate(self.taskdir, "ack"))

    def test_modified_state_blocks(self):
        self.state["next_task"] = "tampered"
        self.write_json("STATE.json", self.state)
        with self.assertRaisesRegex(module.Invalid, "sha256"):
            module.validate(self.taskdir, "ack")

    def test_wrong_ack_blocks(self):
        self.ack()
        a = json.loads((self.taskdir / "ACK.json").read_text())
        a["observed_head_sha"] = "0" * 40
        self.write_json("ACK.json", a)
        with self.assertRaisesRegex(module.Invalid, "observed Git"):
            module.validate(self.taskdir, "ack")

    def test_missing_release_blocks(self):
        (self.taskdir / "RELEASE.json").unlink()
        with self.assertRaisesRegex(module.Invalid, "RELEASE.json"):
            module.validate(self.taskdir, "release")

    def test_stale_head_blocks(self):
        (self.root / "x.txt").write_text("2\n")
        subprocess.run(["git", "-C", str(self.root), "commit", "-qam", "change"], check=True)
        with self.assertRaisesRegex(module.Invalid, "stale Git snapshot"):
            module.validate(self.taskdir, "release")

    def test_modified_next_session_blocks(self):
        (self.taskdir / "NEXT-SESSION.md").write_text("## Done\nnew\n## Remaining\nnext\n## Branch\nrepo\n## Next command\ngit status\n")
        with self.assertRaisesRegex(module.Invalid, "next_sha256"):
            module.validate(self.taskdir, "release")

    def test_incomplete_next_session_blocks(self):
        (self.taskdir / "NEXT-SESSION.md").write_text("## Done\n")
        with self.assertRaisesRegex(module.Invalid, "missing ## Remaining"):
            module.validate(self.taskdir, "release")

    def test_invalid_generation_blocks(self):
        self.state["generation"] = True
        self.write_state()
        with self.assertRaisesRegex(module.Invalid, "generation"):
            module.validate(self.taskdir, "release")


if __name__ == "__main__":
    unittest.main()
