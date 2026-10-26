# fable-orchestrator

A capability-first orchestration **skill** for Claude-family, Codex-family,
and explicitly supported agent shells. A head model owns the intent, specs,
judgment and final synthesis; bounded workers implement, while independent
checks accept results. The skill is instructions and validators — **not** a
server, scheduler, background worker service or installation of Orca/Hermes.

## Use

Load `SKILL.md` in a compatible skill host or invoke it through that host's
verified skill-loading mechanism. Follow the host's actual model/tool catalog
instead of assuming a model ID, slash command or native `Agent` API is present.
For a one-off change start with one executor and a separate deterministic
check; scale out only when tasks and isolation justify it. Sensitive effects
(push, merge, deployment, paid actions, external messages, destructive
cleanup, private-data egress) remain subject to explicit human gates.

The reference most likely to prevent a failed first dispatch is
[`references/execution-backends.md`](references/execution-backends.md): it
explains preflights and minimal fallback paths for native subagents, an
**installed and enabled** Orca runtime, and other optional shells.

## Structure

| Path | Purpose |
|---|---|
| `SKILL.md` | Always-loaded operating contract: hard rules, autonomy, routing and handoff |
| `references/execution-backends.md` | Runtime capabilities, supervised worker ownership, worktrees, recovery, bundles |
| `references/pipeline.md` | On-demand recon → spec → dispatch → acceptance → final review |
| `references/loop-mode.md` | Scheduled/recurring work only on a verified durable host |
| `references/model-roles.md`, `references/codex.md` | Conditional model routing and Codex CLI restrictions |
| `references/spec-traps.md` | Evidence-derived spec and DoD pitfalls |
| `references/feedback-loop.md`, `references/consolidation.md` | Local feedback and owner-approved rule promotion |
| `scripts/` | Standard-library validation helpers and tests; `publish-check.sh` is a local leak/allowlist gate |
| `CHANGELOG.md` | Version history (not raw session or project feedback) |

Local `feedback/` journals and project/task artifacts are **not** part of this
skill distribution. They stay outside public material and are excluded by
`.gitignore`. A distribution ZIP does not provide an Orca runtime, Hermes
skill bundle, saved task board, remote credentials or persistent agent sessions.

## License

MIT

## Ownership transfer

Read `references/session-handoff.md` before transferring a head; use the
stdlib `scripts/handoff-validate.py` for snapshot/Git provenance checks.
Neither the skill nor this validator installs a leader lock or proves that
old heads and their workers have lost write permissions. Until the chosen
runner has tested enforcement, transfers are manual and operator-confirmed.
