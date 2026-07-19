# Spec traps — the accumulated catalog

Read this file before writing any spec or verifier prompt (SKILL.md §2 points
here). Every rule below was promoted from logged failures; consolidations
append here so SKILL.md's always-loaded weight stays flat. The three sections
mirror SKILL.md's spec principles: secondhand claims ("Verify, don't
inherit"), category enumeration ("Enumerate the category"), and DoD gates.

## Secondhand claims — surfaces that keep burning sessions

Every secondhand claim (a scout digest, a pasted review, a dossier line, a
memory anchor) is a hypothesis until a direct read confirms existence, exact
location, and current content:

- Build-tool configs: confirm existence and content — never assume missing or
  present.
- "Preserve as-is" values: sample the actual values — the field name proves
  nothing.
- Feature availability: imported/rendered in the live tree, not just present
  in the file tree.
- Any commit/diff DoD step: verify which repo tracks the target path
  (`rev-parse --show-toplevel` + `check-ignore` + `ls-files`) at spec/addendum
  WRITE time, not first at dispatch — a create-document-at-path deliverable
  counts as a commit-DoD step even when the spec never says "commit". Test the
  exact candidate FILE path, never the parent directory: ignore verdicts are
  per-path (a `docs/*` pattern with tracked exceptions ignores new files while
  `docs/` itself reads as not-ignored).
- A call-graph claim ("X never calls Y") — trace it before freezing it into a
  Decision.
- A persistence or render-data claim is traced end-to-end through EVERY
  mapping layer, not only the one a scout quoted: "the `...values` spread
  carries the new field" fails at an action-layer input builder that maps
  fields explicitly, and every named row/field of a render/report spec needs a
  persisted producer — a value can be computed and then discarded.
- A member of a type union is not evidence the code path exists — trace the
  producer of each variant.
- An API gateway's error-code contract differs from the backing system's —
  verify against a live call or spec both families.
- A reviewer's finding is secondhand too — verify its anchors like any scout
  claim.
- Before ordering a test addition in a fix spec, check the branch diff for an
  existing equivalent test.
- Ordering a test-assertion change: quote the WHOLE test body in recon or have
  the envelope order a sibling-assertion audit — a neighboring negative
  assertion can pin the very behavior being fixed.
- A field/column name is verified on the CONSUMING type that reads it (a
  client type, a view's exposed column list), not just on the producer or DB
  row it was copied from.
- A NEW literal ordered into a typed sink (audit action, event kind, enum-ish
  field): recon quotes the sink's type — closed union, exhaustive switch,
  label map — and the spec extends the union and its labels in-scope or
  explicitly authorizes the cast.
- A prescribed cross-module import is a claim about module boundaries: check
  the source module's directive (`'use client'`) before ordering an import
  into server code; when constants must be shared across the RSC boundary,
  prescribe a neutral shared module up front.
- "Artifact A is consumable by tool B" (a patch by `git apply`, an export by
  its importer) is a round-trip fact — execute the round-trip, never infer it
  from format family.
- An identifier's lifecycle across process boundaries (where a run/session id
  is minted vs loaded) — trace it before freezing cross-invocation reuse; a
  same-process observation does not transfer to a resume or restart path.
- Any concrete number a spec or DoD quotes is computed from the real data or
  marked do-not-assert, never invented as an illustration.
- A migration/sequence number is a codebase fact: list the target directory in
  recon; never inherit the next number from a dossier or memory.
- A scout's negative claim ("only consumer", "no X exists") entering a DoD or
  Decision: re-verify with your own grep at spec time, sweeping untracked and
  gitignored files too, or word it conditionally — never freeze it as a hard
  empty-grep DoD.
- Claims beyond file contents are hypotheses too: a library's runtime surface
  (an error class's `.name`, a module's static classes), a command or npm-script
  name entering a DoD, a fixture's arithmetic (zone spreads, date windows), an
  env var's presence under the test runner (`loadEnv` forwards real creds), an
  id's transform as it crosses a layer (a raw record id hashed into an opaque
  one) — verify in recon or prescribe the goal and let the implementer validate
  against the real runtime.
- A dossier/handoff claim ages: 'done' work inherited uncommitted gets its
  tests actually run before you commit it, and dossier 'open items' get
  re-checked against commits newer than the entry before you spec a fix.
- An environment-target label (staging vs prod) in a digest is a hypothesis —
  before it enters an owner-facing report, cross-check it against which env
  prior sessions audited with the same creds and against writes the owner says
  they made; mislabeling prod as 'staging' hides the more severe fact.

## Enumerate the category — corollaries

- Reconcile the enumeration against Boundaries: a category member inside a
  do-not-touch file needs the boundary widened or an explicit deferred-risk
  note.
- Steps/DoD cover every member of a category Context declares, or record a
  per-member carve-out — a hand-narrowed Steps list silently contradicts the
  spec's own category.
- The rule holds inside one file: enumerate every read/render of the value in
  the touched file, never only the line a scout quoted.
- The rule binds the head in direct-edit (waiver) mode too: define each
  cleanup category as a runnable grep (a meta-verb alternation, a slang list)
  and run it BEFORE any verifier — reading-based enumeration misses instances.
- Adding a member to a shared port/interface cascades to every implementor and
  mock — enumerate them in Steps, and word Boundaries as runtime-behavior
  limits, never file-ownership limits over directories the cascade must cross.
- When a spec turns a previously write-only value into logic input (a stored
  date now read against the clock), the sweep includes existing seeds and
  tests whose fixtures thereby become clock-relative.
- A changed TYPE cascades to every constructor and call site of it — test
  fixtures that build it, and every writer that assembles its full literal —
  not only implementors of its interface.
- The recon question is itself category-shaped: grep every member repo-wide,
  never hand the scout a suspect-file list. For an exhaustive sweep (a privacy
  scrub, packaging excludes, a repo-wide fact change) the recon file-list is
  only a seed — the executor sweeps the whole tree and the DoD compares against
  the prior artifact's size/count or runs an independent second pass.
- Before freezing a uniform change across the enumerated category, sample each
  member for a deliberate documented carve-out — one that diverges on purpose
  gets its own Decision line, not the blanket change.

## DoD gates

- A DoD reusing a repo-wide gate (lint, typecheck, a tree-wide pattern scan)
  snapshots the gate's pre-existing state and asserts no NEW violation from
  the touched files, never absolute green — a pre-existing failure elsewhere
  (including the user's own uncommitted WIP) makes a global-green DoD
  unmeetable without violating Boundaries.
- Reconcile every DoD check against the spec's own Boundaries before dispatch:
  a negative grep over a directory must be satisfiable by every step touching
  it; a token-ban grep must not target a file whose spec-mandated content
  legitimately mentions the token in prose/comments — or a test file whose
  negative assertions cite the literal to assert its ABSENCE (scope the grep
  to non-test sources or exempt those tests); this reconciliation covers the
  verifier prompt too — the head authors both DoD and verifier grep and can
  contradict itself; prefer the project's real scanner over an ad-hoc grep
  when one exists. Reconcile every Boundaries/Steps ban against every behavior
  the spec itself requires — a banned data source that a required behavior
  still needs gets an explicit carve-out. Cross-check a scout-authored
  instruction doc's own test list against its Steps/DoD before freezing the
  spec, and resolve any contradiction by the DoD.
- A spec that delegates acceptance to a source doc or shared contract quotes
  the criteria list verbatim (or binds the doc itself) and derives its DoD
  from it line-by-line — every "must" line gets a mechanical check in each
  consuming spec; a paraphrase silently narrows acceptance, and with parallel
  executors the gap ships category-wide.
- In a parallel dispatch over a shared checkout, scope every DoD command to
  the executor's own paths — a directory-wide glob ("exactly N files") sees
  sibling executors' output and fails, or worse passes, spuriously.
- Optimistic or mirrored local state (a local copy shadowing an async store
  write) gets a failure-path DoD test: the write rejects → the mirror reverts;
  the happy path alone hides a stuck-state bug a lane verifier passes over.
- Fresh environment (worktree, CI, clean clone) or first instance of a new
  artifact class: enumerate bootstrap/build prerequisites explicitly; the
  verifier simulates the fresh environment, not a warm checkout. An existence
  check on a directory tooling creates as a side effect (a `.vite`/`.cache`
  dir) must check CONTENT, not mere existence.
- Counts/facts stated in multiple places: assert the invariant (both cases
  tested; all instances updated), never a brittle exact delta — a count other
  tasks may also grow needs a relative assertion (`all pass`, `>=N`); a
  fact/count change greps the OLD value repo-wide and updates every surface
  (docs, CLI help/usage strings, comments), not just the primary one.
- Known-flaky or documented-red tests never enter an absolute gate: check the
  dossier/handoff for flaky tests under the gated path and exclude them, scope
  the gate to the new tests, or assert no-NEW-failures against a recorded
  baseline — and record WHERE the baseline ran; untracked test sources skew
  counts.
- Target test file with a known hang/cancellation tail: place new tests BEFORE
  the hang and assert they actually ran via a pass-count delta — zero failures
  proves nothing about cancelled tests.
- Deleting/renaming user-visible copy, or moving content behind a disclosure
  element: run the project's test suite in the DoD and grep the old strings
  across test files; co-located tests get updated to the new contract
  (open-to-assert), never deleted — typecheck and lint cannot see any of this.
- A mutation probe that only bumps a constant the tests derive their fixtures
  from is tautological — break the comparison or logic the check guards and
  pin at least one literal boundary value independent of the constant.
- A DoD grep asserting a change in a specific file presumes that file must
  change — for a conditional step, assert the resulting behavior, not the
  diff's location.
- A literal command in a DoD or verifier prompt is a claim too: dry-run it
  against the real dispatch/selector logic it routes through (mode flags, env
  precedence) and the actual file layout (a blank line eats a `grep -A`
  budget), or state the content assertion and let the verifier choose the
  command.
- A gate on a deferred/scheduled action (a timer, a queued callback): confirm
  the gate is re-checked at fire time — not only at scheduling time — with a
  race test that flips the condition inside the window; when failure has
  several representations (an error-reason field vs a failed-state enum),
  assert each one dominates the success-styled branches.
- A schema change adding a column accounts for the live DB: apply it with an
  idempotent `ALTER ... ADD COLUMN IF NOT EXISTS`, or explicitly flag that the
  app breaks against any un-migrated DB (a full outage when session bootstrap
  runs a `select *`).
- Cross-check the spec's test enumeration against EVERY behavior and
  user-visible string its own Decisions section mandates — each gets a test or
  an explicit no-test rationale in Decisions.
- A hand-authored HTML deliverable opens with `<meta charset="utf-8">` — a
  locally-opened file has no wrapper to supply the charset, and non-ASCII text
  renders as mojibake.
