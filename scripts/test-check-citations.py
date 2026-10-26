#!/usr/bin/env python3
"""Behavioral subprocess checks for the exact-line citation contract."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().with_name("check-citations.py")
ERROR = b"check-citations: invalid input or citation\n"


def tree_snapshot(root):
    snapshot = {}
    for entry in root.rglob("*"):
        key = str(entry.relative_to(root))
        if entry.is_symlink():
            snapshot[key] = ("symlink", str(entry.readlink()))
        elif entry.is_file():
            snapshot[key] = ("file", hashlib.sha256(entry.read_bytes()).hexdigest())
        else:
            snapshot[key] = ("directory",)
    return snapshot


class CitationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "source"
        self.root.mkdir()
        self.manifest_dir = self.base / "manifests"
        self.manifest_dir.mkdir()
        self.manifest = self.manifest_dir / "citations.json"
        (self.root / "source.txt").write_bytes(
            "source-private-marker\n  точная\tцитата  \n\nneedle only here\n".encode("utf-8")
        )

    def record(self, **changes):
        item = {"path": "source.txt", "line": 2, "quote": "  точная\tцитата  "}
        item.update(changes)
        return item

    def run_helper(self, records=None, raw=None, root=None, args=None, forbid_source_reads=False):
        if raw is None:
            raw = json.dumps(records, ensure_ascii=False).encode("utf-8")
        self.manifest.write_bytes(raw)
        before = tree_snapshot(self.base)
        command = [sys.executable, str(HELPER)]
        if forbid_source_reads:
            # Observe file opens in the real helper process, without importing it into this test runner.
            launcher = """
import os, runpy, sys
source_root = os.path.realpath(sys.argv[1])
helper = sys.argv[2]
def audit(event, args):
    if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        candidate = os.path.realpath(os.fsdecode(args[0]))
        if os.path.commonpath([source_root, candidate]) == source_root:
            raise SystemExit("unexpected source read")
sys.addaudithook(audit)
sys.argv = [helper] + sys.argv[3:]
runpy.run_path(helper, run_name="__main__")
"""
            command = [sys.executable, "-c", launcher, str(self.root), str(HELPER)]
        command.extend(args if args is not None else [str(self.manifest), "--root", str(root or self.root)])
        result = subprocess.run(command, capture_output=True, timeout=5, cwd=self.manifest_dir)
        self.assertEqual(tree_snapshot(self.base), before, "helper modified fixture files or wrote siblings")
        return result

    def assert_failure(self, result):
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(result.stderr, ERROR)

    def test_multiple_unicode_crlf_and_literal_whitespace(self):
        (self.root / "данные.txt").write_bytes("первая\r\nΩ café\r\n".encode("utf-8"))
        result = self.run_helper([
            self.record(),
            self.record(line=4, quote="needle only here"),
            self.record(path="данные.txt", line=2, quote="Ω café"),
        ])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b'{"checked":3,"files":2}\n')
        self.assertEqual(result.stderr, b"")

    def test_unicode_separators_are_literal_source_characters(self):
        (self.root / "unicode.txt").write_text("A\u2028B\u0085C\nsecond\n", encoding="utf-8")
        result = self.run_helper([
            self.record(path="unicode.txt", line=1, quote="A\u2028B\u0085C"),
            self.record(path="unicode.txt", line=2, quote="second"),
        ])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b'{"checked":2,"files":1}\n')
        self.assertEqual(result.stderr, b"")

    def test_wrong_line_blank_line_and_out_of_range(self):
        for line in [1, 2, 3, 5, 999]:
            with self.subTest(line=line):
                self.assert_failure(self.run_helper([self.record(line=line, quote="needle only here")]))

    def test_quote_must_be_literal_nonblank_and_one_physical_line(self):
        for quote in [None, 4, True, "", " \t", "\u2003", "needle.*", "ТОЧНАЯ", "точная цитата", "точная\nцитата", "точная\rцитата"]:
            with self.subTest(quote=quote):
                self.assert_failure(self.run_helper([self.record(quote=quote)]))
        self.assert_failure(self.run_helper([self.record(line=4, quote="needle.*")]))

    def test_schema_and_line_types(self):
        cases = [[], {}, None, "array", [None], [42], [True], [[]],
                 [{"path": "source.txt", "line": 2}],
                 [self.record(extra="forbidden")]]
        cases.extend([self.record(line=line)] for line in [True, False, 0, -1, 2.0, "2", None])
        cases.extend([self.record(path=source)] for source in [None, 8, True, [], {}])
        for records in cases:
            with self.subTest(records=records):
                self.assert_failure(self.run_helper(records))

    def test_malformed_duplicate_nonfinite_and_invalid_utf8_json(self):
        cases = [b"", b"[", b"[{", b"[] trailing", b"[] []", b"[{},]", b"\xff", b"\xef\xbb\xbf[]",
                 b'[{"path":"source.txt","path":"source.txt","line":2,"quote":"x"}]',
                 b'[{"path":"source.txt","line":2,"quote":"x","extra":{"a":1,"a":2}}]']
        for value in [b"NaN", b"Infinity", b"-Infinity"]:
            cases.append(b'[{"path":"source.txt","line":' + value + b',"quote":"x"}]')
            cases.append(b'[{"path":"source.txt","line":2,"quote":"x","extra":' + value + b'}]')
        for raw in cases:
            with self.subTest(raw=raw):
                self.assert_failure(self.run_helper(raw=raw))

    def test_complete_manifest_validation_precedes_source_reads(self):
        first = self.record()
        observed = self.run_helper([first], forbid_source_reads=True)
        self.assertNotEqual(observed.returncode, 0)
        self.assertEqual(observed.stdout, b"")
        self.assertEqual(observed.stderr, b"unexpected source read\n")
        raw_prefix = json.dumps([first]).encode("utf-8")[:-1]
        for raw in [raw_prefix + b",", raw_prefix + b',{"path":"source.txt","line":2,"quote":"x","quote":"y"}]',
                    raw_prefix + b',{"path":"source.txt","line":NaN,"quote":"x"}]']:
            with self.subTest(raw=raw):
                self.assert_failure(self.run_helper(raw=raw, forbid_source_reads=True))
        self.assert_failure(self.run_helper([first, self.record(line=True)], forbid_source_reads=True))

    def test_canonical_relative_path_and_containment(self):
        outside = self.base / "outside.txt"
        outside.write_text("private-quote-marker\n", encoding="utf-8")
        paths = ["", "/source.txt", str(outside), "../outside.txt", "./source.txt", "a/../source.txt",
                 "a/./source.txt", "a//b", "source.txt/", "a\\b", "a\x00b", "a\nb", "a\tb", "a\x7fb", "a\x85b"]
        for source in paths:
            with self.subTest(source=source):
                self.assert_failure(self.run_helper([self.record(path=source, line=1, quote="private-quote-marker")]))

    def test_symlink_escape_and_inside_alias(self):
        outside = self.base / "outside.txt"
        outside.write_text("private-quote-marker\n", encoding="utf-8")
        (self.root / "escape").symlink_to(outside)
        (self.root / "escape-dir").symlink_to(self.base, target_is_directory=True)
        for source in ["escape", "escape-dir/outside.txt"]:
            with self.subTest(source=source):
                self.assert_failure(self.run_helper([self.record(path=source, line=1, quote="private-quote-marker")]))
        (self.root / "alias").symlink_to(self.root / "source.txt")
        result = self.run_helper([self.record(), self.record(path="alias")])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b'{"checked":2,"files":1}\n')
        self.assertEqual(result.stderr, b"")

    def test_invalid_roots_missing_and_nonfile_sources(self):
        for root in [self.base / "missing-root", self.root / "source.txt"]:
            with self.subTest(root=root):
                self.assert_failure(self.run_helper([self.record()], root=root))
        (self.root / "directory").mkdir()
        (self.root / "broken").symlink_to(self.base / "absent")
        (self.root / "loop").symlink_to("loop")
        os.mkfifo(self.root / "fifo")
        for source in ["missing", "directory", "broken", "loop", "fifo"]:
            with self.subTest(source=source):
                self.assert_failure(self.run_helper([self.record(path=source)]))

    def test_invalid_utf8_anywhere_in_source(self):
        (self.root / "bad.txt").write_bytes(b"matching quote\n\xff\n")
        self.assert_failure(self.run_helper([self.record(path="bad.txt", line=1, quote="matching quote")]))

    def test_later_failure_emits_no_partial_success(self):
        self.assert_failure(self.run_helper([self.record(), self.record(line=3)]))
        self.assert_failure(self.run_helper([self.record(), self.record(path="missing")]))

    def test_hash_preservation_and_no_sibling_writes(self):
        (self.manifest_dir / "untouched.txt").write_text("manifest sibling\n", encoding="utf-8")
        (self.root / "untouched.txt").write_text("source sibling\n", encoding="utf-8")
        result = self.run_helper([self.record()])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b'{"checked":1,"files":1}\n')
        self.assertEqual(result.stderr, b"")
        self.assert_failure(self.run_helper([self.record(quote="private-quote-marker")]))

    def test_cli_and_manifest_file_errors_are_generic(self):
        for args in [[], ["private-argument-marker"], [str(self.manifest), "--unknown", str(self.root)],
                     [str(self.base / "missing.json"), "--root", str(self.root)],
                     [str(self.manifest_dir), "--root", str(self.root)]]:
            with self.subTest(args=args):
                self.assert_failure(self.run_helper([self.record()], args=args))


if __name__ == "__main__":
    unittest.main(verbosity=2)
