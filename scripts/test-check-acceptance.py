#!/usr/bin/env python3
"""CLI tests for declared acceptance evidence consistency."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).with_name('check-acceptance.py')
SHA = 'a' * 40

class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'evidence'
        self.root.mkdir()
        self.artifact = self.root / 'log.txt'
        self.artifact.write_bytes(b'synthetic log\n')
        self.digest = hashlib.sha256(self.artifact.read_bytes()).hexdigest()
        self.manifest = {'schema_version': 1, 'target': 'Demo target', 'required_gates': [
            {'id': 'browser', 'kind': 'full_e2e', 'suite': 'Full browser suite'}]}
        self.receipts = {'schema_version': 1, 'receipts': [self.receipt()]}

    def receipt(self):
        return {'gate_id': 'browser', 'target': 'Demo target', 'kind': 'full_e2e',
                'suite': 'Full browser suite', 'candidate_sha': SHA, 'candidate_ref': 'refs/heads/demo',
                'status': 'PASS', 'exit_code': 0, 'artifact_path': 'log.txt', 'artifact_sha256': self.digest}

    def run_cli(self, m=None, r=None, sha=SHA, ref='refs/heads/demo', root=None, extra=(), raw_m=None, raw_r=None):
        mp, rp = self.base / 'manifest.json', self.base / 'receipts.json'
        mp.write_bytes(raw_m if raw_m is not None else json.dumps(self.manifest if m is None else m).encode())
        rp.write_bytes(raw_r if raw_r is not None else json.dumps(self.receipts if r is None else r).encode())
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (mp, rp, self.artifact)}
        cmd = [sys.executable, str(HELPER), str(mp), str(rp), '--candidate-sha', sha,
               '--candidate-ref', ref, '--evidence-root', str(root or self.root), *extra]
        result = subprocess.run(cmd, capture_output=True, timeout=5)
        after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (mp, rp, self.artifact)}
        self.assertEqual(before, after)
        return result

    def check(self, expected, **kwargs):
        result = self.run_cli(**kwargs)
        self.assertEqual(result.returncode, expected, (result.stdout, result.stderr))
        self.assertEqual(result.stderr, b'')
        self.assertEqual(json.loads(result.stdout), {'result': ['EVIDENCE_CONSISTENT', 'EVIDENCE_INCOMPLETE', 'INVALID_INPUT'][expected]})
        return result

    def altered(self, **fields):
        r = copy.deepcopy(self.receipts)
        r['receipts'][0].update(fields)
        return r

    def test_success_sha_lengths_and_other_kind(self):
        self.check(0)
        self.check(0, sha='b'*64, r=self.altered(candidate_sha='b'*64))
        m = copy.deepcopy(self.manifest); m['required_gates'][0]['kind'] = 'other'
        self.check(0, m=m, r=self.altered(kind='other'))

    def test_scope_and_identity_mismatches(self):
        for change in ({'kind':'component'}, {'kind':'mocked_e2e'}, {'kind':'other'},
                       {'candidate_sha':'b'*40}, {'candidate_ref':'other'},
                       {'target':'other'}, {'suite':'other'}):
            with self.subTest(change=change): self.check(1, r=self.altered(**change))
        self.check(1, r={'schema_version':1, 'receipts':[]})
        self.check(2, r=self.altered(gate_id='renamed'))
        self.check(2, r=self.altered(kind='ci'))
        self.check(2, r={'schema_version':1, 'receipts':[self.receipt(), self.receipt()]})
        m=copy.deepcopy(self.manifest); m['required_gates'].append(m['required_gates'][0]); self.check(2,m=m)
        m=copy.deepcopy(self.manifest); m['required_gates'].append({'id':'unit','kind':'unit','suite':'Unit'})
        unit=self.receipt(); unit.update(gate_id='unit', kind='unit', suite='Unit')
        self.check(1,m=m,r={'schema_version':1,'receipts':[unit]})

    def test_status_and_precedence(self):
        for status, code in [('FAIL', 1), ('SKIPPED', None), ('NOT_RUN', None), ('PENDING', None)]:
            with self.subTest(status=status):
                self.check(1, r=self.altered(status=status, exit_code=code, artifact_path=None, artifact_sha256=None))
                self.check(1, r=self.altered(status=status, exit_code=code))
                self.check(2, r=self.altered(status=status, exit_code=code, artifact_sha256='0'*64))
        for fields in ({'status':'PASS','exit_code':1}, {'status':'FAIL','exit_code':0},
                       {'exit_code':True}, {'status':'PENDING','exit_code':0},
                       {'artifact_path':None,'artifact_sha256':None}, {'artifact_path':None}):
            with self.subTest(fields=fields): self.check(2,r=self.altered(**fields))
        self.check(2,r=self.altered(candidate_sha='b'*40,artifact_sha256='0'*64))

    def test_artifact_paths_and_content(self):
        (self.root/'empty').write_bytes(b'')
        (self.root/'dir').mkdir()
        (self.root/'alias').symlink_to(self.artifact)
        (self.root/'linkdir').symlink_to(self.root, target_is_directory=True)
        for path in ('missing','empty','dir','alias','linkdir/log.txt','/tmp/x','../x','./log.txt','a//x','a\\b','log.txt/'):
            with self.subTest(path=path): self.check(2,r=self.altered(artifact_path=path))
        self.check(2,r=self.altered(artifact_sha256='0'*64))
        self.artifact.write_bytes(b'changed')
        self.check(2)
        self.artifact.write_bytes(b'synthetic log\n')
        rootlink=self.base/'rootlink'; rootlink.symlink_to(self.root,target_is_directory=True)
        self.check(0,root=rootlink)
        loop=self.base/'loop'; loop.symlink_to(loop)
        self.check(2,root=loop)

    def test_strict_inputs_and_labels(self):
        for raw in (b'', b'{', b'\xff', b'{"schema_version":1,"schema_version":1}',
                    b'{"schema_version":NaN}', b'{"x":{"a":1,"a":2}}', b' '* (2*1024*1024+1)):
            with self.subTest(raw=raw[:50]): self.check(2,raw_m=raw)
        for m in ({}, {'schema_version':True,'target':'x','required_gates':[]},
                  {'schema_version':1,'target':'x','required_gates':[]},
                  {**self.manifest,'unknown':1}, {**self.manifest,'target':None}):
            with self.subTest(m=m): self.check(2,m=m)
        for ref in (' ', 'x\n', 'x\x85', 'x\u2028', 'x\ud800'):
            # Surrogates cannot be passed through OS argv; test them in JSON instead.
            with self.subTest(ref=repr(ref)):
                if '\ud800' in ref: self.check(2,r=self.altered(candidate_ref=ref))
                else: self.check(2,ref=ref)
        for sha in ('A'*40,'a'*39,'a'*41): self.check(2,sha=sha)

    def test_no_echo_or_execution(self):
        marker=self.base/'marker'
        sentinel='private-sentinel'
        m=copy.deepcopy(self.manifest)
        m['target']=f'$(touch {marker}) {sentinel}'
        r=self.altered(target=m['target'])
        self.check(0,m=m,r=r)
        self.assertFalse(marker.exists())
        m['required_gates'][0]['id']='private-secret-id'
        result=self.check(2,m=m,extra=['--private-secret-argument'])
        self.assertNotIn(sentinel.encode(),result.stdout+result.stderr)
        self.assertNotIn(b'private-secret',result.stdout+result.stderr)
        result=self.check(1, m=m, r={'schema_version':1,'receipts':[]})
        self.assertNotIn(b'private-secret-id', result.stdout + result.stderr)
        result=self.check(2,r=self.altered(artifact_path='private-sentinel'))
        self.assertNotIn(sentinel.encode(),result.stdout+result.stderr)

    def test_no_external_effects(self):
        mp, rp = self.base / 'manifest.json', self.base / 'receipts.json'
        mp.write_text(json.dumps(self.manifest)); rp.write_text(json.dumps(self.receipts))
        launcher = """
import runpy, sys
helper = sys.argv[1]
def guard(event, args):
    if event in ('subprocess.Popen', 'os.system', 'socket.connect', 'socket.bind'):
        raise RuntimeError('external effect')
    if event == 'open' and len(args) > 1:
        mode = args[1]
        if isinstance(mode, str) and any(c in mode for c in 'wax+'):
            raise RuntimeError('write')
sys.addaudithook(guard)
sys.argv = [helper] + sys.argv[2:]
runpy.run_path(helper, run_name='__main__')
"""
        command = [sys.executable, '-c', launcher, str(HELPER), str(mp), str(rp),
                   '--candidate-sha', SHA, '--candidate-ref', 'refs/heads/demo', '--evidence-root', str(self.root)]
        before = {str(p.relative_to(self.base)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.base.rglob('*') if p.is_file()}
        result = subprocess.run(command, capture_output=True, timeout=5)
        after = {str(p.relative_to(self.base)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in self.base.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {'result': 'EVIDENCE_CONSISTENT'})

if __name__ == '__main__': unittest.main(verbosity=2)
