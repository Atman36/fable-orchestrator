# Consolidation — promoting feedback into rules

Read this file when the review trigger fires (see SKILL.md "Review trigger")
and the user confirms a consolidation run.

Consolidation is a normal task through the pipeline: spec → executor → fresh
verifier, target repo = this skill's directory.

**Exception for the skill's own files:** subagent edits to the startup-loaded
SKILL.md get blocked by the self-modification classifier when the text arrives
via a spec file — the head applies SKILL.md/CHANGELOG edits itself in the main
session, grounded in the user's in-conversation instruction; the fresh
verifier still validates the result.

- **Promotion gate:** promote a cluster only at ≥2 observations from ≥2
  sessions; a single anecdote is promoted only on explicit user request.
- **Smallest surface wins:** routing lesson → routing-table row; spec-quality
  lesson → spec template or readiness test; verification lesson → DoD/verifier
  rules; scope lesson → Boundaries defaults; project-specific trap → that
  project's CLAUDE.md or dossier, never this skill. Situational reference
  material (needed only when a specific situation arises) → the matching
  `references/*.md`, with an imperative pointer at the decision point in
  SKILL.md. Spec/DoD trap lessons (secondhand-claim surfaces,
  category-enumeration corollaries, DoD-gate rules) append to
  `references/spec-traps.md`, not to SKILL.md — that keeps the always-loaded
  file's weight flat.
- **Prune before adding:** for every candidate, locate the current covering
  clause first. Then audit the destination section for duplicate, superseded,
  dated, or overly situational guidance; delete it or move it to the narrowest
  reference before adding new text. A consolidation that only appends while an
  equivalent rule already exists is incomplete.
- **Count with a parser:** counts over `log.jsonl` come from a JSON parser
  (`python3 -c "..."`), never a grep for an exact `"key":"value"` string —
  JSON formatting varies across writers and a grep silently undercounts.
- **Privacy scrub:** generalized wording only; no project names, private
  paths, client or employer specifics in tracked files.
- **Disposition:** every reviewed entry becomes `applied@<version>` or
  `rejected(<reason>)`; applied/rejected entries move to `archive.jsonl`;
  bump CHANGELOG.md; regenerate SUMMARY.md.
- **Measure and audit the edit:** size deltas are in bytes (`wc -c`), never
  lines — a reflow makes line counts incomparable across versions; and any
  compression or rewrite of a rules section gets a clause-level diff audit by
  the fresh verifier, because even careful rewriting silently drops directives.
- **DoD:** `scripts/publish-check.sh` exits 0; hard rules unchanged unless the
  user approved changing them; frontmatter intact. Commit; push on user
  confirmation or when the user asked for publication.
