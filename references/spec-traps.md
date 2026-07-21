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
  than one assumed-supported mechanism.
- A dry-run / no-op flag is unverified until its GUARD EXPRESSION is read: a
  boolean input compared to a string literal (`inputs.dry_run != 'true'`)
  silently disables the guard, and the "dry" run pushed straight to prod with
  autodeploy. An ops spec relying on a dry run quotes the guard expression
  proving the flag suppresses the mutation, or tests it on a no-change state.
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
  pin at least one literal boundary value independent of the constant. Keep the
  probe mandatory for gate-invariant specs and NAME the test expected to die:
  its real value is not confirming coverage but exposing tests that assert an
  unreachable state. A probe that kills nothing has proven the guard is
  untested and possibly unreachable — that finding goes to the final review,
  never into a green checkmark. When a spec ruling is a CONJUNCTION (A and B ⇒
  refuse), the DoD demands a test hitting exactly that conjunction, not each
  side separately.
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
- A permission-gated UI spec states EVERY control's state in the ungated
  variant — hidden vs disabled vs read-only, save footers and bulk actions
  included; kin of the failure-branch-UX rule.
- When Steps contain both a costly external call and a cheap terminal guard,
  order the guard FIRST and explicitly: executors follow Steps literally.
- "Reuse the existing pattern at X" transfers the SHAPE, not the preconditions
  that make the shape correct — the spec states WHY X is correct so the
  executor can check those preconditions still hold. An idiom sound only
  because it runs OUTSIDE a transaction and issues zero queries after failure
  became a latent bug the moment it was copied inside a BEGIN with recovery
  queries added.
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
- A percentage-based deletion or stop threshold cannot distinguish
  absence-driven removals (dangerous: an empty upstream response) from
  policy-driven removals (intended: a gate tightened). When such a rule fires,
  triage by joining the removed ids against the discovered and rejected sets
  before treating it as an incident; the decision to proceed stays with the
  owner.
