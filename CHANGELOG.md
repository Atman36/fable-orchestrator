# Changelog

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
