# Changelog

## 2.19.0 — 2026-07-25

Consolidation of the 25 entries logged since 2.18.0 (2026-07-24..25, five
projects): 23 applied, 2 archived as confirmations of rules already in force,
log drained to zero. One literal `issue_key` repeat, so clustering ran by
FAILURE FAMILY again. SKILL.md +3.0 KB (pipeline mechanics only), spec-traps.md
+8.1 KB (every spec/DoD lesson).

Headline promotion — **a measurement is a claim about the act of measuring, not
about the thing measured.** Five entries, four projects, one shape: the number
was true of the query, the window, or the tree that produced it, and false of
the system. A scout's "26 runs, one unclosed" over 87 days became 27 unclosed
once the run id was joined across all 152 events — after the wrong figure had
reached the user and an owner-facing document; so every "N of M" now states M
from its own `COUNT(*)` and names the join key. A `git log -3` hid the
fourth-commit-back implementation of the task about to be re-specced — ranges
`base..HEAD`, never fixed windows. A baseline probe built off a dirty tree
compiled another session's uncommitted fix for the very defect being baselined
and reported it absent — a baseline pins its artifact to a sha. And a
`0.6 × topScore` floor was frozen over an un-normalised fusion sum whose scale
nobody measured, silently reversing a per-document cap an earlier MAJOR fix had
introduced (invisible to 1143 green tests): a ratio threshold is a claim about
the SCALE, so recon reports the distribution — including the value for the class
the threshold must NOT exclude — or the spec defers the number.

Second family — **a declaration is not a location, and a digest is not a
shape.** `Project.timezone: string` froze the access path `project?.timezone`
while the value lived at `project.settings.timezone`; a hand-maintained types
file declared the same table twice and the converter imported the OTHER
declaration; a digest's item COUNT licensed a spec prescribing a per-item icon
for a registry with no icon field at all; a scout established a document's
structure from its table of contents while the running text disagreed. Recon now
quotes a live READ before an access path is frozen, greps the entity name
file-wide before a schema edit, traces a prescribed attribute to a quoted member,
and reports structural facts as a per-item table with a SOURCE column after
scanning every representation.

Third family — **the half-named category.** An upsert has two column lists and a
spec naming only `values` is half a spec (the UPDATE path silently lost both new
columns; the mocked DB kept everything green). A changed literal is grepped
across tests too, and the test-to-update set declared an authorized Boundaries
extension — otherwise "don't change assertions" + "0 failed tests" + the rewrite
order are mutually unsatisfiable, and the assertion rule is worded as
anti-weakening from the start. A Decision changing what an endpoint RETURNS
pulls the response-type module into the allowlist. A hand-authored vocabulary
list is a claim that the module owns no equivalent — and in an inflected
language its entries are roots, verified by a root → forms → predicate table.
An exempted sibling consumer of a shared constant gets an end-to-end probe and a
pinning test, not a paragraph of reasoning.

Pipeline mechanics (SKILL.md): session-start recon checks for a live CONCURRENT
writer (other `claude` processes, source mtimes), and a foreign writer in the
same checkout halts dispatch as one narrow question; a whole dispatch block
dying on the same transport error is infrastructure — re-dispatch verbatim once
before any triage; an API-death recovery audits git traces first, then resumes
the SAME agent; stall recovery on a fault-injection DoD RUNS the gate rather
than reading `git status`, since that window leaves the tree deliberately broken
and file-level inspection calls it complete. Final review gains a fourth
standing axis — every destructive or terminal transition must establish its
recovery path BEFORE it commits, and stay reachable by the sweep meant to retry
it (three reviews, two repos, same shape, all passing their happy-path tests) —
and an adversarial REFUTE pass now precedes any rework that would rewrite
shipped behavior. Plus a DoD gate: a fix answering an owner complaint is
verified against the branch THEY hit, not the generic case.

## 2.18.0 — 2026-07-24

Consolidation of the 17 entries logged since 2.17.0 (2026-07-21..24, four
projects): 15 applied, 2 archived as confirmations of rules already in force,
log drained to zero. Literal `issue_key` repeats were 2, so clustering again ran
by FAILURE FAMILY across sessions.

Headline promotion — **a check proves nothing until its VENUE can fail for the
reason under test** (SKILL.md §2, full rule in `references/spec-traps.md` § DoD
gates). Seven entries across four sessions, one shape: the command ran, the
probe went green, and the venue could never have produced a failure. Four
preconditions now precede any DoD command or probe — the runner is read from the
repo's own scripts and dry-run against the real tree (a spec froze
`npx vitest run` where the gate was `npm test`; a bare `pytest -q` could not
collect at all against a pre-existing basename collision); the harness entry
point traverses the layer that WRITES the state the feature reads (a probe
bypassing the webhook that owns those writes tested the fallback path); the
probe's surface and principal match the real usage scenario (a group-surface
probe hard-gated to public documents produced a FALSE regression that reached
the owner-facing QA report); and the artifact under test is the freshly built
one. Paired: nondeterministic answer paths need N≥3 runs before any
zero-occurrence claim, and when stale-deploy and missing-env are
indistinguishable through the failing route, a read-only SIBLING route sharing
its helper chain isolates the cause by elimination.

Second family — **enumerate affected tests by IDENTIFIER, never by user-facing
literal** (spec-traps § Enumerate the category). Four entries, three projects: a
literal-string sweep misses a test driving the removed branch through a mocked
input; a scout's test list is a seed, not the category; the same enumeration
feeds the Boundaries file allowlist, not only Steps (a changed type's mock
fixtures are members); a user-visible "confirmation" is a category of surfaces
(message, toast, edited original, keyboard) and anchoring the requirement to one
builder shipped a toast soliciting a comment the flow no longer captured; and a
category used to GENERATE inputs is checked against higher-priority routing
rules before the property is frozen.

Also promoted:

- Autonomy tiers: a red op plans its PERMISSION path up front — auto mode denies
  even user-authorized prod-write commands, and the user's own `!` attempt can
  silently do nothing; confirm the run by its EFFECT, never by the report.
- Spec-traps § DoD gates: an external-system capability premise gets a live
  Step-0 guard with a STOP clause; a gate is never edited to make it pass; a
  project's git hooks can fail inside a worktree while passing in the main
  checkout; a screenshot set claiming N states proves nothing until the N hashes
  are distinct; a performance DoD states its measurement conditions.
- Feedback capture: the log's field set is fixed — one entry written with a
  variant schema (`ts`/`note`) had been invisible to every consolidation count;
  and writes into sectioned documents use anchored edits, never `cat >>`, which
  lands under whatever heading happens to be last.

Confirmed without an edit (rules already in force, kept as evidence): the
API-death resume protocol (2.15.0) and the measured blast-radius stop rule
(2.17.0), both of which worked end-to-end this round.

Sizes: SKILL.md 51819 → 53452 bytes; `references/spec-traps.md` 29047 → 35472.

## 2.17.0 — 2026-07-21

Consolidation of 75 feedback entries (63 new from 2026-07-19..21 plus the 11
singles left pending at 2.16.0 and 1 applied-inline): 73 applied, 2 rejected,
log drained to zero. Literal `issue_key` repeats were only 3, so clustering ran
by FAILURE FAMILY across sessions — that is what met the promotion gate, and
it is how the next round should read the log too.

Headline promotion — **changing a predicate voids every blast-radius claim
scoped to the old one** (spec-traps § Enumerate the category). Two blockers,
two sessions, same shape: removing a narrowing clamp turned a "no audience
stated" placeholder into a real company-wide grant on 257 documents, and
widening an admin gate from one capability to a set of five granted 10 of 13
principals access previously denied. Both survived every per-task
verification, both surfaced only at the cross-task review axis, and in both
cases the head had told the user the change had zero blast radius. Paired
promotion in §6: feed the final reviewer the session's live measurements —
severity is a function of blast radius, and "not measured" in a review is an
action item for the head, not a caveat to accept.

Into `references/spec-traps.md` (12.6KB → 28.9KB; read at spec-writing time,
so the always-loaded file stays the constrained one):

- Secondhand claims — 9 new surfaces: external review/audit packages (dead
  file:line citations AND prescribed fixes as unmeasured hypotheses); negative
  premises ("no caller exists"); a gate cited by superseded migration number;
  migration dependency claims; state ownership / row shape / comment content;
  quantities carried from memory; a third-party library's config surface; a
  dry-run flag's guard expression; WHEN a destructive mechanism fires.
- Enumerate the category — 6 new corollaries: the predicate rule above;
  hand-listed call sites are never the category (2 sessions); registry
  accessor lookups by id; shared-derivation consumers; copy that describes
  changed behavior; existence/cardinality invariants on a new delete path.
- DoD gates — 22 new rules, incl. no DoD may run SQL before recon names the
  venue; production build in the gate for app-router diffs; numeric invariants
  cite their literal output line; mutation probes name the test expected to
  die (a probe that kills nothing is a finding); in-memory DB doubles prove
  nothing about transaction abort; fixtures derive from the real parser; test
  edits outside named files reported with assertions quoted; RLS-filtered
  DELETE fails silently; Boundaries verified against the test harness; ops
  migration application (object census, row count, baseline first).

Into SKILL.md (48.7KB → 51.9KB, +6.5%) — only head-binding and envelope rules:
direct mode widened from documentation-only to any task with NO CODE TO AUTHOR
(user correction); fetch-before-push extended to CI bots writing to main;
recon gains diff-branch-first, masked prod-scout command forms, and the
auto-mode classifier blocking prod DB reads; owner feedback diffed against the
owner's same-day decisions; the git-stash ban now quotes the revert-proof
recipe IN FULL (two executors breached the bare ban); the executor envelope
demands literal command output and test counts split diff-touched vs
swept-unchanged (5 occurrences, 2 sessions); worktree isolation cuts from the
PUSHED ref, with a fast-forward self-heal and never-resume-an-autocleaned-
worktree; verifier file lists re-derived after rework; orchestrator git
mutations use `git -C` plus a branch assertion.

Rejected: api-403-mass-agent-death (already covered by the §4 API-death resume
protocol); executor-stopped-correctly-with-measured-proof (a positive
confirmation of the RED-first and literal-output riders, no rule change).

Note for the next round: SKILL.md grew 3.2KB after 2.16.0 cut it to 45KB. The
additions are all genuinely head/envelope/dispatch rules rather than spec
traps, but the trend is worth a compression pass — with the clause-level diff
audit consolidation.md requires, since careful rewriting silently drops
directives.

## 2.16.0 — 2026-07-19

Consolidation of 40 feedback entries (2026-07-13..19, five projects): 29
applied, 11 singles kept pending. Structural change alongside: the three
accumulated trap lists (verify-don't-inherit surfaces, enumerate-the-category
corollaries, DoD-gate rules) moved VERBATIM out of the always-loaded SKILL.md
into the new `references/spec-traps.md`, with an imperative pointer at the
top of §2 Specs — future spec/DoD-trap promotions append there
(consolidation.md updated), so SKILL.md's weight stays flat. SKILL.md ~53.9KB
→ ~45KB despite this round's additions.

Gate-met clusters promoted:

- commit-dod-path-untracked (×2, 2 projects) — check-ignore/ls-files runs at
  spec/addendum WRITE time; a create-document-at-path deliverable counts as a
  commit-DoD step; verdicts are per-FILE-path, never the parent directory
  (folds check-ignore-directory-vs-file).
- source-criteria-to-dod (dod-paraphrase-dropped-source-criterion +
  contract-requirement-without-dod-check, 2 projects) — quote source-doc/
  contract criteria verbatim and derive the DoD line-by-line; every "must"
  gets a mechanical check in each consuming spec.
- failure-branch-ux (piggyback-save-partial-failure-semantics +
  fail-safe-branch-needs-ux + ui-copy-edgecase-unspecified) — new §2
  paragraph: specify partial-failure semantics of composed writes, the UX of
  disabled auto-transitions, zero/empty renderings of composed strings.
- review-axes (review-axis-interaction-matrix +
  owner-parallel-review-catches-missed-defects) — §6 standing axes: cross-task
  interaction; pre-demo adversarial pass on async/UI-state seams by a second
  independent or out-of-family reviewer.
- dataflow-producer-tracing (dod-item-without-data-producer +
  persist-path-mapping-untraced) — persistence/render claims traced through
  EVERY mapping layer to a persisted producer.
- visual-geometry (visual-dod-no-usability-floor +
  visual-compaction-without-bulk-map +
  jsx-reorder-vs-class-builder-track-mismatch) — visual DoD sets a usability
  floor; height cuts cite a measured per-section map; grid reorders pin the
  class→track mapping or assert rendered widths.
- shared-checkout non-exclusivity (dod-scope-blind-to-parallel-checkout +
  foreign-uncommitted-edit-mid-pipeline) — DoD commands scoped to the
  executor's own paths; foreign tracked-file edits quarantined between
  dispatches with an envelope exclusion line.
- direct-mode-preferred-for-small-doc-tasks (user correction ×2) — the head
  proposes direct mode for small documentation-only tasks.
- Re-armed folds into existing rules: token-ban grep exempts negative test
  assertions; digest distrust extends to env-shape/behavior-pattern claims;
  enumerate-the-category binds the head in direct-edit mode (grep-based
  sweeps); successor-races-live-predecessor extends the live-concurrent-run
  check to "continue" handoffs; smoke-server-inturn-shell sanctioned in the
  envelope (start/poll/kill inside one call); standalone HTML opens with
  `<meta charset="utf-8">` (user correction); api-death-resume ×2 archived as
  rule-held confirmations; log counts via JSON parser → consolidation.md.

From the user's agent-rules digest (2026-07-19): §5 gains three rules —
deterministic DoDs may be gated by scripts/direct runs (independence ≠ model),
reviewers/verifiers never see the executor's reasoning (anchoring), and
acceptance splits into "built right?" (verifier) vs "right thing built?"
(head, against the user's original intent).

## 2.15.0 — 2026-07-18

Consolidation of 42 feedback entries (2026-07-13..18, three projects): 27
applied, 4 rejected as rule-held/covered, 11 singles kept pending (status
`pending` — reviewed below the promotion gate; a repeat re-arms the trigger).
Gate-met clusters promoted into SKILL.md:

- verify-don't-inherit (×4 + history) — new recon bullets: a NEW literal into
  a typed sink quotes the sink's closed union; a test-assertion change quotes
  the whole test body; migration/sequence numbers are listed from the
  directory, never inherited; a scout's negative claim ("only consumer",
  "no X exists") is re-grepped incl. untracked/ignored files or worded
  conditionally.
- enumerate-the-category (×5 + history) — Steps/DoD must cover a
  Context-declared category or record per-member carve-outs; the rule applies
  within a single file too.
- executor-skipped-red-tdd (×3, rider self-caught all) — RED-output-before-
  source-edits promoted into the standing executor envelope.
- agent-backgrounded-own-gate (×3 recurrence after the 2.13 foreground line) —
  envelope bans `&`/run_in_background/Monitor by name; long-gate verifiers
  dispatch synchronously (§5).
- api-death-resume (×4) — a terminal-error notification is not death:
  SendMessage-resume the SAME agent first; fresh finisher only after a stalled
  resume plus a liveness re-check (§4).
- spec-test-list-vs-decisions (×2) — DoD bullet: test enumeration
  cross-checked against every Decisions-mandated behavior and string.
- Near-zero-cost folds: owner-facing/tracked-doc facts recomputed from pasted
  output (digest-distrust + ungrounded-claim-in-owner-doc); combined failure
  matrix covers a new DB trigger vs every existing writer incl. ops scripts;
  complete-report rider extended to chat-text scouts (×2, one session).

SKILL.md 51.0KB → ~53.9KB — AT the ~54KB watch threshold: structural
compression pass due before the next consolidation adds text.

## 2.14.0 — 2026-07-13

Consolidation of 17 feedback entries (2026-07-12/13, two projects). Gate-met
clusters: disk/rollback-artifact loss (×3), runner capture-blind idle-kills
(×2 + a prior-session occurrence), allowed-path mis-scoping (asymmetry +
type-cascade, 2 sessions). New "External runners (a kernel between you and
the executor)" section in references/loop-mode.md consolidates kernel-path
reconciliation, allowed-path unions incl. consumer-test cascades,
gate-exit-code verification, notional cost caps, disk guard +
rollback-patches-are-lossy-period, and kill triage (capture-blind kills,
sleep-suspended timeouts); SKILL.md §3 Dispatch gains an imperative pointer
to it. Prior-session working-tree drafts ratified and committed:
env-label-in-digest hypothesis (verify-don't-inherit), instruction-doc
tests-vs-DoD cross-check, optimistic-mirror failure-path DoD, and
single-order-flake rerun triage. Near-zero-cost folds into the new section:
notional-cost-gate, unverified-check-exit-code, cache-deletion-scope,
macos-sleep-kills-agent-timeout. enumerate-the-category repeat archived with
no text change (rule exists since 2.11.0). One entry stays pending
(executor-skipped-red-tdd ×1). SKILL.md 50.7KB → 51.0KB.

## 2.13.0 — 2026-07-12

Consolidation of 62 feedback entries from ~15 sessions across projects. Clusters
past the ≥2-observations/≥2-sessions gate: enumerate-the-category (×9),
agent-backgrounded-own-gate (×3), dod-grep-vs-spec-mandated-prose (×3),
dod-probe-wrong-invocation (×2), compression-metric-bytes (×2); the rest are
singles promoted on explicit user request (prompt-style-by-model-strength) or
folded into an existing rule at near-zero cost. Repeat-evidence singles (already
covered) were archived without a text change; narrow/project-specific singles
were rejected but kept in `archive.jsonl` as evidence for future repeats.

- Dispatch/recovery — the DoD-gate envelope now says run checks in the
  FOREGROUND (a backgrounded run or Monitor pause will not re-wake you), and
  stall recovery splits on liveness: a still-alive paused agent resumes on a
  SendMessage nudge, a dead one (no notification, work uncommitted) is
  trace-audited and finished by a FRESH agent, never nudged.
- Spec quality — prompt prescription scales with the reader's tier (frontier =
  goal+why+success-criteria; Opus = goal+short plan; executor-tier = fully
  explicit); verbatim code/predicates in a spec are claims too (statics,
  error-class `.name`, copied mock idioms break against real test doubles and
  toolchain hoisting) — prescribe the goal or check against the module's
  existing doubles first.
- Verify-don't-inherit extensions: claims beyond file contents are hypotheses
  (a library's runtime surface, a command/script name, a fixture's arithmetic,
  an env var's presence under the test runner, an id's transform across a
  layer); a dossier/handoff "done"/"open-items" claim ages — run inherited
  uncommitted tests before committing and re-check dossier items against newer
  commits.
- Enumerate-the-category corollaries: a changed TYPE cascades to every
  constructor/call site (test fixtures included), not just interface
  implementors; the recon question is itself category-shaped (grep every member
  repo-wide, not a suspect-file list — exhaustive sweeps like privacy scrubs or
  packaging excludes get a whole-tree pass plus a prior-artifact/second-pass
  check); sample each member for a deliberate carve-out before a uniform change.
- DoD/verifier — the token-ban-grep vs spec-mandated-prose reconciliation covers
  verifier prompts too, and every Boundaries/Steps ban is reconciled against
  every behavior the spec requires; a literal command in a DoD/verifier prompt
  is a claim (dry-run it against the real selector logic and file layout, or
  assert the content and let the verifier choose the command).
- Recon/scope — a "read-only" scout that live-drives a server can still mutate
  persistent state (point mutating probes at a temp store or keep them GET-only);
  before prescribing a new helper, recon greps the domain term for an existing
  one.
- UI DoD — headless checks use the cached ms-playwright Chromium, not a
  system-Chrome `channel` (a sandboxed shell SIGKILLs the system browser).
- Budget — near a usage-block boundary keep every dispatch's partial completion
  durable (commit-per-spec) and defer long unsplittable passes past it.
- `references/consolidation.md` — measure size in bytes not lines; a
  compression/rewrite pass gets a clause-level diff audit by the fresh verifier.
- `references/loop-mode.md` — prod env mutation is a red owner-checklist action
  even under a goal-pack; on a mid-`/goal` user pivot, name `/goal clear` at
  once and author goal conditions with a user-override clause.

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
