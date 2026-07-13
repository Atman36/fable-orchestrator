# Loop mode (recurring / scheduled runs)

Read this file before creating, scheduling, or resuming any standing job —
a queue drained task-by-task, or a check re-run on a schedule until a
condition holds (Claude Code's `/loop` and `/goal`, cron, event triggers).

The one-shot pipeline's division of labor is unchanged, just recurring: **the
head creates the key files, a cheap model runs the routine rounds,
deterministic checks decide, git records.** The head's spend goes into the
durable artifacts — the task queue/manifest, the per-task specs, the curated
cross-run lessons file — never into the repeated rounds. A round a cheap model
can drive is never a head round; the head steps back in only for a round the
cheap model failed (a logged escalation) or to revise a key file. The
orchestrator itself stays deterministic: it routes, checks, and records — it
does not think each round.

## The five mandatory parts

A loop needs all five, or it either never stops or never learns:

1. **Schedule / trigger** — when a round fires: a manual in-session loop
   (`/loop`), a cron schedule, or an event (a CI failure, a new PR). A
   days-long or laptop-off run belongs on hosted infra (a saved cloud routine),
   not a local session that dies when the terminal closes.
2. **One change per round** — fix the single most important thing found, never
   everything at once; one round = one small, reviewable diff.
3. **The same check every round** — a fixed, falsifiable gate (exit code + diff
   + the check commands), so this round is comparable to the last and the
   agent's self-report decides nothing (see "Done is proven" in SKILL.md).
4. **A loop-owned state file** — what was done and what's queued next, read at
   the start of every round so finished work is never redone. A round *reads*
   it but may not rewrite it; promotion into the steering memory is a
   human/loop decision, not something a round self-serves.
5. **A hard stop** — a cap on rounds/attempts, a spend cap, and an explicit
   definition of *done* and *blocked* that fits the loop's job: an improvement
   loop stops at a target metric or the done-check passing; a discovery/audit
   loop stops after N consecutive rounds surface nothing new (until-dry). A
   model that never tires never stops on its own, and this is the most
   expensive model to leave running.

## Tier routing and dry runs

Route every round through the Autonomy tiers: green rounds run unattended,
yellow rounds stop at a branch/draft for a human, red rounds never fire without
a per-action authorization. Run any new loop once by hand and read the state
file it writes before putting it on a schedule.

## Classifier refusals

In an unattended loop a **classifier refusal is a distinct outcome, not a
failed round**: route that round to Opus and log it, never silently retry it on
Fable or spend the attempt cap on it — a refusal that reads as a generic
failure becomes a silent regression that costs you at debug time.

A **production env mutation is a red action even when a goal-pack orders it**:
the auto-mode classifier blocks the write and reads "record blocked items" as
no-prod-writes. Verify the read-only form first, then hand the exact command to
the owner as a checklist item — never spend attempts retrying it.

## When the user pivots mid-run

When the user orders an early wrap-up mid-`/goal`, the Stop hook keeps firing
until the goal clears — name `/goal clear` in the SAME message, keep every
subsequent hook-round reply to 2-3 sentences (no re-reporting), and author goal
conditions with an explicit user-override clause ("…or the user closes the
session early") so the hook can satisfy on a recorded handoff.

## External runners (a kernel between you and the executor)

When any job — standing loop or one-shot pipeline — dispatches specs through
an external/programmatic runner instead of the built-in Agent tool, the runner
interposes a kernel with its own path allowlists, cost caps, watchdogs, and
rollback artifacts — reconcile each spec against the kernel BEFORE dispatch,
or the runner silently rolls back healthy work:

- **Forbidden paths** — enumerate the runner's global/kernel forbidden paths
  and reconcile them against every file each spec orders changed; a
  spec-mandated file on the forbidden list needs an explicit pre-dispatch
  workaround decision, not a mid-run surprise.
- **Allowed-path union** — sibling tasks sharing a surface (a doc section, a
  config file) each get the UNION of that surface in their allowed paths; derive
  the globs from the shared category, never hand-scope per task, or the second
  task policy-fails on the shared file. The union includes the CONSUMER-TEST
  dirs of every contract or behavior the task changes: an accept/reject or type
  change cascades into test fixtures that construct or assert it, and globs
  scoped to the primary module dir policy-fail that healthy cascade.
- **Exit code is a claim** — verify a gate command's exit code in isolation
  (`echo $?` immediately) against the documented baseline before freezing it
  into a manifest: a compound command's outer exit can come from `tail`, not the
  test runner, and a runner like `node --test` exits non-zero on accepted
  cancelled/flaky tests — gate on parsed pass-counts when the suite has any.
- **Cost caps** — under subscription auth the adapter's reported cost is
  notional; omit a max-cost cap in manifests, or the default policy-fails
  healthy tasks.
- **Disk pressure** — a full disk silently corrupts the runner's rollback
  artifacts (a truncated `diff.patch`), and a policy-failed task leaves no
  commit, so that patch is the only record: check free disk before every
  dispatch and PAUSE below the disk guard rather than salvaging post-rollback
  (treat any such patch as lossy — `git apply --check`). Free disk with
  project-local and package-manager-native cleanup only (`npm cache clean`,
  `pip cache purge`, `pnpm store prune`); deleting caches outside the project
  dir is an owner action. Rollback patches have also truncated with disk
  headroom present: treat them as lossy, period — WIP commits and pushed
  branches are the only reliable work artifacts; never plan salvage around a
  rollback patch.
- **Kill triage** — a killed run with 0-byte captured agent output, zero
  changed files, and an awake machine is a runner capture defect (environment
  failure): resume without advancing the escalation ladder; after two
  consecutive capture-blind kills on the same task, stop retrying and run that
  task with an in-session executor instead. Machine sleep suspends the
  adapter's timeout timer and the wake-time kill of a likely-finished agent is
  also an environment failure — dispatch long runs only while the machine will
  stay awake.
