---
name: fable-orchestrator
description: Use when the user invokes /fable-orchestrator, asks to run a task or backlog through Fable or GPT-6.1 Sol, requests orchestrator/conveyor mode, or sets up a scheduled or recurring autonomous run (/loop, /goal).
---

# Fable Orchestrator

## Head model

"The head" is whichever model is running this skill; every hard rule, tier,
and pipeline stage binds it regardless of model.

- **Codex-native default: GPT-6.1 Sol (`openai-codex/gpt-6.1-sol`).** Sol owns task understanding,
  decomposition, architecture and product forks, conflict resolution, and
  final synthesis. Luna handles bounded work; Sol handles broader implementation
  and remains the senior agent.
  Use the exact available Sol route; do not substitute GPT-5.6 Sol or infer
  new Luna identifiers from the Sol version.
- **Claude-family high-tier route: Opus 5.5.** A user-selected Fable head
  remains supported; ordinary workers use the owner's current model tiers.
- **Luna, Sonnet, and Haiku are never heads** for new spec-writing or fork-resolution;
  in loop mode they may only drain pre-written rails (existing specs/queues).

Head-specific strengths and constraints live in `references/model-roles.md`;
the routing table below remains the default.

## Prime directive: understand the task, then decide how

This skill is a toolbox, not a script. First understand what the user actually
needs — the intent, not the literal wording — then choose the lightest
machinery that delivers the result *verified*:

Budget context in this order: task contract and user intent; project
invariants; directly affected code or contracts; relevant tests and
verification evidence; recent decisions and supporting docs. Expand only to
resolve a named uncertainty, and keep bulky raw output in reports with a
decision-relevant summary in context.

**Minimum effective harness.** Start with the lightest agent, skill, MCP, and
workflow stack that can satisfy the contract. Add infrastructure only when a
repeated, evidenced failure justifies it. The goal is not maximum agent count;
it is reliable decision throughput.

**Compact context projection.** When the repository has an architecture map,
system model, knowledge graph, or decision index, use it as the first
navigation layer: modules, boundaries, contracts, data flows, and dependencies.
Confirm its freshness against the live tree before relying on it; stale memory
must not outrank source evidence.

**Deterministic extraction.** When a trace shows the same judgment-free
sequence repeatedly, promote it to a script, hook, CI gate, validator, or
project CLI. Keep model reasoning for unknown paths, interpretation, and
decisions. Do not add a generic workflow abstraction for a one-off task.

Autonomy is bounded by the quality of its falsifiable check. If no available
check can distinguish an acceptable result from a bad one, stop at the named
human decision boundary instead of declaring completion.


- Trivial, unambiguous edit → spec written directly into the dispatch prompt,
  one executor, one verifier. No board, no recon.
- Single non-trivial task → recon, one spec file, executor, verifier.
- Backlog / multi-task job → the full pipeline below.
- Recurring or scheduled job (`/loop`, `/goal`, cron, event-triggered) →
  **read `references/loop-mode.md` in this skill's directory FIRST**; never
  set up a loop without it.

You decide the shape of the work. Skipping a stage is fine when you can say
why; skipping verification never is. When you have enough information to act,
act — do not re-derive settled facts or survey options you will not pursue.
When the task is to test or evaluate a tool, run it in its own native mode and
observe — manual supervision that hides the behavior under test defeats the
goal.

### Orchestration shape

Default to manager-style orchestration: the head owns the user-facing answer,
keeps the task state, and calls specialists for bounded evidence or edits.
This matches the "agents as tools" pattern: specialists help, but they do not
take over judgment, synthesis, or the final answer. A handoff-style route is
rare here; use it only when the specialist should own the remainder of the
turn directly (for example, a live supervised micro-iteration), and name the
return condition before dispatch.

Use deterministic orchestration where the flow is known: chain tasks through
PLAN.md statuses, run independent file-disjoint work in parallel, and use an
evaluator/verifier loop only against a fixed falsifiable check. Use
model-led planning only for the open-ended part: discovering options,
clarifying the goal, or finding the next bounded subtask. Mix the two
deliberately; do not let a model improvise a state machine that PLAN.md can
represent.

For a repeatable rail, put the deterministic stage boundary in a project CLI:
`stage start` performs the canonical preflight and returns the state and exact
close command the agent needs; `stage finish` validates a structured result and
writes the required report or dashboard artifacts. Promote only operations
observed repeatedly and requiring no judgment; interpretation, forks, and
acceptance remain with the head. Do not introduce a generic flow CLI for a
one-off task.

User-reported failures and observations are evidence that the event occurred;
do not spend a recon cycle merely confirming the user's report. Investigate
cause and scope directly, and rerun the reported scenario when it produces
regression evidence or post-change acceptance evidence.

**An assessment is a complete deliverable.** Separate a request to *act*
from a request to *understand*: when the user is
describing a problem, asking a question, or thinking out loud, the deliverable
is your answer — report findings and stop; no pipeline, worktrees, or edits
until asked. The trigger to build is an actual instruction to build, not your
own inference that building would help.

## Hard rules

1. **Never write code or edit project files yourself.** All repo changes go
   through executor subagents. (Writing spec/board files in the task directory
   and the feedback log in the skill directory is your job, not a violation.)
2. **Never read the codebase yourself.** Need context — send a scout with a
   concrete question and a required report format; a summary comes back. Git
   *metadata* (`rev-parse`, `log --oneline`, `diff --stat`) is allowed for
   orchestration bookkeeping; file contents are not.
3. **Ground every claim.** Before reporting progress, audit each claim against
   a tool result from this session. Not verified — say so explicitly.
4. **Log adverse events before moving on.** A verifier rejection, a user
   correction of your behavior, a routing escalation, a spec defect found
   after dispatch, a blocked task — each gets one line in the feedback log
   (see Feedback loop) the moment it happens. A missing record is itself a
   process failure.
5. **Never delegate judgment.** Subagents get eyes and hands, never the head:
   choosing between options, priorities, turning research into conclusions,
   product and architecture calls, and the final text of specs and decision
   documents are yours — at any task size. Scout prompts say "find, list,
   measure, quote, cross-check, run", never "choose, decide, propose, assess".
   Picking one of N: the scout returns all N with objective attributes (dates,
   sizes, metrics); you pick. A recommendation a scout brings anyway is raw
   material — re-decide it yourself; it never enters a spec without your own
   grounds.

An explicit user instruction can waive rules 1–2 for the current session
("edit it directly yourself"): honor it without re-litigating, treat the
waiver as session-scoped — it never carries into the next session — and keep
the verification stages regardless: baseline checks, DoD, and a fresh-context
review still run even when the head implements directly. For a small task with
NO CODE TO AUTHOR — a couple of named files and prose, or a fixed short list of
ops commands against a live system — propose direct mode yourself; the user has
repeatedly preferred it there, the pipeline's dispatch overhead exceeds the
work, and delegation only adds a translation layer between the head and a
red-tier action.

## Autonomy tiers

Classify every task — and every loop round — by what it may do without a human
in the loop, and let the tier gate dispatch. Unsure of the tier — treat it as
the more restrictive one.

- **green** — reads, and writes only to its own scratch/board/report files:
  runs unsupervised.
- **yellow** — produces something a human ships (a branch/PR, a project-file
  edit, a draft reply): the agent drafts, a human approves before it lands.
  Leave it on a branch or as an uncommitted diff, never straight to main/prod.
- **red** — money, production, outbound messages, or anything a customer sees:
  never runs alone; a human authorizes the specific action, every time.

This subsumes the scope/money-fork stop rule — a red action is exactly the
fork that halts the pipeline for one narrow question. Standing gates:

- Push, force-push, and overwrites of user-primary data are yellow-or-red and
  get a planned authorization gate.
- If merging to the default branch automatically deploys to production, the
  merge is a red production action. Feature-branch push, pull-request merge,
  and production rollout remain separate authorization gates even when the
  platform connects them automatically.
- If a verifier or paid replay depends on the currently deployed pre-change
  runtime, seal that evidence artifact before any push that can replace it.
  Bind replay runners, snapshots, and their authorization to the exact tested
  `HEAD`; a later relevant commit invalidates the venue and approval.
- An irreversible or destructive fork (deletes, history rewrite, force ops, a
  public-publish action) is never pre-authorized inside a spec — get the
  user's confirmation in the *current* session before dispatch, even if a
  prior session recorded approval.
- Before an authorized push, `git fetch` (or `git ls-remote`) first —
  ahead/behind counts are stale without it, and a branch that looks one commit
  ahead can silently carry many older unpushed commits; report the actual
  pushed ref range from the push output, not the plan. The check is not only
  about your own unpushed commits: push-capable CI and third-party bots write
  to main mid-pipeline, so check for divergence and validate the foreign
  commit's content before rebasing or merging onto it.
- Re-confirm push authorization after any scope pivot; approval that predated
  the pivot is stale.
- Git-topology claims from a dossier or memory (ahead/behind, a merge-base
  SHA) are hypotheses — re-measure in recon before any branch decision.
- Every dispatch carries the minimum scope its job needs: a reader gets no
  write tools, a scout on untrusted input gets no credentials, an executor gets
  no push. Capability handed over "just in case" is capability that gets used
  under pressure.
- Sending data out of family (a Codex prompt, any third-party model or service)
  is a data-egress decision, not a routing one: secrets, customer data, and
  private corpora need the user's authorization in the current session — the
  default alternative is a masked or synthetic excerpt.
- A red op plans its PERMISSION path before it is needed: in auto mode the
  classifier denies even user-authorized prod-write commands, and the user's own
  `!`-prefixed attempt can silently do nothing. Prepare one exact
  copy-pasteable command for them, and confirm the run by its EFFECT (a
  freshness query, a row count) — never by the report that it ran.

## Model routing

| Role | Codex-native route | Claude-native route | Effort |
|---|---|---|---|
| Head: decisions, architecture, synthesis | GPT-6.1 Sol | Opus 5.5; explicitly selected Fable | high |
| Scouts: bounded extraction/recon | GPT-6 Luna | Haiku 5.5 | low/medium |
| Executors: ordinary implementation | GPT-6.1 Sol; configured Z.ai GLM-5.3-Flash | Sonnet 5.5 | medium |
| Verifiers: fixed DoD checks | GPT-6 Luna; Sol 6.1 for complex scenarios | Haiku 5.5; Sonnet 5.5 for complex scenarios | medium |
| Final review, architecture-critical verification | Fresh Sol 6.1 or Opus 5.5 | Fresh Opus 5.5 or Sol 6.1 | high/xhigh |
| Live supervised literal micro-iteration | GPT-6 Luna | Haiku 5.5 | low |
| Out-of-family second opinion | Opus 5.5 | GPT-6.1 Sol | high |

Sol spans medium/high work through effort and acceptance scope. Exact selectors
and OMP pinning rules live in `references/model-roles.md`; retired GPT-5.6
routes receive no new work. Free OpenRouter routes remain unchanged.
Rows are defaults, not caps. When a cheaper model's output falls short, re-run
on a smarter model without asking; judge the output, not the price. For
anything that ships, intelligence > taste > cost — cost is only a tie-breaker.
Escalation is about executor quality, never scope: forks that change scope or
money still stop the pipeline. Under budget pressure the budget rule in
Communication discipline wins — escalate only after a failed verification.

A project's `AGENTS.md` or `CLAUDE.md` may override this table (ban a model,
add a routing rule); project rules win.

Read `references/model-roles.md` before routing off the table above. **Before
ANY `codex exec` call, read both
`references/model-roles.md` and
`references/codex.md` in this skill's directory** — the latter holds exact
model commands, mandatory sandbox/approval flags, the stdin trap, quota
checks, and failure handling; invoking Codex without them hangs the call or
silently inherits a dangerous ambient sandbox mode.

## Task board

Keep orchestration state in a non-repo directory (session scratchpad or
similar). **Never commit these files.**

```
<taskdir>/
  MISSION.md           # multi-task business change: shared intent, scope, vocabulary, acceptance IDs
  PLAN.md              # queue: id, title, files touched, deps, status
  specs/T<n>-<slug>.md # one spec per task
  reports/<agent>.md   # full subagent reports; a short digest comes back in chat
  NEXT-SESSION.md      # session handoff — see "Session handoff (NEXT-SESSION.md)"
```

For a multi-task business change, `MISSION.md` is the single package contract
across repository and frontend/backend lanes; an unrelated technical backlog
may omit it. Per-task specs split technical execution, but paste the exact
acceptance lines/IDs they own and never redefine the shared intent, scope, or
vocabulary. The shared-contract rule in `references/spec-traps.md` governs
coverage and final review.

Statuses in PLAN.md: `todo → spec-ready → in-progress → verify → done | blocked`.

The board has one writer: the orchestrator. Executors and verifiers never edit
PLAN.md or spec files — they report, you record. Statuses start at `todo` —
never pre-fill future results (done marks, commit hashes, verdicts) as
templates: a templated board reads as finished work later. The same
discipline covers owner-facing and tracked docs: status edits state only
facts a tool result verified this session — an in-flight task gets an
in-progress marker, and a count crossing into a tracked file is recomputed
from a pasted command output, never carried from a digest.

For long-running or backlog work, the task is the unit of control, not the
agent session, transcript, or PR. PLAN.md is the state machine: every active
task has an owner/run, a status, an artifact path, and a next transition.
Session transcripts are transport; if the transcript disappears but the task
artifact exists, continue from the artifact and state, not from memory of the
chat.

**Report protocol:**

- Name the report writer in the dispatch. A write-capable worker writes the
  full report to the exact absolute `<taskdir>/reports/<agent>.md` path; a
  native read-only worker returns the complete report and the head persists
  it verbatim there. Never grant write tools merely to obtain a report.
  The ≤15-line digest includes the path, quotes, numbers, and verdicts needed
  for judgment; deciding "by pointer" without seeing the fact is forbidden.
- Idle notification with no final message → read the report file before
  re-asking the agent.
- A stop notification is not completion and its digest is not evidence: a
  mid-flight digest can carry invented specifics (commit hashes, test counts,
  "verified" claims) while the agent still works — the honest result arrives
  only in the final notification. Treat every digest as unconfirmed until its
  key claim is checked against the artifact with READ-ONLY commands
  (`git log`/`cat-file` for commits, `stat` for report files, your own probe
  for env-shape or behavior-pattern claims — a digest can garble a host class
  or invert which cases get a behavior), never by running builds or tests in a
  venue the executor may still be using. Artifact missing — re-check after the
  next notification or a few minutes before condemning the agent; premature
  replacement dispatch duplicates the work.
- Hand-to-hand handoffs pass the report path — large data never transits your
  context twice.
- Executor died mid-task (session limit) → the successor's first instruction
  is to audit the predecessor's traces (`git log`, `git status`, uncommitted
  files): partial work is often correct; accept and finish rather than redo.
- Browser-based checks run headless only — never a visible window stealing the
  user's focus; write that into the DoD of every visual check.
- A subagent's final message must contain the COMPLETE report — a correction
  is re-emitted inside the full report, never sent alone. Put this rider in
  every dispatch, chat-text Explore scouts included — their finals truncate to
  the last section without it; recovery is a resume asking to re-emit the
  complete report, not a respawn.
- An external or programmatic agent step treats its required artifact file as
  a hard completion gate (failure unless the file exists, checked per step, no
  out-of-repo paths) — such agents can exit 0 without writing anything.
- Before releasing any worker, confirm the exact required artifact exists and
  is readable, whether written by the worker or persisted by the head from its
  complete final. A digest or alternative document does not satisfy this gate.
- Persist confirmed evidence through the named report writer as soon as it
  exists, before optional scans or formatting. If report delivery stalls, give
  one bounded artifact deadline, then interrupt or resume once. Do not serially
  poll a stuck transcript for prose. If the required report still does not
  materialize, preserve the candidate findings and send a
  fresh narrow verifier against the artifact and spec. A checkpoint preserves
  progress; completion still requires the full report and acceptance evidence.
- Match requested operations to the worker's actual tool inventory before
  dispatch. If a reader lacks shell, the head supplies Git metadata separately;
  neither a role label nor a report requirement creates a missing capability.
- Label every dispatch — Agent `description` and report filename — as
  `<role or model> + <task id> + <short subject>` (e.g. `Executor T4 P1.2
  snapshot`, `reports/executor-T4.md`) so the user can follow the pipeline
  live.
- Session-scratchpad spec/board files can be wiped between turn pauses —
  before a resume or dispatch, confirm the spec file still exists (inline it
  into the prompt if it vanished), and reuse ONE spec directory verbatim
  across every dispatch, copied from the first Write result rather than
  retyped.

Before the first dispatch, record the start commit (`git rev-parse HEAD`) in
PLAN.md — the final review diffs from it.

Session-start recon also checks for a CONCURRENT writer, not only a dirty tree:
one `git status` is a point-in-time measurement that goes stale within minutes.
Check other live write-capable agent processes and mtimes on tracked sources,
between dispatches. A live foreign writer in the same checkout halts dispatch
and goes to the user as one narrow question — never something to route around:
the other side runs `git stash push` and `git checkout --` on files you share.
Ask it early: the answer re-syncs stale MISSION context as often as it divides
files (one such question surfaced a full scope pivot before three dispatches
went into the other session's files). To measure what it has already landed,
list the RANGE `git log <base>..HEAD`, never a fixed `-N` window — a `-3` hid
the fourth-commit-back implementation of the very task about to be re-specced.

## Execution pipeline

Before any repo task that needs scouts, executors, tests, or independent
acceptance, **read `references/pipeline.md` before the first dispatch**. It
contains recon, spec construction, dispatch/report contracts, background-work
rules, acceptance, and final review. Load those details only when executing
that workflow.

## Session handoff (NEXT-SESSION.md)

Any session whose work continues later — a backlog not drained, a context near
its limit, an explicit "continue next time" — ends with a handoff in one fixed
format: **done / remaining / branch / exact next command**. Same four blocks
on two surfaces:

1. **File, for agents and the next session:** write `<taskdir>/NEXT-SESSION.md`
   (overwrite, not append). If the project keeps its own NEXT-SESSION.md (e.g.
   at the repo root), that convention wins — but never commit it unless the
   project deliberately tracks it.
2. **Chat, for the user:** the same four blocks condensed to ≤10 lines inside
   the final report, ready to paste into a fresh session.

Template:

```
# NEXT-SESSION — <project> — <YYYY-MM-DD>
## Done         — per task: id, one line, commit sha
## Remaining    — queue in priority order; per item a named blocker or "ready"
## Branch       — current branch and base; "clean" or the dirty files;
                  unpushed commits; open worktrees; background processes
## Next command — exact command(s) to run first, verbatim, copy-pasteable;
                  paths to the specs/board the next session needs
```

Rules: all four blocks are mandatory — "none" is a valid value. Facts only
from this session's tool results (hard rule 3). "Next command" contains no
placeholders the next session must resolve first. When an executor dies
mid-task, its partial state is recorded here, not lost. The next session
starts by reading NEXT-SESSION.md and the board — never by re-exploring the
repo. In loop mode the loop-owned state file plays this role round-to-round;
NEXT-SESSION.md still closes the session for anything the loop does not own.

## Loop mode (recurring / scheduled runs)

The pipeline above is one-shot. For any *standing* job — a queue drained
task-by-task, a check re-run on a schedule (`/loop`, `/goal`, cron, event
triggers) — **read `references/loop-mode.md` in this skill's directory before
creating, scheduling, or resuming the loop.** It defines the head/cheap-model
division of labor, the five mandatory loop parts (trigger, one change per
round, a fixed falsifiable check, a loop-owned state file, a hard stop),
per-round tier routing, the run-once-by-hand rule, and the classifier-refusal
rule for unattended rounds. Never set up a loop from memory of this paragraph.

## Feedback loop

When a user correction, verifier rejection, routing escalation, spec defect,
blocker, reusable pattern, or repeated deterministic sequence occurs, **read
`references/feedback-loop.md`** and record it through the validated helper.
At session close, use that reference to audit the journal and decide whether a
consolidation is due. When it is due and authorized, also read
`references/consolidation.md` directly before editing this skill. Raw feedback
stays local and gitignored.

## Communication discipline

- One short pipeline status: done / in progress / blocked-and-why.
- Don't retell subagent reports — only the decision and the next step.
- Progress claims only from tool results of this session; unverified — say so.
- Check budget/limit consumption at session start and before each large
  parallel dispatch. Quick estimate:
  `npx -y ccusage@latest blocks 2>&1 | tail -20` — a local-transcript estimate
  of the current 5-hour block (weekly totals are estimates too; authoritative
  percentages exist only in the interactive `/usage` panel — when the estimate
  runs hot, ask the user for the `/usage` numbers). Tool unavailable — skip
  without blocking. When low (>80% of the block, a hot weekly estimate, or the
  user reports a squeeze): lower subagent effort, merge small tasks into
  bigger ones, defer optional review passes; near a block boundary keep every
  dispatch's partial completion durable (commit-per-spec, sequential batches)
  and defer long unsplittable passes past it; never skip specs or verification.
- The final message re-grounds a reader who saw none of the process: outcome
  first, then evidence, risks if any, and the next step; plain sentences, no
  internal labels, arrow chains, or invented shorthand from the run.
