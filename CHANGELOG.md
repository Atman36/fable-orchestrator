# Changelog

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
