# Model roles — strengths, limits, refusal behavior (as of 2026-10)

Read this before routing anything off the default table in SKILL.md § Model
routing: an unusual role, an escalation, a first-touch decision in a sensitive
domain, or a model you have not used this session. The table stays the default;
this file is why the table looks the way it does.

Current automatic pool (owner policy; verify exact live availability):

| Tier | Exact OMP selectors | Effort / role |
|---|---|---|
| Small | `openai-codex/gpt-6-luna`, `anthropic/claude-haiku-5-5` | bounded, auto-verifiable work |
| Medium | `zai/glm-5.3-flash`, `anthropic/claude-sonnet-5-5`, `openai-codex/gpt-6.1-sol` | low/medium for bounded GLM artifacts; Sol medium for normal work |
| High | `openai-codex/gpt-6.1-sol`, `anthropic/claude-opus-5-5` | Sol high/xhigh; Opus planning/review, never cheap work |

Codex-native default: **Sol leads and builds → Luna clears bounded volume →
a fresh Sol or Opus reviews critical output.** Claude-native default:
**Opus carries planning/review risk → Sonnet builds → Haiku clears bounded
routine work.** Cross-family review is a deliberate independence tool.
Fable, Astra, and Spark below require explicit opt-in; none is an automatic tier.

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
  - **`gpt-5.3-codex-spark` — near-instant research preview.** Live,
    user-supervised, no-reasoning micro-iterations only: one literal rename,
    prop, type error, CSS adjustment, or similarly exact patch with an explicit
    check. It is separate from Fast mode and is never an autonomous acceptor,
    final reviewer, security reviewer, architecture decision-maker, or
    executor of an irreversible action.
- **Haiku 5.5 (`anthropic/claude-haiku-5-5`) — bounded junior.** Classification, extraction, simple edits, short
  summaries, routing, mechanical checks. NOT for architecture, complex
  debugging, large ambiguous tasks, or expensive-mistake decisions; drifts from
  instructions in large contexts.

- **GLM-5.3-Flash (`zai/glm-5.3-flash`) — bounded medium-tier worker.**
  Use low/medium for clear artifacts with an exact acceptance gate, durable
  report and deadline; high only after demonstrated complexity. Use only a
  configured runner; sending private code to Z.ai is a data-egress decision.
- **Astra (`gpt-6-astra`) — explicit opt-in execution escalation.** Terminal,
  recovery and stateful unknown environments; never mechanical routine work.

**Exact routing.** Catalog presence is not successful inference. Tool role
labels do not guarantee per-dispatch model selection: check supported pinning
or overrides and report the actual route. For an authorized OMP smoke, pin
`--model <exact-provider/model>` and a temporary configuration overlay with
`retry: { modelFallback: false }`; do not resume a session or use fuzzy ids.
Judgment separately requires `modelRoles.judge: openai-codex/gpt-6-luna` and
`retry.fallbackChains.judge: []`; do not append a chat thinking suffix to judge.
Existing free OpenRouter choices remain unchanged.

**Smoke before routing.** Before the first real dispatch on a pinned model,
and before advising any production model switch, run one trivial call on the
exact route (same CLI, auth kind, and model id) and quote its result; an
account can reject a model the table lists. Match the planned capabilities:
a tool-using route must execute a harmless real tool call and deliver a readable
artifact through the named report writer. A text-only response proves neither.
Record observed latency and remaining runtime budget; a passing smoke proves
capability, not that a larger task will meet its deadline.
