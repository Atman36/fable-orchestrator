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

The documented task wire schema carries no per-spawn model for ordinary
agents; precedence is `task.agentModelOverrides[<agent>]`, then the agent's
frontmatter `model`, then the parent's model. Check the installed task schema
first. When it offers no usable per-task model, route one spawn through a
temporary override:

1. Read and record the current `task.agentModelOverrides` value.
2. Set the session-only override for that agent name (a settings write needs
   the owner's approval; never persist it).
3. Spawn exactly the dispatches that need the route.
4. Restore the recorded value immediately after the spawn.
5. Ledger the requested route and the child's self-reported model.

A blanket override left active reroutes every later spawn of that agent: one
owner-requested reviewer model silently became the route for all reviewers.

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
