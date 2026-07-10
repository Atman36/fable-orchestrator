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
