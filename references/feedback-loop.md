# Feedback loop

## Contents

- Storage and privacy
- Capture
- Review trigger
- Consolidation
- Session close


The skill improves from evidence, not impressions. State lives next to
`SKILL.md`: `feedback/log.jsonl` (append-only raw events), `feedback/SUMMARY.md`
(short digest read at session start), `feedback/archive.jsonl` (consumed
entries). `feedback/` is gitignored: raw lessons may contain project specifics
and never leave this machine — only distilled, generalized rules enter the
versioned skill files (never published without owner approval).

Treat traces as improvement data, not context to retain wholesale. Preserve
the decision, tool outcome, error, and repeated sequence needed to explain a
failure; omit routine transcript bulk. A repeated sequence first becomes a
realistic eval, then — when the successful path is judgment-free — a
deterministic helper or gate. A prompt or workflow that has not passed that
eval remains a hypothesis.

### Capture

The moment a trigger fires — verifier rejection, user correction, routing
escalation, spec defect, blocked task, or a reusable pattern — append one
record through the bundled validator:

```text
python3 <this-skill-dir>/scripts/feedback-log.py append --record-json '<one-line JSON>'
```

The JSON shape is:

```json
{"date":"YYYY-MM-DD","project":"<slug>","task":"T<n>","category":"verifier_rejection|user_correction|routing|spec_defect|blocked|pattern","issue_key":"<stable-slug>","observation":"<what happened>","lesson":"<what should change>","rule":"<optional: concrete rule text>","session_id":"<stable originating session id>","status":"new"}
```

The helper rejects malformed records and variant categories, locks the shared
file, appends one canonical line, flushes it, and verifies the write. Never
edit or replace `log.jsonl` from a read snapshot: concurrent orchestrators
share it, so read-modify-write can truncate peer events.

For new records, include the originating head session's stable opaque
`session_id` when available. Reuse it across that session's tasks, workers,
and retries; do not invent a fresh ID per event or use a private path as an ID.
The field remains optional for older writers and unavailable provenance.
Missing IDs mean unknown session identity, never distinct sessions by default.

`issue_key` is the clustering handle — reuse the same slug for the same
underlying issue so repeats become countable evidence. When no narrower
category fits, use `pattern` and preserve the original event label inside
`observation`. Every write into a SECTIONED document — a dossier, PLAN.md,
SUMMARY.md — uses an anchored edit at the target heading; positional append is
reserved for the validated feedback helper.

Audit before counting or consolidating with:

```text
python3 <this-skill-dir>/scripts/feedback-log.py audit
```

Malformed records and exact duplicates fail the audit. Investigate provenance
warnings before using session or date claims. The auditor does not rewrite the
journal.

### Review trigger

At session start (after reading SUMMARY.md and auditing the journal) and again at session close,
consolidation is due when any issue_key has ≥2 entries from ≥2 different
sessions, or ≥5 entries have `status:"new"`, or the user asks for it. When
due, propose it in one line and run on confirmation — never silently rewrite
your own operating rules. **To run a consolidation, read
`references/consolidation.md` first** — it holds the promotion gate, the
smallest-surface and privacy rules, the disposition mechanics, the
consolidation DoD, and the self-modification-classifier exception for editing
SKILL.md itself.

### Session close

The loop closes at the end of every session, not at the start of the next one.
Before the final report:

1. **Audit.** Run `feedback-log.py audit`; resolve malformed/duplicate records
   before using counts, and call out provenance warnings.
2. **Sweep.** Audit the session against the capture triggers and append
   anything missed to `log.jsonl`. "Nothing to log" is valid only when no
   trigger fired.
3. **Digest.** If anything was appended this session, refresh the
   pending-clusters list in `SUMMARY.md` (≤30 lines: issue_key, count,
   one-line lesson). SUMMARY is derived state — the orchestrator updates it
   directly, no pipeline.
4. **Trigger check.** If the review trigger is met, propose consolidation in
   the final report as one line naming the top clusters; run it on
   confirmation — this session if budget allows, else first thing next
   session.
5. **Report.** The final report names the feedback outcome explicitly:
   entries logged (by issue_key) or "no feedback events this session".
   Closing a session with pending work in `feedback/` and no mention of it
   is itself a process failure.
