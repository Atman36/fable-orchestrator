# Changelog

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
