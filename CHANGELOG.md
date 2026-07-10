# Changelog

## 2.12.0 — 2026-07-10

Structural compression of SKILL.md: 54.7KB → 45.5KB always-loaded (−17%),
with a further 8.2KB of situational material moved to `references/*.md`,
loaded only when that situation arises. (Line counts are not comparable across
versions: the old file kept whole paragraphs on single lines; the new file
wraps at ~78 columns.) No rules changed — only relocated behind decision-point
pointers or reformatted; every hard rule, tier, caveat, and catalog item
preserved.

- Progressive disclosure: Codex rules of engagement → `references/codex.md`
  (imperative pointers at the routing-table row and the Codex section); Loop
  mode → `references/loop-mode.md` (pointers in the prime directive and the
  Loop mode section); consolidation mechanics → `references/consolidation.md`
  (pointer in the Review trigger section).
- Bulletized the large rule catalogs for weak-reader enumerability: report
  protocol, autonomy standing gates, "Verify, don't inherit" surfaces,
  "Enumerate the category" corollaries, "DoD gates" rules, final-review
  arbitration and cleanup.
- Tightened model-role profiles to role + routing + caveats (all caveats
  kept: Sonnet tokenizer +30%, Fable classifier refusal→Opus, Haiku drift,
  Opus noisy-context literalism).
- "Smallest surface wins" gains a target: situational reference material goes
  to `references/*.md` with an imperative pointer at the decision point.
- `scripts/publish-check.sh` allowlist extended with `references/*.md`; README
  "What's inside" table updated.

## 2.11.0 — 2026-07-10

Consolidation of 56 feedback entries — 43 applied across 11 rule-groups plus
minor folds, 13 rejected as already-covered or project-specific. Clusters past
the ≥2-observations/≥2-sessions gate: enumerate-the-category (×8, ≥3 sessions),
artifact-without-consumer (×3), field-name-on-consumer (×2), rendering-model-
before-curl (×2); the rest are safety/ops singles promoted on explicit user
request.

- Verify-don't-inherit extensions: a field/column name is verified on the
  CONSUMING type (client type, view's exposed columns), not the producer/DB row;
  artifact round-trip consumability (patch→`git apply`, export→import) is
  executed, never inferred from format family; an identifier's cross-process
  lifecycle (minted vs loaded) is traced before cross-invocation reuse; concrete
  numbers in a spec/DoD are computed, never invented.
- Spec quality — enumerate the category, never a hand-picked list: define the
  category (fields, copy strings, state writers, render variants, invariant
  code-paths, worktree gates, deep-equal tests, shared-port implementors/mocks)
  and have the executor enumerate members; word Boundaries as runtime-behavior
  limits when a type cascade must cross them.
- Spec quality — no new surface without a consumer: wire the first consumer or
  state why it ships unconsumed; gate an extracted helper on a duplication
  census of landed code. Final review resolves an unconsumed artifact in-package
  (wire or delete), never deferred.
- Spec quality — fail safe on destructive paths: trace every producer of a
  decisive value, distinguish absent-by-design from absent-by-failure, default
  the failure branch to inert (a fail-open loader feeding a removal set is a
  mass-delete on any blip).
- Cross-task — reconcile the combined failure matrix when task N+1 modifies a
  recovery/error path task N also changed this session.
- DoD — mutation probes break the guarded logic (not a shared constant) and pin
  a literal boundary; conditional steps assert behavior, not diff location; a
  gate on a deferred/scheduled action is re-checked at fire time with a race
  test; every failure representation dominates success-styled branches; a
  schema-add accounts for the live DB.
- UI DoD — confirm the rendering model before a `curl` smoke check: SSR `curl`
  executes the real server render (a strong crash check); CSR needs a headless
  browser; client-prefill/interactivity verified by code-read, not the curl body.
- Dispatch — resume-from-transcript is risky for write work (respawn fresh on a
  stall after auditing traces); consecutive watchdog stalls across agents mean
  infrastructure, so go synchronous.
- Cleanup/monitoring — check liveness before destroying seemingly-stale
  branches/worktrees; use `ps -p <pid>` not `kill -0` (sandbox EPERM reads as
  death → treat permission-denied as ALIVE), watch the recorded worker pid, and
  double-confirm terminal events; trust the orchestrator's own `git status`, not
  a scout's clean report, before an overwriting dispatch.
- Push — `git fetch`/`ls-remote` before an authorized push to learn the true
  scope and report the real pushed range; re-confirm authorization after a scope
  pivot; git-topology from a dossier/memory is a hypothesis to re-measure.
- Report protocol — label dispatches as `<role/model> + <task-id> + <subject>`
  with aligned report filenames; session-scratchpad specs can vanish between
  turns (verify existence before dispatch, reuse one spec dir verbatim).
- Minor folds: a shared key schema for parallel consistency sweeps; run a tool
  in its native mode when the task is to test it; re-read the host sentence for a
  verbatim in-sentence insert; relevance-check all candidate sources before
  synthesis.

Rejected (13): audit cross-migration redefinition, UI-mechanics existence,
API-gateway status-class, out-of-family cross-check, documented-limitation-as-
bypass, cache-cleanup denial (already covered by existing rules); foreign-repo
pre-commit hooks, prompt-template drift, runner manifest allowed-paths, runner
kill/resume recovery, base-branch upstream (project-specific → dossier).

## 2.10.0 — 2026-07-10

Consolidation of 33 feedback entries — 8 rule-groups, each past the
≥2-observations/≥2-sessions gate:

- Report protocol: a stop-notification digest is unconfirmed until its key
  claim (commit hash, report file, test count) is artifact-checked with
  read-only commands; on a missing artifact, re-check before condemning the
  agent or dispatching a replacement.
- Verify-don't-inherit extensions: call-graph claims, type-union members,
  API-gateway error-code contracts, reviewer findings as secondhand claims,
  existing-test coverage in the branch diff.
- DoD gates: known-flaky/red tests excluded from absolute gates (baseline
  provenance recorded); pass-count delta when a hang/cancellation tail exists;
  UI-copy/structure deletions must run the test suite and update co-located
  tests open-to-assert.
- Task board: statuses start at todo; never pre-fill future results.
- Final review: standing axis — engine/runner tests run only on self-created
  temp fixtures, never against the enclosing repo.
- Dispatch: verify a check-driven executor can actually run its checks
  (permission surface, dependency installs) before dispatch.
- Hard rules: an explicit user waiver of rules 1–2 is honored, session-scoped,
  with verification stages kept.
- Consolidation: the head applies SKILL.md/CHANGELOG edits itself (the
  self-modification classifier blocks subagent edits of startup-loaded files);
  the fresh verifier is unchanged.

## 2.9.2 — 2026-07-07

- §4: notification-driven chain documented as the default dispatch loop
  (pre-written specs + one background executor per file-intersection group +
  completion-notification wake-ups; resume the same agent for follow-ups on its
  own work; parallel only for disjoint repos/file sets). Promoted on explicit
  user request after a full-session run of the pattern.

## 2.9.1 — 2026-07-06

- Dispatch envelope: DoD checks must run/complete inside the executor's turn
  (no background-wait turn endings); promoted on explicit user request
  (issue_key executor-ended-turn-waiting-on-background-check).

## 2.9.0 — 2026-07-06

- Head-model parameterization: the skill now names "the head" (whichever
  model runs it) instead of assuming Fable throughout the operating rules.
  Fable 5 stays the default and strongest head; Opus 4.8 is a supported head
  via explicit user opt-in; Sonnet is not a supported head for spec-writing
  or fork-resolution. New "Head model" section (after "Why this mode
  exists") states the Opus adaptations: final review/architecture-critical
  verification stays a fresh-context subagent, never self-review; a one-shot
  Fable "architect consult" is an escape valve for the hardest ill-defined
  forks (raw material only, the head still decides); scouts keep the head's
  context clean since Opus executes noisy context literally; vision-heavy DoD
  comparisons delegate to a vision-capable subagent for non-Fable heads. The
  visual-DoD rule's screenshot-reading claim is generalized accordingly.
  Frontmatter description updated to name the head parameterization.

## 2.8.0 — 2026-07-05

- First feedback-log consolidation (71 raw entries reviewed, backlog cleared to
  `archive.jsonl`; see `SUMMARY.md`). 10 clusters cleared the promotion gate
  (≥2 observations, ≥2 sessions) and were folded into the smallest fitting
  surface:
  - **Verify, don't inherit** (9 sessions, the dominant pattern): a spec
    asserting a codebase fact — existence, location, validity, live wiring,
    git-tracking state — inherited from a scout summary, pasted report, or
    memory anchor instead of a direct read. New spec-writing rule to treat
    every secondhand claim as a hypothesis to verify.
  - **DoD gates must fit the task's scope** (merges 4 sub-patterns, 3-9
    sessions each): repo-wide gates asserted as absolute-green break on
    pre-existing unrelated failures — scope to the delta; grep-based bans must
    not collide with spec-mandated prose; fresh-environment specs need
    explicit bootstrap steps and content-aware (not existence-only) checks;
    DoD counts must assert invariants, not brittle deltas, and a changed fact
    must be grepped and updated across every surface.
  - **Contracts frozen early must fit what's consumed later** (2 sessions):
    derive a consumer task's needs field-by-field against the frozen producer
    contract before dispatch.
  - **Runtime/live smoke beyond visual fidelity** (3 sessions): typecheck +
    build + HTTP-200 can all stay green while the page crashes at runtime or
    a spawned process hangs — any UI-behavior or external-process change
    needs a live smoke stage, not just visual-design diffs.
  - **Destructive-fork and publish discipline** (6 sessions, reinforces
    Autonomy tiers from 2.7.0): irreversible/destructive actions are never
    pre-authorized inside a spec, even via prior-session board notes — always
    re-confirmed live; executor envelope now states "commit only, never push"
    explicitly.
  - **Subagent reporting mechanics** (4 sessions): final messages must carry
    the complete report, not a lone correction; external-CLI agent artifacts
    are a hard completion gate; Explore-type scouts can't Write.
  - **Background-dispatch turn discipline** (bundled with the above): end the
    turn after a background dispatch instead of polling; a subagent waiting on
    its own child job polls in-turn rather than pausing on Monitor.
  - **Worktree/disk hygiene** (3 sessions): check `df -h` before fanning out
    dependency-installing worktrees; verify a prerequisite commit is present
    in a worktree's base before dispatch.
  - **No `git stash` for executors in shared checkouts** (2 sessions): use
    `git show`/`git diff <sha>` for baseline comparisons instead.
  - Roughly 25 single-session observations (incl. this session's own
    dev-server teardown and DoD-grep-self-collision findings) were reviewed
    and rejected for now under the promotion gate — logged in `archive.jsonl`
    for re-evaluation if they recur.

## 2.7.1 — 2026-07-05

- Loop mode refinements from a third-party "self-improving system in 14 steps"
  write-up. Most of it was already covered (verifier>self-critique, routing
  matrix, worktrees, visual DoD, safety boundary, the state-file/memory
  progression = the feedback loop + project dossier) or too unreliable to trust
  on specifics (mixed model versions, unverifiable launch lore) — only the
  loop-execution nuances were taken:
  - Trigger types named: manual `/loop`, cron schedule, or event (CI failure,
    new PR); days-long / laptop-off runs belong on hosted infra (a saved cloud
    routine), not a local session that dies with the terminal.
  - Hard-stop condition fits the loop's job: an improvement loop stops at a
    target metric / done-check; a discovery/audit loop stops after N rounds
    surface nothing new (until-dry).
  - A classifier refusal in an unattended loop is a distinct outcome, not a
    failed round: route to Opus and log it, never silently retry on Fable or
    burn the attempt cap — otherwise it becomes a silent regression.

## 2.7.0 — 2026-07-05

- Folded the orchestration-relevant patterns from two third-party Fable 5
  write-ups (a "build anything" guide and a "loop library"); items already
  covered by v2.6.0 (effort dial, refusal→Opus fallback, review-the-output)
  were left as-is. New material was grounded against a real deterministic
  loop harness ("agents execute, loop orchestrates, checks decide, git records"),
  not the marketing framing:
  - Autonomy tiers (green/yellow/red): classify every task and loop round by
    what it may do unsupervised — green runs alone, yellow drafts for a human
    to ship (branch/PR/diff, never straight to main/prod), red
    (money/prod/outbound/customer-facing) never runs alone. Subsumes and
    generalizes the scope/money-fork stop rule; push/force-push/primary-data
    overwrite are yellow-or-red with a planned authorization gate.
  - DoD "Done is proven, never self-reported": the check's evidence (real
    output, exit code, diff, screenshot) is the deliverable, not the agent's
    claim; a conversation-only judge (`/goal`) can confirm only the proof in
    front of it, so its done-condition must demand that proof inline — "done
    when tests pass" is a wish, "done when the green run is in the report" is a
    contract.
  - New "Loop mode" section for recurring/scheduled runs (`/loop`, `/goal`):
    same division of labor, recurring — Fable creates the key files (queue,
    specs, cross-run lessons), a cheap model runs the routine rounds,
    deterministic checks decide, git records; the five parts a loop needs
    (schedule, one-change-per-round, same falsifiable check, loop-owned state
    file, hard stop with round/spend caps + done/blocked); route rounds through
    the autonomy tiers; run once by hand before scheduling.
  - Not adopted: the guides' core "cheap model plans, Fable executes the long
    run" inverts this skill's Fable-as-orchestrator paradigm (Fable does
    judgment and creates key files; cheap models execute) — kept the skill's
    stance.

## 2.6.0 — 2026-07-05

- Folded the in-scope, orchestration-relevant guidance from Anthropic's
  official Fable 5 prompting guide into the skill (items already covered —
  progress-audit rule, memory loop, delegate-and-continue — were left as-is):
  - Model routing: effort is a cost/latency trade-off, not a quality dial —
    `high`/`xhigh` only where first-shot correctness beats speed; raising a
    subagent's effort (Agent `effort` param or `ultrathink` in-prompt) is a
    legal escalation lever alongside swapping models.
  - Prime directive: an assessment is a complete deliverable — Fable is more
    proactive than Opus, so a question/thinking-out-loud gets an answer, not
    an auto-spun pipeline; the trigger to build is an instruction, not an
    inference.
  - Fable role caveat: named the safety-classifier domains (offensive-security,
    biology/life-sciences, summarized-thinking extraction); route first-touch
    work in those domains to Opus instead of eating a likely refusal.
  - Specs: UI tasks get a visual DoD — compare a live headless screenshot to
    the design target/baseline and name the diffs; crop-and-zoom to unlock
    noisy-input preprocessing; a pass without a rendered comparison is
    unverified.
  - Communication: final-message shape made explicit — outcome, evidence,
    risks, next step; no internal shorthand or arrow chains.

## 2.5.0 — 2026-07-04

- Merged the most valuable rules from two user-provided orchestrator variants
  (an issue-based "hands" pipeline and a multi-model pipeline); model routing
  and the PLAN.md/spec-file board are unchanged:
  - New hard rule 5: judgment is never delegated — scouts bring facts with
    coordinates and all N options with objective attributes; the orchestrator
    picks. Scout prompts get an allowed/forbidden verb list.
  - Falsifiable DoD: the check must be able to fail — mentally break the
    solution and confirm the command catches it.
  - Under-recon markers: "probably/likely/apparently" banned in specs —
    resolve before dispatch or promote to an explicit Decision.
  - Grounding gate for synthesis artifacts: name the deepest source of truth,
    verify claims against it verbatim (connectives/quantifiers added during
    compression); derived-vs-derived agreement proves nothing.
  - Executor envelope: STOP on spec-reality divergence or already-done work,
    with proof (a divergence is a spec defect, the ladder does not advance);
    reports gain a "Noticed, didn't touch" section triaged into new tasks.
  - Report protocol: full subagent reports as files under `<taskdir>/reports/`
    with self-sufficient ≤15-line digests; successor audits predecessor's
    traces after mid-task death; browser checks headless only.
  - Verifier verdict "unverifiable here" is legal — a named risk beats a
    silent green.
  - Final review arbitration: accept / reject-with-rationale / defer-to-task;
    always accept "tests green but a protection silently died". Pipeline-end
    cleanup: stop leftover processes before removing worktrees and branches.
  - Codex: end every `codex exec` with `</dev/null` (stdin hang trap).

## 2.4.0 — 2026-07-04

- Session close step (user correction: the skill was never updated after
  sessions despite 28 pending feedback entries): mandatory end-of-session
  sweep of uncaptured events, SUMMARY.md pending-clusters refresh,
  review-trigger check with a one-line consolidation proposal, and an
  explicit feedback outcome in the final report. Review trigger now
  evaluated at session close as well as session start.

## 2.3.0 — 2026-07-03

- Codex headless launch rules made precise (user prompt about permission
  requests): approvals never block `codex exec` — they fail cleanly; pin
  `--sandbox` AND `-c approval_policy=never` explicitly (ambient config.toml
  sandbox_mode may be danger-full-access); post-subcommand `-a` is broken
  (openai/codex#26602); write tasks get `workspace-write` inside a worktree;
  full-access/bypass only in externally sandboxed environments with explicit
  user approval.

## 2.2.0 — 2026-07-03

- Codex quota check (explicit user request): before the first Codex routing of a
  session, read the weekly/5-hour `rate_limits` snapshot from the newest Codex
  session rollout log (quota-free, offline); re-read after each `codex exec`;
  above ~80% weekly used, route to Codex only on explicit user request.

## 2.1.0 — 2026-07-03

- Budget check made concrete (explicit user request): at session start and before
  large parallel dispatches, estimate the current 5-hour block via `ccusage`
  (local-transcript estimate); the authoritative session/weekly percentages exist
  only in the interactive `/usage` panel — ask the user for them when the estimate
  runs hot. Downshift actions unchanged: lower effort, merge tasks, defer optional
  review passes, never skip specs or verification.

## 2.0.0 — 2026-07-03

- Feedback loop: adverse events captured to `feedback/log.jsonl` (issue_key clustering), review trigger (≥2 repeats from ≥2 sessions, or ≥5 pending), consolidation through the normal spec→executor→verifier pipeline with promotion gate, smallest-surface mapping, and privacy scrub.
- New hard rule 4: log adverse events before moving on; a missing record is a process failure.
- Failure triage before the escalation ladder: spec defects and environment failures no longer burn executor attempts.
- Continue-vs-spawn rule for executor reuse; task board single-writer rule; verifiers now also check for unintended tracked changes.
- Recon starts by reading `feedback/SUMMARY.md`.
- Published as a public repo with `scripts/publish-check.sh` (tracked-file allowlist + secret/path leak scan).

## 1.0.0

- Initial orchestrator skill: hard rules, Sonnet/Haiku/Opus routing table with Codex exception channel, self-contained spec template, dispatch by pointer, fresh-context verification with escalation ladder, final review.
