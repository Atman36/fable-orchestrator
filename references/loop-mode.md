# Loop mode (recurring / scheduled runs)

Read this file before creating, scheduling, or resuming any standing job —
a queue drained task-by-task, or a check re-run on a schedule until a
condition holds (`/loop`, `/goal`, cron, event triggers **only when verified
in the current host**). A slash command mentioned in a guide is not a
portable platform feature; read `references/execution-backends.md` first.

The one-shot pipeline's division of labor is unchanged, just recurring:
**the head owns the queue/specs/gates, a verified executor runs one bounded
round, independent checks decide, durable state records.** Use a cheaper
model for routine rounds only after proving its tools and DoD reliability;
otherwise keep a stronger/synchronous executor. The orchestrator follows
recorded state transitions rather than re-planning every round.

## The five mandatory parts

A loop needs all five, or it either never stops or never learns:

1. **Schedule / trigger** — an observed, supported host mechanism (manual
   in-session execution, configured cron/CI/event or an authorized cloud
   automation). A days-long or laptop-off run requires an actually running,
   durable host and tested restart/notification behavior; do not promise it
   from a local session or from a `/loop` or `/goal` name alone.
2. **One change per round** — fix the single most important thing found, never
   everything at once; one round = one small, reviewable diff.
3. **The same check every round** — a fixed, falsifiable gate (exit code + diff
   + the check commands), so this round is comparable to the last and the
   agent's self-report decides nothing (see "Done is proven" in SKILL.md).
4. **Durable one-writer loop state** — a loop-owned state file or an
   equivalent verified host state store, not both competing as authorities.
   A round reads it at start so completed work is not redone; only the
   coordinator updates progress. The round cannot promote its own output
   into steering memory without review.
5. **A hard stop** — a cap on rounds/attempts, a spend cap, and an explicit
   definition of *done* and *blocked* that fits the loop's job: an improvement
   loop stops at a target metric or the done-check passing; a discovery/audit
   loop stops after N consecutive rounds surface nothing new (until-dry). A
   model that never tires never stops on its own, and this is the most
   expensive model to leave running.

A standing loop must REMOVE decisions from the owner, not add an object to
supervise. If its rounds produce output nobody reads or acts on, the answer is
to delete the loop, not to tune it — ask that question at every review, and
report the answer honestly: an automation kept alive out of sunk cost consumes
the exact resource (attention) it was built to free.

## Tier routing and dry runs

Route every round through the Autonomy tiers: green rounds may run unattended
**only** on a proven runner, yellow rounds stop at a task branch/draft for a
human, and red rounds never fire without per-action authorization. Run any new
loop once by hand, including one failed-check scenario and its stop path, and
read the durable state before putting it on a schedule. Do not create a second
board when a backend already provides auditable single-owner task state.

## Classifier refusals

In an unattended loop a **classifier or safety refusal is a distinct terminal
outcome**: record it and stop the affected round. Do not route to another
model to bypass a refusal. A clearly technical model-unavailability error may
use an already-authorized equivalent route after a capability smoke; a safety
refusal requires changing the request to permitted work or human review.

A **production env mutation is red even when a goal-pack orders it**:
headless runners may reject user-authorized writes as well. Do not assume a
particular classifier or bypass it. Gather read-only evidence when permitted;
for the specific change require the user's explicit action/approval through
a supported permission path, and verify its *effect*, not the attempt.

## When the user pivots mid-run

If the **active host** actually exposes a `/goal` Stop hook and the user
orders early wrap-up, follow that host's verified goal-clear procedure and
record the handoff. Never assume `/goal clear` exists in Codex, Claude Code,
Orca or any other shell merely because another installation exposes it.
A user stop always overrides the loop; cease new dispatch and preserve state.

## External runners (a kernel between you and the executor)

When a job uses an external/programmatic runner, verify its actual policy
kernel (if any): paths, quotas, watchdogs and rollback rules. Reconcile the
spec with those rules BEFORE dispatch; do not assume the runtime even exposes
a built-in Agent tool or that a third-party runner automatically isolates work:

- **Launch lifetime** — before dispatching an external worker, the head
  applies the long-check lifetime contract in `references/pipeline.md` §
  Dispatch to the launch itself. Record the effective host/job deadline and
  worker CLI time bound separately; demonstrate launcher → worker → report/exit
  completion with a harmless probe through that same launcher. A worker's
  internal gate timeout does not prove its parent launch can survive it.
- **Forbidden paths** — enumerate the runner's global/kernel forbidden paths
  and reconcile them against every file each spec orders changed; a
  spec-mandated file on the forbidden list needs an explicit pre-dispatch
  workaround decision, not a mid-run surprise.
- **Task-scoped allowed paths** — derive the minimum paths for the task's
  own change **and its evidenced consumer-test cascades**. Include shared
  contracts when the task genuinely owns them, but never grant every sibling's
  union just to make parallel jobs pass policy; serialize overlapping tasks.
  Unexpected edits outside this bound stop for re-scoping, not silent policy
  expansion.
- **Exit code is a claim** — verify a gate command's exit code in isolation
  (`echo $?` immediately) against the documented baseline before freezing it
  into a manifest: a compound command's outer exit can come from `tail`, not the
  test runner, and a runner like `node --test` exits non-zero on accepted
  cancelled/flaky tests — gate on parsed pass-counts when the suite has any.
- **Cost/attempt caps** — an adapter under subscription auth may report
  notional cost rather than chargeable usage. Never claim it enforces a spend
  cap that it cannot measure. Use an enforceable maximum of rounds, calls,
  wall time and permitted actions; if paid exposure cannot be bounded, do
  not schedule unattended paid work. Retain any supported hard quota gate.
- **Disk pressure** — a full disk silently corrupts the runner's rollback
  artifacts (a truncated `diff.patch`), and a policy-failed task leaves no
  commit, so that patch is the only record: check free disk before every
  dispatch and PAUSE below the disk guard rather than salvaging post-rollback
  (treat any such patch as lossy — `git apply --check`). Free disk only from
  exact, reviewed targets with the required owner approval. Package-manager
  cache commands may purge **shared, out-of-repo data** and are not implicitly
  safe cleanup. Rollback patches have also truncated with disk
  headroom present: treat them as lossy, period — verified local task
  commits and reviewed snapshots are recovery artifacts; **a push is never
  a recovery shortcut without separate owner authorization**. Never plan
  salvage around a rollback patch.
- **Kill triage** — a killed run with 0-byte captured agent output, zero
  changed files, and an awake machine is a runner capture defect (environment
  failure): resume without advancing the escalation ladder; after two
  consecutive capture-blind kills on the same task, stop retrying and run that
  task with an in-session executor instead. Machine sleep suspends the
  adapter's timeout timer and the wake-time kill of a likely-finished agent is
  also an environment failure — dispatch long runs only while the machine will
  stay awake.
