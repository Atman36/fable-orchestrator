# Model roles — strengths, limits, refusal behavior (as of 2026-10)

Read this before routing anything off the default table in SKILL.md § Model
routing: an unusual role, an escalation, a first-touch decision in a sensitive
domain, or a model you have not used this session. The table stays the default;
this file is why the table looks the way it does.

Current automatic pool (owner policy; verify exact live availability):

| Tier | Exact OMP selectors | Effort / role |
|---|---|---|
| Small | `openai-codex/gpt-6-luna`, `anthropic/claude-haiku-5-5` | bounded, auto-verifiable work |
| Medium | `anthropic/claude-sonnet-5-5`, `openai-codex/gpt-6.1-sol` | Sonnet/Sol medium for normal work |
| High | `openai-codex/gpt-6.1-sol`, `anthropic/claude-opus-5-5` | Sol high/xhigh; Opus planning/review, never cheap work |

Codex-native default: **Sol leads and builds → Luna clears bounded volume →
a fresh Sol or Opus reviews critical output.** Claude-native default:
**Opus carries planning/review risk → Sonnet builds → Haiku clears bounded
routine work.** Cross-family review is a deliberate independence tool.
Fable and Astra below require explicit opt-in; neither is an automatic tier.

- **Fable 5 — explicit opt-in architect & inventor.** Hardest, newest, most ill-defined work:
  inventing products/systems, agent architectures, unexpected approaches,
  codebase-wide investigations, long-horizon autonomous runs, dense
  visual/product work. Spend it on creating
  projects, specs and architectures — never routine code, never first-touch for
  simple tasks. Safety classifiers
  (offensive-security, biology/life-sciences, summarized-thinking-extraction)
  can reroute benign requests to Opus 5.5 as a `refusal`, not an error — route
  first-touch architecture/spec work in those domains straight to Opus.
- **Opus 5.5 (`anthropic/claude-opus-5-5`) — senior reviewer / tech lead.** Complex planning,
  architecture review, debugging, and carrying high-risk work to done; require
  honest uncertainty and evidence. The
  premium reviewer, the risk-tier route, the fallback when Fable refuses;
  never assign cheap routine work to Opus. Needs
  clean scope — given noisy context it executes the noise literally. When Opus
  is the head, use a fresh same-family context for final review only; an
  architect consult returns options, trade-offs, and evidence, never the
  decision; keep bulky raw output in report artifacts; send dense visual
  comparisons to a vision-capable agent with crop/zoom instructions.
- **Sonnet 5.5 (`anthropic/claude-sonnet-5-5`) — main Claude builder.**
  Code, repo changes, tool use, executing a clear plan; the default Claude
  executor. Escalate architecture, compliance-sensitive and cross-service
  work instead of trusting the default.
- **Codex family (native hierarchy or via Codex CLI).** Metered quota — the
  invocation, cost, and safety rules in `references/codex.md` apply to every
  CLI call. Choose by the task's clarity, latency, volume, and cost of error:
  - **`openai-codex/gpt-6.1-sol` — lead, builder, senior reviewer.** Own task
    understanding, decomposition, architecture/product forks, conflict
    resolution, complex or ambiguous high-value work, security, research, and
    final review. Use medium for normal implementation; high/xhigh for
    demonstrated complexity or risk. Use a fresh context for acceptance.
    Preserve the exact available route; do not invent Luna or Terra variants.
  - **`openai-codex/gpt-6-luna` — bounded worker.** Clear, repeatable
    extraction, classification, routing, mechanical checks and focused coding
    with a precise acceptance gate. Give Luna a narrow contract; do not make
    it resolve product or architecture forks; escalate to Sol when the task
    changes architecture, security posture, scope, or remains ambiguous after recon.
    Observed Luna failures, three sessions: a positional insert into a
    ~1400-line doc corrupted it; reads of long single-line CSS came back
    truncated, with cited lines beyond the file's length; a screenshot
    verifier returned UNCLEAR on every row without opening the images. Route
    large-file inserts to a deterministic anchored script plus a diff check
    (or Sol), long-line census to grep-based extraction with cited line
    numbers checked against file length, and image judgments to a reliable
    vision route — Luna gets only metric/JSON checks there. A Luna report
    with UNVERIFIED core sections goes to Sol once with the same spec.
- **Haiku 5.5 (`anthropic/claude-haiku-5-5`) — bounded junior.** Classification, extraction, simple edits, short
  summaries, routing, mechanical checks. NOT for architecture, complex
  debugging, large ambiguous tasks, or expensive-mistake decisions; drifts from
  instructions in large contexts.

- **GLM-5.3-Flash (`zai/glm-5.3-flash`) — paused, not in the current pool.**
  Owner does not use it as of 2026-10-26: never route to it, even when the
  catalog lists it, until the owner re-enables it; a re-enabled Z.ai route is a
  data-egress decision.
- **Astra (`gpt-6-astra`) — explicit opt-in execution escalation.** Terminal,
  recovery and stateful unknown environments; never mechanical routine work.

**Exact routing.** Catalog presence is not successful inference. Tool role
labels do not guarantee per-dispatch model selection: check supported pinning
or overrides and report the actual route. Observed in four OMP sessions: the
native `task` tool accepts `model` only for `seance`; scouts and task workers
run on the host default route. For an authorized OMP smoke, and as the worker
runner when the exact route matters, use the installed
`omp -p --model <exact-provider/model>` with a temporary configuration overlay
`retry: { modelFallback: false }` (a worker run only after its smoke); do not
resume a session or use fuzzy ids. Otherwise dispatch natively, record the
requested route as unpinned, and ledger the self-reported model.
Judgment separately requires `modelRoles.judge: openai-codex/gpt-6-luna` and
`retry.fallbackChains.judge: []`; do not append a chat thinking suffix to judge.

**Free OpenRouter pool** (owner-listed 2026-10-26; all three ids present in the
OMP catalog that day — presence is not inference, smoke each before use):

- `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` — text, 1M context, the
  strongest free reasoner (55B active MoE). Narrow cross-checks, second
  opinions, long-context extraction, bounded drafts behind a fixed gate. Never
  acceptance, never alone on the critical path; tests it authors get a realism
  review (production-imported units, request-derived mocks).
- `openrouter/nvidia/nemotron-3.5-super-vl:free` — images, screenshots,
  documents, video → text (12B active). Visual triage only; its verdicts fall
  under § Free vision verdicts.
- `openrouter/nvidia/nemotron-3.5-lightning:free` — 3B active, high
  throughput. Bulk classification or extraction with a deterministic check;
  no judgment, no code edits.

The provider logs free-endpoint traffic and asks for no confidential data or
personal data. Send only public, synthetic, or masked material unless the
owner authorizes private code or data for that route in the current session;
screenshots with personal data never go there. The catalog also lists paid
variants of the same models: pin the `:free` suffix with
`modelFallback: false` and never fall back to a paid variant silently. A
`:free` variant can be retired without notice; re-check the catalog each
session.

**Smoke before routing.** Before the first real dispatch on a pinned model,
and before advising any production model switch, run one trivial call on the
exact route (same CLI, auth kind, and model id) and quote its result; an
account can reject a model the table lists. Match the planned capabilities:
a tool-using route must execute a harmless real tool call and deliver a readable
artifact through the named report writer. A text-only response proves neither.
Record observed latency and remaining runtime budget; a passing smoke proves
capability, not that a larger task will meet its deadline.

**Free-route throughput.** Free routes pass smoke and still fail at task
scale: every free-route dispatch carries an explicit short deadline, a
checkpoint-commit instruction, and an artifact-existence check before any
successor dispatch. When a free worker stalls or times out on the critical
path, move that work to a stronger route; keep free models for narrow
cross-checks.

**Free vision verdicts.** A free VL model's verdict — PASS or FAIL — is a
hypothesis, never acceptance evidence: open the actual image behind every
security, P1/P2, or FAIL claim, check the capture method (masks, fullPage),
and re-verify its rows on a reliable vision route before acceptance.
