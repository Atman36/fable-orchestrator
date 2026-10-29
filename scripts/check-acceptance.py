#!/usr/bin/env python3
"""Check consistency of declared required gates and evidence receipts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import unicodedata

LIMIT = 2 * 1024 * 1024
KINDS = {'lint', 'typecheck', 'unit', 'component', 'mocked_e2e', 'full_e2e',
         'integration', 'build', 'repo', 'review', 'other'}
STATUSES = {'PASS', 'FAIL', 'SKIPPED', 'NOT_RUN', 'PENDING'}
ID = re.compile(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z', re.ASCII)
SHA = re.compile(r'(?:[0-9a-f]{40}|[0-9a-f]{64})\Z', re.ASCII)
DIGEST = re.compile(r'[0-9a-f]{64}\Z', re.ASCII)

class Invalid(Exception):
    pass

class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Invalid

def pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise Invalid
        out[key] = value
    return out

def invalid_constant(value):
    raise Invalid

def load(path):
    with open(path, 'rb') as handle:
        data = handle.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise Invalid
    return json.loads(data.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid_constant)

def fields(value, expected):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise Invalid

def version(value):
    if type(value) is not int or value != 1:
        raise Invalid

def label(value):
    if (not isinstance(value, str) or not 1 <= len(value) <= 200 or not value.strip()
            or any(unicodedata.category(c) in {'Cc', 'Cs'} or c in '\u2028\u2029' for c in value)):
        raise Invalid

def identifier(value):
    if not isinstance(value, str) or len(value) > 64 or not ID.fullmatch(value):
        raise Invalid

def sha(value):
    if not isinstance(value, str) or not SHA.fullmatch(value):
        raise Invalid

def kind(value):
    if not isinstance(value, str) or value not in KINDS:
        raise Invalid

def artifact(root, path, digest):
    if (not isinstance(path, str) or not path or '\\' in path or path.startswith('/')
            or any(part in ('', '.', '..') for part in path.split('/'))
            or not isinstance(digest, str) or not DIGEST.fullmatch(digest)):
        raise Invalid
    current = root
    for part in path.split('/'):
        current = current / part
        if stat.S_ISLNK(current.lstat().st_mode):
            raise Invalid
    if not stat.S_ISREG(current.stat().st_mode):
        raise Invalid
    hasher = hashlib.sha256()
    count = 0
    with current.open('rb') as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            count += len(chunk)
            hasher.update(chunk)
    if count == 0 or hasher.hexdigest() != digest:
        raise Invalid

def validate(manifest, receipts, candidate_sha, candidate_ref, root):
    sha(candidate_sha)
    label(candidate_ref)
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise Invalid
    fields(manifest, ('schema_version', 'target', 'required_gates'))
    version(manifest['schema_version'])
    label(manifest['target'])
    gates = manifest['required_gates']
    if not isinstance(gates, list) or not gates:
        raise Invalid
    required = {}
    for gate in gates:
        fields(gate, ('id', 'kind', 'suite'))
        identifier(gate['id']); kind(gate['kind']); label(gate['suite'])
        if gate['id'] in required:
            raise Invalid
        required[gate['id']] = gate
    fields(receipts, ('schema_version', 'receipts'))
    version(receipts['schema_version'])
    if not isinstance(receipts['receipts'], list):
        raise Invalid
    seen = set()
    incomplete = False
    for receipt in receipts['receipts']:
        fields(receipt, ('gate_id', 'target', 'kind', 'suite', 'candidate_sha', 'candidate_ref',
                         'status', 'exit_code', 'artifact_path', 'artifact_sha256'))
        identifier(receipt['gate_id']); label(receipt['target']); kind(receipt['kind'])
        label(receipt['suite']); sha(receipt['candidate_sha']); label(receipt['candidate_ref'])
        gate_id = receipt['gate_id']
        if gate_id not in required or gate_id in seen:
            raise Invalid
        seen.add(gate_id)
        status, code = receipt['status'], receipt['exit_code']
        if not isinstance(status, str) or status not in STATUSES:
            raise Invalid
        if status in {'PASS', 'FAIL'}:
            if type(code) is not int or (status == 'PASS' and code != 0) or (status == 'FAIL' and code == 0):
                raise Invalid
        elif code is not None:
            raise Invalid
        path, digest = receipt['artifact_path'], receipt['artifact_sha256']
        if path is None and digest is None:
            if status == 'PASS':
                raise Invalid
        else:
            artifact(root, path, digest)
        gate = required[gate_id]
        if (status != 'PASS' or receipt['target'] != manifest['target']
                or receipt['kind'] != gate['kind'] or receipt['suite'] != gate['suite']
                or receipt['candidate_sha'] != candidate_sha or receipt['candidate_ref'] != candidate_ref):
            incomplete = True
    return not incomplete and seen == set(required)

def main():
    parser = Parser(prog='check-acceptance.py', description=__doc__)
    parser.add_argument('manifest')
    parser.add_argument('receipts')
    parser.add_argument('--candidate-sha', required=True)
    parser.add_argument('--candidate-ref', required=True)
    parser.add_argument('--evidence-root', required=True)
    try:
        args = parser.parse_args()
        result = validate(load(args.manifest), load(args.receipts), args.candidate_sha,
                          args.candidate_ref, args.evidence_root)
        code = 0 if result else 1
    except (Invalid, OSError, UnicodeError, ValueError, RuntimeError):
        code = 2
    print(json.dumps({'result': ('EVIDENCE_CONSISTENT', 'EVIDENCE_INCOMPLETE', 'INVALID_INPUT')[code]}, separators=(',', ':')))
    return code

if __name__ == '__main__':
    sys.exit(main())
