#!/usr/bin/env python3
"""CLI contract tests for value-free JSON shape inspection; stdlib only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).with_name("inspect-json.py")
SECRET = "scalar-content-must-never-be-printed"


class InspectJsonTests(unittest.TestCase):
    def invoke(self, raw, pointer=None, success=True):
        data = raw if isinstance(raw, bytes) else raw.encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            source.write_bytes(data)
            before = hashlib.sha256(source.read_bytes()).hexdigest()
            command = [sys.executable, str(HELPER), str(source)]
            if pointer is not None:
                command.extend(["--pointer", pointer])
            process = subprocess.run(command, capture_output=True, text=True, timeout=5)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)
            self.assertEqual([item.name for item in Path(directory).iterdir()], ["input.json"])
        self.assertNotIn(SECRET, process.stdout + process.stderr)
        if success:
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(process.stderr, "")
            return json.loads(process.stdout)
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(process.stdout, "")
        self.assertEqual(process.stderr, "inspect-json: invalid input or unresolved pointer\n")

    def test_object_immediate_shapes(self):
        raw = json.dumps({"dict": {"inner": SECRET}, "list": [SECRET, 91],
                          "null": None, "bool": True, "string": SECRET,
                          "number": 73123456789})
        actual = self.invoke(raw)
        self.assertEqual(actual, {"pointer": "", "type": "object", "container_size": 6,
            "total": 6, "unshown_count": 0, "children": [
                {"pointer": "/dict", "type": "object", "container_size": 1},
                {"pointer": "/list", "type": "array", "container_size": 2},
                {"pointer": "/null", "type": "null"},
                {"pointer": "/bool", "type": "boolean"},
                {"pointer": "/string", "type": "string"},
                {"pointer": "/number", "type": "number"}]})
        self.assertNotIn("73123456789", json.dumps(actual))

    def test_scalars_and_empty_containers(self):
        for raw, kind in [('null', 'null'), ('true', 'boolean'), ('false', 'boolean'),
                          (json.dumps(SECRET), 'string'), ('98', 'number'), ('3.1', 'number')]:
            with self.subTest(raw=raw):
                self.assertEqual(self.invoke(raw), {"pointer": "", "type": kind})
        for raw, kind in [('{}', 'object'), ('[]', 'array')]:
            self.assertEqual(self.invoke(raw), {"pointer": "", "type": kind,
                "container_size": 0, "children": [], "total": 0, "unshown_count": 0})

    def test_array_and_leaf(self):
        raw = json.dumps([None, True, SECRET, {"item": []}])
        actual = self.invoke(raw)
        self.assertEqual([item['type'] for item in actual['children']],
                         ['null', 'boolean', 'string', 'object'])
        self.assertEqual([item['pointer'] for item in actual['children']], ['/0', '/1', '/2', '/3'])
        self.assertEqual(self.invoke(raw, '/2'), {"pointer": "/2", "type": "string"})
        self.assertEqual(self.invoke(raw, '/3/item')['type'], 'array')

    def test_escaped_and_empty_object_keys(self):
        raw = json.dumps({"a/b": {"~": SECRET}, "": True, "~1": None, "01": []})
        self.assertEqual(self.invoke(raw, '/a~1b/~0'), {"pointer": '/a~1b/~0', "type": 'string'})
        self.assertEqual(self.invoke(raw, '/')['type'], 'boolean')
        self.assertEqual(self.invoke(raw, '/~01')['type'], 'null')
        self.assertEqual(self.invoke(raw, '/01')['type'], 'array')
        self.assertEqual(self.invoke(raw)['children'][0]['pointer'], '/a~1b')

    def test_missing_and_invalid_pointers(self):
        raw = json.dumps({"array": [SECRET], "scalar": SECRET})
        for pointer in ['/absent', '/scalar/child', '/array/1', '/array/-', '/array/-1',
                        '/array/00', '/array/01', '/array/+0', '/array/٠', 'array', '/~2', '/~']:
            with self.subTest(pointer=pointer):
                self.invoke(raw, pointer, success=False)

    def test_duplicate_keys(self):
        for raw in ['{"key":1,"key":2}', '{"outer":{"key":1,"key":2}}',
                    '{"a":1,"\\u0061":2}']:
            self.invoke(raw, success=False)

    def test_nonfinite_numbers(self):
        for token in ['NaN', 'Infinity', '-Infinity', '1e9999']:
            self.invoke('{"item":' + token + '}', success=False)

    def test_truncated_malformed_and_nonutf8(self):
        for raw in ['{"secret":' + json.dumps(SECRET), '[] trailing', '', b'"\xff"']:
            self.invoke(raw, success=False)

    def test_child_limit_and_exact_coverage(self):
        for value in [list(range(137)), {str(i): SECRET for i in range(137)}]:
            actual = self.invoke(json.dumps(value))
            self.assertEqual(len(actual['children']), 100)
            self.assertEqual(actual['container_size'], 137)
            self.assertEqual(actual['total'], 137)
            self.assertEqual(actual['unshown_count'], 37)
            self.assertEqual(actual['total'], len(actual['children']) + actual['unshown_count'])
            self.assertEqual(actual['children'][-1]['pointer'], '/99')

    def test_parse_entire_input_even_for_selected_leaf(self):
        self.invoke('{"leaf":true,"other":NaN}', '/leaf', success=False)
        self.invoke('{"leaf":true,"other":{"x":1,"x":2}}', '/leaf', success=False)
        self.invoke('{"leaf":true} trailing', '/leaf', success=False)


if __name__ == '__main__':
    unittest.main(verbosity=2)
