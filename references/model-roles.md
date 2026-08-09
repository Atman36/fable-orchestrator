# Model roles — strengths, limits, refusal behavior (as of 2026-08)

Read this before routing anything off the default table in SKILL.md § Model
routing: an unusual role, an escalation, a first-touch decision in a sensitive
domain, or a model you have not used this session. The table stays the default;
this file is why the table looks the way it does.

Codex-native default: **Sol leads → Terra builds → Luna clears bounded volume
→ a fresh Sol reviews critical output.** Claude-native default: **Fable leads
→ Opus carries risk → Sonnet builds → Haiku clears bounded routine work.**
Cross-family review is a deliberate independence tool, not the default worker
route.

- **Fable 5 — architect & inventor.** Hardest, newest, most ill-defined work:
  inventing products/systems, agent architectures, unexpected approaches,
  codebase-wide investigations, long-horizon autonomous runs, dense
  visual/product work. While subsidised access lasts, spend it on creating
  projects, specs and architectures — never routine code, never first-touch for
  simple tasks. Expensive, slow on hard runs; safety classifiers
  (offensive-security, biology/life-sciences, summarized-thinking-extraction)
  can reroute benign requests to Opus 4.8 as a `refusal`, not an error — route
  first-touch architecture/spec work in those domains straight to Opus.
- **Opus 4.8 — senior engineer / tech lead.** Complex multi-step tasks,
  architecture review, debugging, autonomous agent work, carrying a complex
  project to done; reliable on long tasks, honest about uncertainty. The
  premium reviewer, the risk-tier route, the fallback when Fable refuses. Needs
  clean scope — given noisy context it executes the noise literally.
- **Sonnet 5 — main builder.** The bulk of development: code, repo changes,
  tool use, executing a clear plan; the default executor. Its tokenizer
  inflates token counts (~30% vs Sonnet 4.6); low/medium effort can under-think
  hard problems — escalate architecture, compliance-sensitive and cross-service
  work instead of trusting the default.
- **Codex family (native hierarchy or via Codex CLI).** Metered quota — the
  invocation, cost, and safety rules in `references/codex.md` apply to every
  CLI call. Choose by the task's clarity, latency, volume, and cost of error:
  - **`gpt-5.6-sol` — lead orchestrator and senior reviewer.** Own task
    understanding, decomposition, architecture and product forks, conflict
    resolution, complex or ambiguous high-value work, security, research, and
    polished final review. Keep Sol out of routine implementation when Terra
    can execute a clear contract; use a fresh Sol context for acceptance.
  - **`gpt-5.6-terra` — default implementation workhorse.** Everyday
    production tasks, ordinary coding, read-heavy analysis, complex debugging,
    and supporting-document work. Escalate to Sol when the task changes
    architecture, security posture, scope, or remains ambiguous after recon.
  - **`gpt-5.6-luna` — fastest, lowest-cost GPT-5.6 tier.** Clear, repeatable,
    high-volume extraction, classification, routing, mechanical checks, and
    focused coding with a precise acceptance gate. Give Luna a narrow contract;
    do not make it resolve product or architecture forks.
  - **`gpt-5.3-codex-spark` — near-instant research preview.** Live,
    user-supervised, no-reasoning micro-iterations only: one literal rename,
    prop, type error, CSS adjustment, or similarly exact patch with an explicit
    check. It is separate from Fast mode and is never an autonomous acceptor,
    final reviewer, security reviewer, architecture decision-maker, or
    executor of an irreversible action.
  - **Compatibility only.** GPT-5.5 is used only when explicitly pinned or
    required for compatibility. GPT-5.4 and GPT-5.4 Mini retire from Codex with
    ChatGPT sign-in on 2026-08-31; assign them no new routing role, and prefer
    Terra or Luna for work they previously handled.
- **Haiku 4.5 — fast junior.** Classification, extraction, simple edits, short
  summaries, routing, mechanical checks. NOT for architecture, complex
  debugging, large ambiguous tasks, or expensive-mistake decisions; drifts from
  instructions in large contexts.
