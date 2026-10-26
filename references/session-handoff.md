# Head-to-head session handoff — evidence and ownership

Read this when one coordinating head gives way to another. This is a **protocol
for safe manual handoff and traceable state**, not an installed leader-election
service. The skill, an ACK file, a launch receipt and a timestamp alone cannot
revoke an old head's write permission. If the runner cannot enforce exclusive
ownership, require an operator-mediated stop/confirmation before the new head
mutates or dispatches work. Default to manual transfer; never silently enable
auto-takeover.

## Human handoff — always current, never a transcript

Rewrite `<taskdir>/NEXT-SESSION.md` on each handoff (do not append history),
or the project's established equivalent outside Git. Use four blocks:

```markdown
# NEXT-SESSION — <project> — <date>
## Done         — task IDs, outcomes and measured commit SHAs
## Remaining    — priority queue, blockers and next acceptance gate
## Branch       — repo/worktree, branch, verified HEAD, dirty paths,
                  unpushed commits and any live write-capable agents
## Next command — exact first CLI command and paths to active specs/PLAN
```

Report the same four blocks briefly to the operator. Base facts on this
session's tool outputs, not inherited claims. Keep outdated history in the
journal, never in NEXT-SESSION.md. Do not commit taskdir files unless the
project has explicitly adopted tracked handoffs.

## Machine-readable snapshot (file-backed runs)

If the verified backend already exposes **authoritative** owner/task state,
store equivalent fields there and link to its immutable receipt rather than
creating a competing state authority. Otherwise write `<taskdir>/STATE.json`
for the transfer, alongside `NEXT-SESSION.md`. `STATE.json` is a frozen
*projection* of PLAN.md / task evidence, not a second queue or a lock.

Example schema v1 (the values below are illustrative, not observed facts):

```json
{
  "schema_version": 1,
  "handoff_id": "s80-to-s81",
  "generation": 80,
  "outgoing_head": "head-s80",
  "git": {
    "repo_root": "/absolute/repo/path",
    "branch": "feature/work",
    "head_sha": "0000000000000000000000000000000000000000",
    "checked_at": "2026-10-26T08:00:00Z"
  },
  "next_task": "T12 independent acceptance",
  "blockers": [],
  "checks": [{"command": "npm test", "result": "PASS", "checked_at": "2026-10-26T08:00:00Z"}],
  "workers": [{"id": "worker-7", "write_capable": true, "status": "stopped"}]
}
```

Include every known live, stopped or uncertain worker and the venue it can
write to in the real snapshot (add fields as needed). A missing record does
not prove no workers exist. The `generation` is descriptive unless assigned
atomically by a shared coordinator; do not infer a fencing token from it.
Report independently measured SHA, branch and test commands/results; do not
carry test `PASS` forward as verification at a newer HEAD.

## Transfer: PREPARE → RELEASE → CLAIM → ACK

1. **PREPARE (old head):** stop creating new assignments, record pending
   work, inspect live write-capable heads/workers on all known venues,
   drain/cancel them via their **verified** backend or explicitly park the
   transfer. Re-measure repo root, branch, HEAD, dirty paths and key checks
   after the last mutation. Rewrite NEXT-SESSION and STATE atomically in
   taskdir; compute SHA-256 of the final STATE and NEXT-SESSION bytes.
2. **RELEASE (old head):** write `<taskdir>/RELEASE.json` containing
   `handoff_id`, `generation`, `state_sha256`, `next_sha256`,
   `released_by`, `released_at`,
   `status: "RELEASED"`. Once released, the previous head MUST NOT start
   workers, write the task board/specs or mutate the project. Its only
   allowed remaining work is communicating the frozen handoff. If it
   subsequently changes any artifact, invalidate RELEASE and start over.
3. **CLAIM (new head):** before any dispatch, read NEXT-SESSION, STATE,
   RELEASE and the active task board. Verify both snapshot checksums, actual Git
   repo/root/branch/HEAD, dirty worktree, live worker registry and any
   conflicting project writers. If HEAD or ownership differs, write a
   blocked receipt and stop for reconciliation; never silently substitute a
   new SHA or kill an unknown agent.
4. **ACK (new head):** only after exclusive authority has been confirmed
   by the installed runner's *enforced* ownership check OR by an explicit
   operator-supervised manual handoff, write `<taskdir>/ACK.json` with
   `handoff_id`, `generation`, `state_sha256`, `next_sha256`,
   `accepted_by`, `accepted_at`,
   `status: "ACCEPTED"`, `observed_branch`, `observed_head_sha` and the
   observed remaining workers/conflicts. Only then can new writes/dispatch
   begin. A rejected or absent ACK is a failed transfer, not success.

For local files use `shasum -a 256 STATE.json` on macOS or Python hashlib.
A shipped `scripts/handoff-validate.py` checks JSON cross-references,
STATE and NEXT-SESSION checksums and current Git branch/HEAD; run it with `--phase release` before
publishing the handoff and `--phase ack` after writing ACK. **A passing
validation checks a snapshot, not worker liveness or exclusivity**.

## Implementing enforced ownership (separate runtime work)

A reliable automatic transfer requires a common authority with atomic claim
(CAS or process-held OS lock) **and** preventing a stale owner or its workers
from writing after takeover. Check owner generation / fencing token at
side-effect boundaries (dispatch, write, commit, external actions). Ensure
writers cannot bypass that check. A TTL file or Lease expiration without
fencing is not proof that the old process stopped. Plain read/write of a
JSON lock file is not atomic acquisition; a `flock` held only while a CLI
check runs is not a session-wide lock. Never delete a "stale" lock using
age alone. A file-lock on one Mac does not by itself protect remote workers
or external databases. Do not install Kubernetes, Temporal or a new daemon
just to support this handoff without a demonstrated requirement.

On crash, unclear ownership, orphan workers, changing release files, absent
ACK, or failed checksum/HEAD validation: **STOP** new writes, preserve all
artifacts, report one precise blocker and request manual reconciliation. Do
not silently take over on a timeout. This fail-closed route is the supported
behavior until a real ownership adapter and fault-injection tests exist.
