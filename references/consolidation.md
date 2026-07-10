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
  SKILL.md.
- **Privacy scrub:** generalized wording only; no project names, private
  paths, client or employer specifics in tracked files.
- **Disposition:** every reviewed entry becomes `applied@<version>` or
  `rejected(<reason>)`; applied/rejected entries move to `archive.jsonl`;
  bump CHANGELOG.md; regenerate SUMMARY.md.
- **DoD:** `scripts/publish-check.sh` exits 0; hard rules unchanged unless the
  user approved changing them; frontmatter intact. Commit; push on user
  confirmation or when the user asked for publication.
