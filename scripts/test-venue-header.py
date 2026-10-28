#!/usr/bin/env python3
"""CLI contract tests for measured venue headers; stdlib only."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).with_name("venue-header.py")


class VenueHeaderTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.base = Path(self.directory.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.git("init")
        self.git("-c", "user.name=Venue Test", "-c", "user.email=venue@example.test",
                 "commit", "--allow-empty", "-m", "Initial commit")
        self.sha = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        process = subprocess.run(["git", "-C", str(self.root), *args],
                                 capture_output=True, text=True, check=True, timeout=5)
        return process.stdout

    def invoke(self, role, root=None, evidence=()):
        command = [sys.executable, str(HELPER), "--root", str(root or self.root),
                   "--task-dir", str(self.base / "task"), "--role", role]
        for path in evidence:
            command.extend(["--evidence-dir", str(path)])
        return subprocess.run(command, capture_output=True, text=True, timeout=5)

    def test_reader(self):
        evidence = [self.base / "evidence-one", self.base / "evidence-two"]
        process = self.invoke("reader", evidence=evidence)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stderr, "")
        self.assertEqual(process.stdout, "\n".join([
            "Venue (supplied by the head, not measured by you):",
            f"- repo root: {self.root.resolve()}",
            f"- HEAD: {self.sha}",
            f"- task directory: {(self.base / 'task').resolve()}",
            *[f"- evidence directory: {path.resolve()}" for path in evidence],
            'Echo the repo root and HEAD as the first lines of your report, marked "supplied, not measured".',
            "Read repository files only by absolute path under the repo root, plus the directories above; search with your read/grep/find tools.",
            "Do not run or request shell commands, counts, or test runs; mark anything that needs one UNMEASURED for the head.",
            ""]))
        self.assertNotIn("rev-parse", process.stdout)

    def test_executor(self):
        process = self.invoke("executor")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stderr, "")
        self.assertEqual(process.stdout, "\n".join([
            f"Venue: absolute repo root {self.root.resolve()} at HEAD {self.sha}; task directory {(self.base / 'task').resolve()}.",
            f"Before anything else, run `git -C {self.root.resolve()} rev-parse --show-toplevel HEAD` and paste the output as the first lines of your report; if it differs from the venue, STOP.",
            f"Address every file and command by absolute path or `git -C {self.root.resolve()}`: shell and eval-kernel cwd does not persist between calls.",
            ""]))

    def test_subdirectory_refused(self):
        nested = self.root / "evidence"
        nested.mkdir()
        process = self.invoke("reader", root=nested)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, "")
        self.assertEqual(len(process.stderr.splitlines()), 1)

    def test_non_git_directory_refused(self):
        process = self.invoke("reader", root=self.base)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, "")
        self.assertEqual(len(process.stderr.splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
