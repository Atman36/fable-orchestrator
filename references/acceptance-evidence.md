# Required-gate evidence consistency

An opt-in coordinator or runner can check declared receipts before treating required gates as closed:

```text
python3 scripts/check-acceptance.py MANIFEST RECEIPTS --candidate-sha FULL_SHA --candidate-ref REF --evidence-root DIRECTORY
```

The independently supplied candidate SHA is 40 or 64 lowercase hexadecimal characters. The ref is an exact label. Inputs are UTF-8 JSON, at most 2 MiB each. The following synthetic example requires one browser gate:

```json
{"schema_version":1,"target":"Demo app","required_gates":[{"id":"browser","kind":"full_e2e","suite":"Full browser suite"}]}
```

The separate receipts file has this shape; use the real SHA-256 of the nonempty artifact bytes:

```json
{"schema_version":1,"receipts":[{"gate_id":"browser","target":"Demo app","kind":"full_e2e","suite":"Full browser suite","candidate_sha":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","candidate_ref":"refs/heads/demo","status":"PASS","exit_code":0,"artifact_path":"browser.log","artifact_sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}]}
```

Fields are exact; unknown fields, duplicate keys and duplicate IDs are invalid. IDs are lowercase ASCII kebab-case starting with a letter, at most 64 characters. Target, suite and ref are nonblank single-line labels of 1–200 Unicode codepoints without controls or surrogates; comparisons are exact. Kinds are `lint`, `typecheck`, `unit`, `component`, `mocked_e2e`, `full_e2e`, `integration`, `build`, `repo`, `review`, and `other`. No kind substitutes for another. Every receipt must name a required gate; every required gate must have a matching receipt. `PASS` requires integer exit code 0 and an artifact; `FAIL` requires a nonzero integer; `SKIPPED`, `NOT_RUN`, and `PENDING` require null exit code. Nonpassing records may have both artifact fields null; any supplied pair is validated.

Artifact paths are relative to the evidence root, with no empty, dot, dot-dot, backslash or symlink components. The root itself may be a symlink. Artifacts must be nonempty regular files matching their lowercase 64-hex SHA-256. The helper reads and hashes evidence without executing commands or writing files; it is not designed to defend against concurrent malicious filesystem changes.

Exit 0 and `EVIDENCE_CONSISTENT` mean the provided claims match; exit 1 and `EVIDENCE_INCOMPLETE` mean a required gate is missing, nonpassing, or differs in scope or candidate; exit 2 and `INVALID_INPUT` mean the input or artifact is invalid. Invalid input takes precedence over incomplete evidence. Output is static JSON and does not echo input. This is not automatic enforcement or proof of execution, authenticity, coverage, Git state, acceptance, or release readiness. The coordinator must establish manifest completeness, truthful labels and provenance, reconcile canonical test collection, and independently verify the actual committed candidate and clean state.
