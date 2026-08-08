# Spec traps — the accumulated catalog

Read this file before writing any spec or verifier prompt (SKILL.md §2 points
here). Every rule below was promoted from logged failures; consolidations
append here so SKILL.md's always-loaded weight stays flat. The sections mirror
SKILL.md's spec principles: secondhand claims ("Verify, don't inherit"),
category enumeration ("Enumerate the category"), divided ownership, and DoD
gates.

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
  claim — and so is the ARCHITECTURE its phrasing implies. Before a spec places
  a guard "in the repository/service layer", recon quotes the function that
  actually executes the operation with its `file:line`: a finding worded around
  a "repository" delete described a delete written inline in a store slice
  (the only repository delete was bulk-only), so the executor built an
  equivalent guard inside the file allowlist and left the real DELETE
  unguarded.
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
- An executor's explanation that the venue cannot exercise a behavior is a
  secondhand claim, not permission to weaken downstream DoDs. A fresh verifier
  measures the capability neutrally, including sampling resolution for
  timing-sensitive probes; sibling specs inherit only that measured result.
- A dossier/handoff claim ages: 'done' work inherited uncommitted gets its
  tests actually run before you commit it, and dossier 'open items' get
  re-checked against commits newer than the entry before you spec a fix.
- An environment-target label (staging vs prod) in a digest is a hypothesis —
  before it enters an owner-facing report, cross-check it against which env
  prior sessions audited with the same creds and against writes the owner says
  they made; mislabeling prod as 'staging' hides the more severe fact.
- A pasted external review or audit is secondhand at two levels. Every
  `file:line` it cites is confirmed to exist at spec-WRITE time — a cited path
  can be absent from the checkout entirely, and a dead pointer is replaced by a
  measurement taken this session, never re-derived from it. And every fix it
  PRESCRIBES is a hypothesis about the system: before implementing a
  recommendation that changes a retry, redelivery, or deletion contract,
  measure the state machine it depends on (attempt counters, whether a retry is
  distinguishable from a fresh attempt, what a reclaim erases) — one audit's
  "return 500 so the platform redelivers" was an unbounded retry loop against a
  store with no attempt counter. The burden of proof sits with the
  implementer, not the reviewer.
- A negative premise ("no legitimate caller exists", "this path is dead") gets
  its own grep across callers AND the test suite before it freezes a removal
  order: a path guarded by an existing test is a consumed contract, not dead
  code.
- A gate cited by migration/policy NUMBER: check for a later migration
  superseding the same policy, and prove the new gate is at least as strict as
  the CURRENT chain, not the cited one. Likewise an ordering/dependency claim
  between migrations is a codebase fact — never write it into a spec or
  operator note as a template fact; order the executor to derive the
  prerequisite chain from the guard's full history (every `CREATE OR REPLACE`
  of the function) and word the DoD as "state which earlier migrations this one
  requires, with the deciding quote".
- Which module OWNS a piece of state, the SHAPE of a row a prescribed helper
  signature is written against, and what a COMMENT says are codebase facts like
  any other: have the scout quote the state declaration, the field names, and
  the comment verbatim — or word the spec as trace-from-call-site with an
  explicit adapt-allowance, never naming the owner.
- Any quantity that SCOPES a decision is measured this session or labelled
  UNVERIFIED — never carried from a dossier or memory file. Memory figures
  predate the very changes that invalidate them (one carried "~790" was really
  22), and an executor will restate a spec's number in a deliverable as
  established fact.
- A scout's claim about a THIRD-PARTY library's config or runtime surface is a
  hypothesis, never a finding — a flat "the library does not expose this option
  at all" has been simply wrong, and believing it would have forced a needless
  workaround. Order the executor to read the INSTALLED package's own typings
  and paste the evidence, and prescribe a preference order of mechanisms rather
  than one assumed-supported mechanism. Verbatim third-party surface a spec
  DICTATES (option keys, method names, error statics) is the same claim about
  the installed version: recon quotes that version's signature for exactly that
  call, or the spec states the GOAL and lets the implementer bind the API. A
  prescribed conflict-clause option key belonged to a sibling method in the
  pinned release — as written it would either fail to compile or silently drop
  the predicate that made the write idempotent.
- A dry-run / no-op flag is unverified until its GUARD EXPRESSION is read: a
  boolean input compared to a string literal (`inputs.dry_run != 'true'`)
  silently disables the guard, and the "dry" run pushed straight to prod with
  autodeploy. An ops spec relying on a dry run quotes the guard expression
  proving the flag suppresses the mutation, or tests it on a no-change state.
- A declaration is not a LOCATION. A field named in a type declaration says
  nothing about where the value sits at runtime: before a spec freezes an access
  path, recon quotes one live READ of it from a working consumer. A scout's
  `Project.timezone: string` froze `project?.timezone`; the value lives at
  `project.settings.timezone`, and the single-level chain would also have
  crashed every fixture lacking `settings`.
- A digest's COUNT of items says nothing about their SHAPE. Prescribing a
  per-item attribute (icon, label, order key, variant) requires that attribute
  traced to a quoted MEMBER of the artifact, never to a summary sentence about
  it — "6 nav items, 45 lines" licensed a spec ordering "the icon from the same
  set the neighbours use" for a registry with no icon field and no icon
  rendering anywhere.
- When a scout reports the STRUCTURE of an artifact that has more than one
  internal representation (table of contents vs body headings, schema vs
  migration, README vs code), the dispatch enumerates the representations first,
  scans EACH, and requires a per-item table with a SOURCE column. "Sections 1–9
  as expected" was read off the document's own TOC while the running text
  disagreed on three of them — the source contradicted itself, and the head
  nearly rejected a correct review finding as a false positive. Never accept
  "matches expectation" without the source named per item.
- A scout's aggregate is a claim about its own QUERY, not about the table. Every
  "N of M" entering a report states M from its own `COUNT(*)` of the base table
  and NAMES the join key, or a filtered or sampled query masquerades as a
  census: "26 runs over 87 days, one unclosed" became 27 unclosed once the run
  id was joined across all 152 run events — after the wrong figure had reached
  both the user and an owner-facing document. Two disagreeing counts are settled
  by re-measurement, never by picking the more plausible one.
- A threshold expressed as a FRACTION of another value is a claim about the
  SCALE. Recon reports the real distribution (min / median / top, plus the value
  for the class the threshold must NOT exclude) before the spec names a number,
  and the DoD exercises realistic magnitudes rather than fixture integers. A
  `0.6 × topScore` relevance floor over an un-normalised weighted-fusion sum
  rejected the diversity candidate on every realistic query, refilled the slot
  from the dominant document's overflow, and thereby REVERSED the per-document
  cap a previous MAJOR fix had introduced — invisible to six per-task runs and a
  green 1143-test suite, caught by an adversarial verifier reproducing
  production scoring. Where the distribution cannot be measured, the spec output
  is "measure first" or "defer", never a plausible-looking constant.
- A literal vocabulary, pattern list, or threshold table handed to an executor
  is a claim that the target module owns no equivalent: recon greps the module
  for a list serving the same role, and the spec orders REUSE or extension of it
  — a hand-written prefix list omitted a word the module's own catalog
  vocabulary already knew and broke a test protecting legitimate browsing, in a
  task whose stated purpose was to REMOVE divergent heuristics. In an inflected
  language the entries are ROOTS, not dictionary forms ("базе" does not start
  with "база"), and the DoD requires a root → inflected forms → predicate
  verdict table over EVERY entry, not a spot check of the entries that motivated
  the change. Both failures happened in one session, the second after the spec
  had been amended to fix the first.
- A regression guard is a claim that something WORKS TODAY. Every expected-pass
  example in such a list is RUN at the baseline commit during recon and reported
  with its literal verdict; an example that fails at baseline is dropped or
  becomes its own task, never a guard. One phrasing invented from plausibility
  turned an untouched pre-existing gap into a verifier FAIL and cost a round to
  tell the two apart.
- An owner-facing REGISTRY document (a session registry, handoff doc, ticket,
  task list) is secondhand at the level of a scout digest: recon its anchors AND
  its vocabulary against code before any spec inherits them. One carried four
  factual errors into speccing range — line anchors for a gate that in fact
  covered deletion only, a status label existing nowhere in the code, a webhook
  attributed to the wrong repo, stale migration numbers.
- When two scouts contradict each other, re-measure before publishing either —
  and re-check any fact already written into a deliverable earlier in the
  session against every later report covering the same ground. A gate attributed
  to one migration number was frozen into an owner-facing addendum before the
  second scout's deciding quote arrived with a different one, forcing a
  correction edit.
- Paths and identifiers enter a spec by PASTE from the scout report, never
  retyped. A plausible-but-wrong parent directory (same file name, same line
  number, same field content) is exactly the token that gets mis-recalled, and
  the executor pays for it at dispatch time.
- WHEN a destructive mechanism fires is never inferred from adjacent facts.
  "Deletions run only at the end of a successful scan" held for one removal
  class while policy-driven removals applied inline mid-run — the reassurance
  was already false when given. After any partial or aborted destructive run,
  measure the target state FIRST and report from the measurement, not the
  mental model.

## Enumerate the category — corollaries

- Reconcile the enumeration against Boundaries: a category member inside a
  do-not-touch file needs the boundary widened or an explicit deferred-risk
  note.
- Steps/DoD cover every member of a category Context declares, or record a
  per-member carve-out — a hand-narrowed Steps list silently contradicts the
  spec's own category.
- The rule holds inside one file: enumerate every read/render of the value in
  the touched file, never only the line a scout quoted. It binds IDENTIFIERS as
  well as rendered values — before ordering a delete, rename, or hoist, grep the
  identifier file-wide at spec-write time and cite every usage site; a spec that
  cited only the two declaration lines of a pair of function-local constants
  would have left two later calls of them as a ReferenceError.
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
- **Changing a predicate voids every blast-radius claim scoped to the old
  one.** Widening a gate from one value to a set, removing a narrowing clamp or
  intersection, and handing an axis to external data are the same move: the
  category is every value that ENTERS or LEAVES the predicate, and each is
  measured (holder count, affected rows) and ruled on before the Decision
  freezes. A clamp neutralises values silently, so removing one ACTIVATES every
  placeholder whose safety came from it — one such removal turned a "no
  audience stated" placeholder into a real company-wide grant on 257 documents,
  exposing a confidential file; widening an admin gate from one capability to a
  set of five granted 10 of 13 principals access they were previously denied.
  Both passed every per-task verification and surfaced only at the cross-task
  review axis, in both cases after the head had told the user the change had
  zero blast radius. Corollaries: a measurement taken for one task applies to
  every later Decision in the same session touching the same population; and a
  spec transferring authority over an access model names each axis separately
  (departments / roles / sensitivity / capability) and states for each whether
  it moves — data that expresses one axis is not authority over its neighbours,
  and including a silent extra axis reverted a deliberate earlier tightening.
- A hand-listed set of call sites — even a scout's — is not the category: grep
  the ACTION or SELECTOR name repo-wide and classify every hit (manual vs
  automatic, on-surface vs off-surface). Two sessions running, a spec that
  enumerated consumers inside the anchor file alone left a sibling call site
  un-wired on the same user surface.
- Removing an entry from a REGISTRY (nav item, feature flag, enum member, route
  table, capability map) enumerates every call of the registry's ACCESSOR keyed
  by that id — `getX('id')`, `byId['id']`, `find(x => x.id === 'id')` — in
  addition to importers of the module and literal hits on the entry's own
  strings. An accessor lookup matches none of those greps and crashes every
  page at module load.
- When a fix changes a QUESTION, COUNT, or STATE the product surfaces in more
  than one place, the spec anchors on the shared MODEL that computes it and
  enumerates every consuming surface — screens, notifications, assistant
  prompts. Fixing the screen the complaint came from is a partial fix by
  construction: the other surfaces kept nagging about a question that screen
  had already resolved.
- A behavior change widens Boundaries to every piece of COPY that describes the
  old behavior — grep the old promise in the touched component. A Boundaries
  line banning string changes beyond the button and toast froze an adjacent
  help paragraph that now promises the opposite of what the feature does.
- A NEW delete/retract path enumerates every existence or cardinality INVARIANT
  any migration asserts about the target table, and states which EDGE enforces
  it: an invariant enforced on one transition is silently unguarded on all
  others, so the exact defect the migration was written to prevent becomes
  reachable by one UI click. Related: a `CREATE OR REPLACE` superseding an
  earlier definition is itself a blanket change over an enumerated category —
  diff the replacement against the CURRENT live definition and carry forward or
  explicitly revoke each conditional carve-out with a Decision line, including
  carve-outs that live in a PREVIOUS migration rather than the edited file.
- Before a Decision orders NEW behavior on an existing failure branch, grep the
  tests that already assert what happens there. A green assertion of the
  opposite is a product decision with an owner: cite and override it
  deliberately, or scope the task to exclude it. Listing those tests as "must
  stay green" while mandating the contradicting behavior puts the executor in
  an unresolvable bind — and the silence being "fixed" may be the tested,
  intended product behavior.
- Affected TESTS are enumerated by IDENTIFIER, never by user-facing literal:
  grep the flag, predicate, constant, component and type names the diff touches,
  plus the importers of every touched file. A literal-string sweep misses a test
  that drives the removed branch through a mocked input (mocked route params, a
  stubbed store), and a scout's test list is a seed, not the category — the spec
  states the runnable grep and orders the executor to re-enumerate rather than
  inherit the count. Two sessions, two projects, same shape: a hand-listed
  seven-test set missed an eighth using the same fixture; a literal grep missed
  a view test exercising the deleted branch via mocked search params.
- The same enumeration feeds the Boundaries FILE ALLOWLIST, not only Steps.
  A changed type's mock fixtures and constructors are category members, so an
  allowlist derived from the Steps list forces the executor to choose between
  the spec and a compiling tree — grep the constructors of every changed type
  before freezing Boundaries. Reconcile the allowlist against every behavior the
  spec's own Decisions require: a Decision changing what an endpoint RETURNS
  pulls in the module DECLARING its response type — an excluded `response_model`
  schema file forced the executor to encode structured data (skipped ids and
  reasons) into a free-text message field.
- A spec that CHANGES a user-visible literal (href, label, copy) makes the
  literal's own grep Step 0, across sources AND tests, classifying every hit as
  rewrite / test-to-update / legitimately-staying, and declares the
  test-to-update set an authorized Boundaries extension. Otherwise "do not
  change existing assertions" + "0 failed tests" + the rewrite order are
  mutually unsatisfiable and the executor correctly stops with zero changes: a
  test pinning `href='/task/t1'` was outside an allowlist that named only source
  files. Word the assertion rule as ANTI-WEAKENING from the start, never as a
  freeze.
- A table written through an UPSERT has TWO column lists, and a spec naming only
  one is half a spec: Steps name the `onConflictDoUpdate` SET payload alongside
  the `values` payload, and the DoD asserts a key-set diff (`keys(set)` equals
  `keys(values)` minus the conflict target) rather than the presence of the
  specific new field. Two specs added columns to a one-row-per-week upsert, so
  the INSERT path carried them and the UPDATE path — the NORMAL path there — did
  not; clearing never wrote the null. Every test stayed green because the DB is
  mocked, and an executor's "Noticed, didn't touch" caught it.
- In a hand-maintained schema or types file, one entity can be declared MORE
  THAN ONCE: the category is every declaration, enumerated by grepping the
  entity name file-wide with the executor reporting the count. A spec named the
  `tasks` block; the converter imported a second hand-maintained `TaskDB`
  interface in that same file, so the column landed in one declaration and tsc
  stayed silent.
- Deliberately EXEMPTING a sibling consumer of a shared constant or predicate is
  a behavioral claim, not a scoping decision. Enumerate the consumers and
  require one end-to-end probe of user-visible output per consumer, the exempted
  ones included, and pin the exempted behavior with a test rather than a
  paragraph of reasoning. A spec fixed a topic-blind shortcut at the pre-search
  layer and exempted the renderer as "topically correct by construction"; the
  renderer read the same widened constant with no topic guard and changed which
  questions get a title list instead of model prose — judged GOOD on
  arbitration, but reached by accident and guarded by nothing.
- A user-visible CONFIRMATION — or any acknowledgement, error, or status the
  actor sees — is a category of SURFACES, not a message: enumerate every one
  (inline message, toast / callback answer, edited original, removed keyboard,
  follow-up prompt) or write "all surfaces" explicitly. A requirement anchored
  to a single builder leaves the siblings contradicting it: a toast kept
  soliciting a comment the flow no longer captured, a UX dead end that passed
  its per-task verifier.
- Adding a PERSISTED field is a round-trip category, not a write-path category:
  enumerate every writer AND every query that lists columns for that table,
  repo-wide by grep, and put one test through the query-BUILDING layer into the
  DoD. Fixtures construct the object with the field present by type definition
  and bypass the query layer entirely, so a green suite proves the type
  compiles, not that the value survives persistence: a column shipped with a
  migration, both row types, converters, UI, filters and 24 green tests, was
  absent from all three SELECT column lists, and simply never came back after a
  reload.
- A new CHILD table is a new member of the parent's children category, and that
  category's existing cascades are its consumers: Steps enumerate every existing
  soft-delete, archive, purge and ops path over that parent's children and add
  the new table to each, with a test per path. Skipping it leaves the new rows
  live under a soft-deleted parent — the same orphan shape an earlier probe had
  already measured in that repo.
- The no-unconsumed-surface rule binds at FIELD granularity, not only at module
  or query granularity: for every field a spec adds to a validator, type, or
  metric input, Decisions name its producer AND its consumer task, and a field
  whose producer is deferred to a sibling task is written into that sibling's
  spec as a required step. Two deferrals nobody carried forward reached the final
  review as dead surface in a single package.
- When the category is used to GENERATE inputs (synthetic queries, property-test
  fixtures), check the generated members against every higher-priority
  dispatch/routing rule before freezing the property: one generated string that
  happened to equal a real record's title was intercepted by an exact-title
  route, making the property unsatisfiable as written. Either exclude the
  colliding members or mandate an intent guard in the test up front.
- When stored state re-enters a processing stage, classify every field as that
  stage's INPUT or OUTPUT and replay only inputs; feeding derived outputs back
  as discovery data can make restrictive classifications impossible to heal.

## Divided ownership — two owners, one behavior

- When a spec prescribes a post-success UI state AND a completion callback to
  the parent, it states the MOUNT LIFETIME explicitly: which component owns
  unmount, and that the result message survives it. Default to giving the parent
  no unmount hook. A component ordered to collapse itself while its parent was
  ordered to unmount it raced its own result rendering — a conflicting resubmit
  left the step unchanged and the block simply vanished. Both final reviewers
  found it independently; every per-task verifier passed it.
- Reusing a user-facing component on a NEW surface silently reuses its COPY,
  which encodes the first surface's time scale and question framing. The reuse
  spec adds a step diffing every shared string against the new surface's own
  vocabulary, parameterizes the ones that differ, and greps the destination
  screen for near-duplicate questions. A node built for a daily surface kept
  naming the day on a weekly one and re-asked a question that screen already
  asked.

## DoD gates

- A DoD reusing a repo-wide gate (lint, typecheck, pattern scan, browser
  console/log noise) snapshots its pre-existing state and asserts no NEW
  violation from the touched files, never absolute green. For logs, capture
  both counts and distinct message texts per route; "no new class" is stronger
  than an unmeetable zero over known noise.
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
  pin at least one literal boundary value independent of the constant. Keep the
  probe mandatory for gate-invariant specs and NAME the test expected to die:
  its real value is not confirming coverage but exposing tests that assert an
  unreachable state. A probe that kills nothing has proven the guard is
  untested and possibly unreachable — that finding goes to the final review,
  never into a green checkmark. When a spec ruling is a CONJUNCTION (A and B ⇒
  refuse), the DoD demands a test hitting exactly that conjunction, not each
  side separately.
- Exact-answer, classifier, routing, and language-boundary changes need
  adversarial controls, not only happy paths. The DoD includes: positive cases
  for each intended spelling/script, negative cases where the token is only a
  topic mention or is negated, absence/blank controls, duplicate/ambiguous
  identity controls, and boundary cases using the runtime's real Unicode rules
  (`\p{L}`/`\p{N}` lookarounds for Cyrillic/Russian classifiers instead of
  ASCII `\b`). A route keyed by "exact match" also tests the collision where
  generated or stored text equals a real title/command.
- A DoD grep asserting a change in a specific file presumes that file must
  change — for a conditional step, assert the resulting behavior, not the
  diff's location.
- A literal command in a DoD or verifier prompt is a claim too: dry-run it
  against the real dispatch/selector logic it routes through (mode flags, env
  precedence) and the actual file layout (a blank line eats a `grep -A`
  budget), or state the content assertion and let the verifier choose the
  command. A reachable CLI does not prove an importable module path; dry-run
  the exact resolution/launch command before hardcoding either.
- Npm scripts hide network and install behavior behind nested `npx` calls.
  For no-network/no-install tasks, inspect the exact script chain before the
  first run, prove each `npx` binary is project-pinned or already cached, and
  set the offline/no-install environment in the literal DoD command. Any
  "will be installed" warning is a stop condition even if the command exits
  zero.
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
- A DoD may not prescribe RUNNING a migration, SQL, or any external-system step
  until recon has NAMED the venue that runs it (a CLI config, a compose file, a
  migrate script, a reachable connection string). Absent a venue the DoD
  becomes three parts: a structural text test following the repo's existing
  convention, a unit-level test of the RULE itself, and an explicit
  "unverifiable here" line naming what only the operator can confirm. Recon
  probes liveness cheaply (one trivial query) BEFORE any DB-dependent stage is
  built — a paused or unreachable environment otherwise reads as code failure.
- Unit tests, typecheck, and lint all pass while the PRODUCTION BUILD fails:
  any diff touching app-router pages or routes (a new `useSearchParams` /
  `usePathname`, dynamic APIs, client/server boundary edits) puts the
  production build in the integration gate. jsdom never exercises prerender, so
  3849 green tests plus clean tsc and lint shipped a build that died at static
  prerender and reached the owner.
- A numeric DoD invariant cites the LITERAL output line it is read from, never
  a paraphrased metric name: "still 80 routes" is ambiguous when the
  static-generation counter (X/Y) and the route table (all routes incl.
  dynamic) are different numbers, and an executor cannot reconcile a metric the
  DoD never located.
- A CONDITIONAL Step carries its conditional member into the DoD's file
  allowlist — otherwise the executor rightly follows Steps and touches a file
  the DoD forbids.
- Every full-suite verification tees to a log file. A one-off failure whose
  identity is lost to summary-only greps escapes unnamed session after session,
  and an unnamed flake cannot be excluded from the next gate.
- A DoD grep with an expected COUNT — especially zero — is a claim that the
  token is unique to this package. Run it at spec-write time against the current
  tree and pin the expectation to the measured baseline, or scope the path and
  pattern to the package under change. An unmeasured zero-match gate on a common
  prop name was unsatisfiable: an unrelated pre-existing component owns the same
  prop plus two call sites, so meeting the gate meant renaming a foreign
  component's API — a refactor the same spec's Boundaries forbade. The fixer
  correctly refused and rescoped the grep.
- Reconciling a gate against the spec's own Steps is a PRE-DISPATCH PASS, not a
  memory check: re-read Steps for anything that contradicts each gate (a test
  asserting the banned token's absence, a conditional step touching a
  DoD-forbidden file) with the gate text in front of you. The token-ban-grep vs
  negative-assertion contradiction is documented above and still shipped again —
  a rule known but unchecked is a rule not applied.
- A test double that RECORDS a write without APPLYING it makes every round-trip
  bug in that channel invisible, and the tests written against it feel thorough
  — the same family as the in-memory-DB rule below. Before ordering two-way sync
  with any external channel (URL/router, storage, clipboard, DB), establish
  whether the repo's existing double closes the loop; if it only records, the
  spec mandates a loop-closing double and the DoD says so. A router mock that
  recorded the navigation call without updating what the read-back hook returns
  shipped a panel that reopened itself on every close, past three new tests and
  a full green suite; the reviewer proved it by copying the test file aside and
  making the mock apply the URL — two immediate failures.
- A green in-memory DB double proves nothing about error recovery inside a
  transaction: a common fake does not model transaction abort, so a
  catch-then-requery is green in tests and unreachable on the real engine
  (which fails the whole transaction with 25P02). Require a no-raise construct
  (a target-less `ON CONFLICT DO NOTHING` covers ALL unique constraints) or
  real-engine proof — and check whether an embedded/real engine is actually
  available before accepting a note claiming it is not.
- Fixtures for classification or policy tests are DERIVED from the real parser,
  never hand-written: a hand-written fixture encodes the very assumption under
  test and is how a blocker survives review (3 hand-written departments where
  the parser emits 10, sensitivity hard-coded false on a title the parser
  flags). A test rename that drops a property name is a warning sign.
- Any test edited OUTSIDE the spec's named files is reported per-file with the
  old and new assertion quoted, and the final review re-derives whether each
  edit preserved the property the test guarded. "Mechanically had to update
  these tests" is the exact phrasing under which a protection dies quietly —
  nine of ten such edits were mechanical and the tenth killed the only guard on
  a wiring path, which then passed with the wiring deleted. When a spec allows
  DELETING a test file with assertions migrated elsewhere, the DoD demands a
  title-by-title migration table in the report; the net suite-count delta is
  the tripwire.
- A verify or smoke SCRIPT is itself an artifact with a DoD: one green
  end-to-end run against a real target before the package ships. "Compiles and
  reviewed" is not verification for a runner.
- A verification command is checked against the real artifact's shape: `grep`
  over a listing containing non-ASCII filenames goes binary and reports a false
  MISSING — use `grep -a` or extract first. A false MISSING wastes rounds; a
  false PASS would be worse.
- In a live check never call auth sign-out (or use a local-scope variant) while
  a browser session of the same user is under test; every PASS needs a URL
  assertion plus a screenshot cross-check.
- A permission mismatch on DELETE fails SILENTLY under row-level security:
  unlike INSERT/UPDATE, an RLS-filtered DELETE is not an error — it returns
  success having deleted zero rows, so the client reports success and the row
  survives a reload. Any spec wiring a client delete quotes the DELETE policy's
  role predicate and the UI's write gate side by side, requires a returning
  select so a zero-row delete is detectable, and puts a zero-rows-affected test
  in the DoD.
- A Boundaries list is a claim about blast radius — verify it against the TEST
  HARNESS, not only the source tree. A change adding SQL that references a
  column an in-memory fixture may not model (a fixture that skips every
  migration matching a keyword) needs that fixture file inside the allowed set,
  or the spec states the seam keeping the new SQL out of fixture-backed tests.
  Otherwise the executor implements the spec verbatim and watches dozens of
  unrelated tests fail.
- Applying a migration is an ops spec with three measured preconditions, all
  read from the migration's own text rather than a summary of it: census every
  object it names and confirm each exists (one `REVOKE` on a missing table
  aborts the ENTIRE transaction and silently applies nothing), count the rows
  every mutating step would touch BEFORE applying so a data-loss fork is
  decided on a measured number, and record the post-check query's baseline
  first so the verification is demonstrably capable of failing. Migration
  numbers are derived at execution time and never reserved for unwritten future
  work — an operator applying in numeric order cannot un-see a gap.
- Verbatim text you author is a claim at every level. A composite key uses a
  separator that cannot appear in either component; user-facing string
  typography is checked against codebase convention before freezing (mixed
  quote styles reached an executor that had to hex-dump them); and escape
  sequences or control characters are NEVER written literally into an agent
  message — they arrive mangled, the order becomes self-contradictory, and an
  executor briefly wrote a raw control byte into source. Spell them in words
  and add a grep-able acceptance check for the exact source text.
- For an outcome a caller must not ignore, prefer a TYPED ERROR over an in-band
  sentinel. Signalling "skipped" by returning the conflicting record made
  ignoring the outcome the path of least resistance: an access-granting UI
  printed a success toast carrying a DIFFERENT person's data and wrote a false
  audit event. The sole context that may continue catches it explicitly.
- A permission-gated UI spec states loading, granted, and denied behavior for
  EVERY control — hidden vs disabled vs read-only, save footers and bulk actions
  included; kin of the failure-branch-UX rule.
- When Steps contain both a costly external call and a cheap terminal guard,
  order the guard FIRST and explicitly: executors follow Steps literally. Any
  fix premised on an EXTERNAL system's capability (an export format, an API
  surface, a quota, a permission) gets that guard as Step 0 with an explicit
  STOP clause — reproduce the capability live against the real target before a
  line of code. One such guard failed in minutes (the export hit the same size
  limit the fix assumed it would dodge), killing a wrong premise for the price
  of one call; a follow-up probe then found the path that did work.
- "Reuse the existing pattern at X" transfers the SHAPE, not the preconditions
  that make the shape correct — the spec states WHY X is correct so the
  executor can check those preconditions still hold. An idiom sound only
  because it runs OUTSIDE a transaction and issues zero queries after failure
  became a latent bug the moment it was copied inside a BEGIN with recovery
  queries added. Such an instruction also NAMES the property being borrowed
  (rollback mechanics, retry shape) and states the new code's own failure
  contract separately, because the two can conflict: "roll back exactly the way
  the code next to it does" carried the neighbour's swallowed repository error
  into new code, so the caller's catch never fired and the UI showed success on
  a write that had been undone. A neighbour's latent defect is invisible to the
  per-task verifier, since the spec itself sanctioned the shape.
- Anchor re-verification covers the DOMAIN VOCABULARY of acceptance criteria,
  not just file:line anchors: every status, enum member, and field name an
  acceptance bullet names must grep to a real declaration. One acceptance
  bullet referenced statuses that exist nowhere in the codebase and survived
  two package re-verifications.
- When an executor claims a spec-authorized DEFERRAL, the verifier quotes the
  exact deferral sentence and checks WHAT it defers — a single out-of-scope
  sentence in an addendum was stretched to cover the addendum's whole mandate.
  When a spec has an addendum with a revised goal, tell executors the
  addendum's acceptance bar supersedes and any out-of-scope claim must quote
  its sentence in the report.
- **A check proves nothing until its VENUE can fail for the reason under
  test.** Four preconditions, each established this session before a command or
  probe is frozen into a DoD. (a) The RUNNER is a codebase fact: read the
  repo's own scripts (`package.json`, the task runner, the CI config) for the
  canonical gate instead of writing the one you expect — a spec froze
  `npx vitest run` where the gate was `npm test` (build + `node --test` over
  `dist`) — and dry-run the literal command against the real tree, since a
  pre-existing basename collision left bare `pytest -q` unable to collect at
  all. (b) The HARNESS ENTRY POINT traverses the layer that WRITES the state the
  feature reads: a probe script that bypasses the webhook owning those writes
  exercises the fallback path, so its green is about the wrong mechanism. (c)
  The probe's SURFACE and PRINCIPAL match the real usage scenario — a
  group-surface probe hard-gated to public documents produced a FALSE regression
  that reached the owner-facing QA report until re-probed as a DM by the
  department-scoped principal testers actually use. (d) The ARTIFACT under test
  is the freshly built one: a reused dev/preview server keeps serving the
  previous build, and a green suite over source says nothing about the `dist`
  the probe loads — rebuild, restart, or assert the artifact's hash/mtime first.
  Where a precondition cannot be met, the DoD says "unverifiable here" and names
  what only the operator can run; extending the harness (in-transaction writes)
  is the alternative, never a green on the fallback. Two corollaries. In a repo
  not exercised THIS session, prove the gate runs at all before writing a
  check-driven spec — one green baseline run of the repo's own runner, or an
  explicit "unverifiable here" declared up front: a venv holding packages for a
  python3.13 the host had since removed, with pytest in neither the venv nor
  `requirements.txt`, cost three rounds of venue repair after the specs were
  already written, and a broken venue turns every executor into a blind one.
  And a before/after or BASELINE probe pins its artifact to a COMMIT: assert a
  clean tree at the expected sha, or build from a clean checkout of the base,
  before building. Precondition (d) forbids a stale artifact; the inverse is
  equally fatal — a baseline build off a dirty tree compiled another session's
  uncommitted fix for the very defect being baselined and reported it absent,
  which as a "before" measurement would have been a false before/after claim.
  Venue facts also expire: re-prove them for each dispatch, and never place a
  multi-dispatch venue under `/tmp` or session scratch that an OS cleanup can
  erase; use durable cache storage plus an explicit failure escalation.
- A user-flow DoD is a scenario matrix, not one happy-path script. Include the
  production-relevant configuration and principal, cold start, plausible
  wrong-order actions, and sibling paths of the same bug class. Assert the
  resulting artifact's content/state directly; a success label, status enum,
  exit code, or "done" message is not proof that the requested effect survived.
- A fix answering an owner's complaint about a surface they cannot see is
  verified against the branch THEY hit — their role, their data distribution —
  not against the generic case, and the report states the branch condition. A
  restored direction selector passed every gate while the owner still saw
  nothing: all of his members hold admin roles, for which the selector is
  contractually absent.
- Nondeterministic answer paths (anything LLM-mediated, retry-driven, or
  timing-sensitive) need N≥3 repeated runs before any zero-occurrence claim: a
  "0 safe-refusals across 59 probes" result was refuted by a re-run hitting one
  on the same question. One green pass proves possibility, never absence.
- When two hypotheses are indistinguishable through the failing surface (stale
  deploy vs missing env/creds vs broken code, and the deployment exposes no
  version), probe a read-only SIBLING route sharing the failing path's helper
  chain: a 200 carrying the real record proves env, DB, and credentials live and
  isolates the deploy by elimination — faster than adding a version endpoint
  mid-incident.
- A gate is never edited to make it pass. When a size, lint, format, or
  file-count guard trips, the fix is the code — never raising the limit, adding
  an allowlist entry, or rewriting the hook command to route around an
  unconfigured environment. State it in Boundaries whenever the DoD runs a
  project guard, and have the verifier diff the guard's own config against the
  base commit.
- A project's git hooks can fail INSIDE a worktree while passing in the main
  checkout (formatters resolving workspace paths from the repo root), blocking a
  worktree executor's commit on a defect that is not its own. Name the fallback
  in the envelope — run the fixer from the main checkout, re-stage, commit — so
  the executor never disables the hook to get unstuck; the same envelope tells
  it to activate the repo's toolchain environment before running git or hooks
  rather than compensating with ad-hoc PATH edits.
- A set of screenshots claiming N distinct states is not evidence until the N
  files are proven distinct (`shasum -a 256 <dir>/*.png` — every hash unique):
  an unscoped full-page capture of a view that renders every state at once
  yields byte-identical files. Scope each capture to its subject, and wait for
  animations to finish — a visibility assertion resolves mid-transition, so the
  shot lands on a half-rendered element.
- A performance DoD states the measurement CONDITIONS, not only the target
  number: profiling overlays, per-event logging, and an open inspector inflate
  the very numbers used to judge the fix. Measure with instrumentation off,
  against a recorded baseline, removing one suspect at a time.
- **Synthesis grounding (full rule; SKILL.md keeps the headline).** When the
  artifact is a synthesis from sources (guide, digest, summary of advice), the
  spec names the deepest available source of truth (transcript over retelling,
  original over derived corpus) and the DoD verifies claims against it verbatim:
  claims carrying a pointer (timecode, link, file:line) are checked AT the
  pointer; a search-based sample covers the rest. The verifier diffs claim
  against quote, watching the connectives and quantifiers added during
  compression ("when", "always", "therefore", "most") — distortion is born in
  connective tissue the source never had. Agreement between two derived copies
  proves nothing; an unexecuted pointer is not evidence. Confirm the assumed
  source IS the source before synthesizing: dispatch relevance-check scouts
  across ALL candidate sources in parallel, each told to confirm or refute
  relevance first and stop early if irrelevant — a plausibly-named file can be
  the wrong corpus.
- **Visual DoD (full rule; SKILL.md keeps the headline).** A visual change's DoD
  compares a live headless screenshot against the design target (or pre-change
  baseline) and names the specific differences to check — spacing, color, copy,
  state — never "looks right". A Fable-class head reads dense raw screenshots
  directly; a non-Fable head delegates to a vision-capable subagent instructed to
  crop and zoom into unclear regions. A pass without a rendered comparison is
  unverified, like a claim without a quote. Not only fidelity: typecheck, build
  and HTTP-200 stay green while the rendered page crashes at runtime (a
  hooks-order violation, a hydration error), so any UI-behavior change needs a
  rendered-browser check, and any long-running external-process integration (a
  spawned CLI, a dev server) keeps a live smoke stage — static review does not
  close runtime acceptance criteria. Cheap default: `npx`-cached Playwright (the
  cached ms-playwright Chromium, not a system-Chrome `channel` — a sandboxed
  shell SIGKILLs the system browser) against the dev server, re-driven
  independently by the verifier. Before using `curl` as the smoke check, confirm
  the rendering model: a server-rendered route executes the real render plus its
  DB queries, so a 200 with the expected content is a strong crash check; a
  client-rendered app returns near-empty HTML and proves nothing — drive a
  headless browser. Either way client-prefilled values and client-only
  interactivity never appear in server HTML — verify those by reading the wiring,
  not the curl body. A mockup is a claim about its item inventory: diff its
  routes/columns/tabs against the live category and decide every mismatch before
  reproducing it. If both a container and its contents are fixed, the executor
  measures and escalates an impossible fit instead of silently shrinking an
  accepted element. Geometry is measured, never guessed: every visual DoD sets a
  usability floor (minimum fully-visible items or px window at the initial state
  — with fixed siblings the leftover width is computable at spec time, so compute
  it); a height-compaction spec cites a measured per-section height map of the
  offending container, never a viewport-cropped screenshot (the real hog can sit
  below the fold); a grid/column reorder pins the class-string→track mapping or
  asserts rendered widths — DOM-order assertions pass in jsdom while the wrong
  column gets the track.
- A percentage-based deletion or stop threshold cannot distinguish
  absence-driven removals (dangerous: an empty upstream response) from
  policy-driven removals (intended: a gate tightened). When such a rule fires,
  triage by joining the removed ids against the discovered and rejected sets
  before treating it as an incident; the decision to proceed stays with the
  owner.
