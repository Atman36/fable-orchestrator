# Model roles — strengths, limits, refusal behavior (as of 2026-07)

Read this before routing anything off the default table in SKILL.md § Model
routing: an unusual role, an escalation, a first-touch decision in a sensitive
domain, or a model you have not used this session. The table stays the default;
this file is why the table looks the way it does.

Default pipeline shape: **the head invents → Opus verifies and plans → Sonnet
builds → GPT-5.6 independently critiques → Haiku clears the routine.**

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
- **GPT-5.6 (via Codex CLI; default `gpt-5.6-sol`, 2026-07) — analyst.**
  Research, option comparison, rigorous analysis, requirements work, synthesis
  over large corpora, independent out-of-family critique of Claude-made plans
  and diffs; strong at heavy bounded execution. Metered quota — the Codex rules
  in `references/codex.md` apply to every call.
- **Haiku 4.5 — fast junior.** Classification, extraction, simple edits, short
  summaries, routing, mechanical checks. NOT for architecture, complex
  debugging, large ambiguous tasks, or expensive-mistake decisions; drifts from
  instructions in large contexts.
