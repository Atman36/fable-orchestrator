# OMP supervision and session controls

Read when considering an OMP advisor, reviewer priorities, event hooks, a
per-spawn model pin, persisting a read-only worker's report, or context
compaction. Confirm the installed version supports the documented interface.
Use features within the task's authorized provider, model and budget; this
reference alone authorizes no configuration change, installation or external
data transfer.

## Advisor during execution

Use an advisor selectively for long or risky work where early feedback can
prevent rework. It makes separately billed model requests and receives session
material, including main-agent reasoning and tool activity. Verify provider
permission, available model and effective state with `/advisor status` before
relying on it; bare `/advisor` toggles state. Keep investigative tools read-only.
The head verifies notes against evidence and retains decisions and approvals.
Because the advisor sees the implementation trajectory, treat it as ongoing
supervision; retain acceptance and final review from a fresh context. An absent,
lagging or failed advisor is not a clean verdict.

## Separate reviewer priorities

When reviewer setup is requested, inspect existing project guidance and use
`WATCHDOG.md` for a short list of concrete architectural boundaries, recurring
failure modes and required evidence. These instructions guide advisors without
being copied into the main agent's ordinary context. Preserve existing rules;
use `WATCHDOG.yml` only when a specialist roster is justified, and confirm the
effective roster with `/advisor status`. Read-only review needs no write tools.
Keep priorities scoped to the task and verify loaded guidance rather than
assuming the nearest file replaces inherited guidance.

## Event hooks for deterministic checks

Prefer existing project checks for repeated, judgment-free restrictions. If OMP
hook setup is requested, bind the installed extension API's actual event and
filter the tool explicitly: the `pre/` and `post/` directory names do not select
an event or tool. A pre-call guard can block a prohibited action; result handlers
can redact output; lifecycle handlers can run checks and retain their evidence.
Hook code runs with the user's privileges. Load trusted code only and inspect
the effective extension set through `/extensions`; do not run an installer just
to obtain these features. Verify each guard in a disposable fixture with an
allowed control and a denied control proving zero prohibited effects. A loaded
hook or completed turn is not a passing gate: record the real check result and
stop dependent work on failure. Hooks preserve the task's approval boundaries.

## Per-spawn model routing

Read the active task schema before selecting a route: hosts differ on whether
ordinary agents accept a per-call `model`. Where supported, use an exact
approved pin only when it does not conflict with that agent's
`task.agentModelOverrides` entry. A rejected pin starts no worker; stop that
dispatch and report the conflict, never silently substitute a configured model.
Check each agent type separately, including `security-reviewer`; a task or
reviewer override says nothing about another specialist's route.

When no usable pin exists, use a configured route only if it is confirmed
approved for the task. Otherwise obtain an owner-approved session-only routing
change, preserving and restoring the exact prior value immediately after the
intended spawns; never persist it or leave a blanket override active. Inspect
settings only through an authorized host interface. A routing workaround does
not change role capability: mechanical agents remain mechanical, not general
executors chosen merely because their pin is accepted.

Ledger the requested route, host-confirmed effective route and child's reported
identity separately; unavailable evidence is `unknown`, not the requested name.
Runtime model changes are recorded per phase, not rewritten as one head model.

## Served service tier

Before billed fan-out, establish the requested and effective service tier for
each role from available host receipts or usage evidence. Configured or
requested speed is not proof of the served tier: record the observed tier per
dispatch, or `unknown` when the host provides no receipt. Tier names and their
prices are host-specific; a Fast/priority request on one host establishes
neither support nor cost on another. Retain the owner's model and cost gates.

An owner usage counter disagreeing with the ledger is evidence of a discrepancy,
not a reason to dismiss the counter. Report it and stop further billed dispatch
until the routing/tier is resolved or the owner authorizes proceeding with the
stated uncertainty. Do not change settings or buy a faster tier to diagnose it.

## Persisting read-only reports

A reviewer or scout without write tools returns its report as final output.
Persist it verbatim with `cp agent://<id> <taskdir>/reports/<agent>.md` in
the shell (internal URLs resolve as paths there), then confirm the file
exists and is non-empty before releasing the agent. Do not grant write tools
for this.

## Context compaction

The head cannot compact its own context. `/compact [focus]` is a host command
the owner types; automatic compaction fires at the configured threshold
(`compaction.thresholdPercent` or `thresholdTokens`; reserve-based by default).
Tell the owner at session start, before it becomes urgent: either they run
`/compact` when the head asks, or they approve a session-only lower threshold
(e.g. 40%) so the head compacts early. Rewrite `NEXT-SESSION.md` before any
compaction. Live subagents kept running and delivering results across an
in-session compaction; prefer it over a relay to a new head while
write-capable workers are live, since a relay must drain them first.

Sources (checked 2026-10-23; installed-docs sections 2026-10-28):
- https://omp.sh/docs/advisor
- https://omp.sh/docs/hooks
- installed OMP docs `task-agent-discovery.md` (model precedence) and
  `compaction.md` (triggers, threshold settings)
- 2026-11-02 routing revision: active task-tool schema and local feedback;
  the web sources above were not rechecked for this revision.
