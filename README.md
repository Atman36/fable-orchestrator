# fable-orchestrator

A Claude Code skill that turns Claude Fable 5 into a pure orchestrator: Fable
understands the task, resolves forks, and writes executor-ready specs — all
reading, coding, and verification is delegated to cheaper subagents (Sonnet,
Haiku, Opus), and every result is accepted by a fresh-context verifier that
did not build it.

## Why

Frontier-model tokens are expensive and context is scarce. The division of
labor that works: the smartest model does judgment (task intent, fork
resolution, spec-writing); execution runs on models that are fast and cheap;
acceptance belongs to an agent with a clean context. This skill encodes that
as hard rules, a model routing table, a spec pipeline, and a feedback loop
that makes the skill itself improve across sessions.

## Install

```sh
git clone https://github.com/Atman36/fable-orchestrator "$HOME/.claude/skills/fable-orchestrator"
```

Then reference it from your global `CLAUDE.md` so it loads for Fable sessions:

> If the running model is Fable (`claude-fable-*`): read
> `~/.claude/skills/fable-orchestrator/SKILL.md` at session start and operate
> as the orchestrator it describes.

The skill also supports Opus 4.8 as the head via explicit invocation
(`/fable-orchestrator`), for when Fable is unavailable or too costly.

## What's inside

| Path | Purpose |
|---|---|
| `SKILL.md` | The skill: hard rules, model routing, spec template, pipeline, feedback loop |
| `references/` | Situational reference material (Codex rules, loop mode) — read only when that situation arises |
| `scripts/publish-check.sh` | Public-safety gate: tracked-file allowlist + secret/path leak scan |
| `feedback/` (local only, gitignored) | Raw session lessons; never published |
| `CHANGELOG.md` | Versioned history of rule changes |

## The feedback loop

1. **Capture** — adverse events (verifier rejections, user corrections,
   routing escalations, spec defects) are appended as one-line JSONL records
   to `feedback/log.jsonl`, keyed by `issue_key` so repeats cluster.
2. **Review trigger** — at session start the orchestrator reads
   `feedback/SUMMARY.md`; consolidation is proposed when an issue repeats
   (≥2 entries from ≥2 sessions) or ≥5 entries are pending.
3. **Consolidate** — a normal spec → executor → verifier task on this very
   repo: repeated lessons are generalized (privacy-scrubbed) and promoted into
   the smallest enforceable surface — a routing-table row beats a prose
   paragraph — then dispositioned in the log, versioned in the CHANGELOG,
   committed.

Raw lessons stay local (`feedback/` is gitignored); only distilled, generic
rules are published. `scripts/publish-check.sh` enforces the boundary and
must pass before every push.

## License

MIT
