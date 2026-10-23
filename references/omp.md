# Optional OMP supervision

Read when considering an OMP advisor, reviewer priorities, or event hooks.
Confirm the installed version supports the documented interface. Use features
within the task's authorized provider, model and budget; this reference alone
authorizes no configuration change, installation or external data transfer.

## Advisor during execution

Use an advisor selectively for long or risky work where early feedback can
prevent rework. It makes separately billed model requests and receives session
material, including main-agent reasoning and tool activity. Verify provider
permission, available model and effective state with `/advisor status` before
relying on it; bare `/advisor` toggles state. Keep investigative tools read-only.
The head verifies notes against evidence and retains decisions and approvals.
Because the advisor sees the implementation trajectory, treat it as ongoing
supervision; retain acceptance and final review from a fresh context. An absent,
lagging or failed advisor is not a clean verdict.

## Separate reviewer priorities

When reviewer setup is requested, inspect existing project guidance and use
`WATCHDOG.md` for a short list of concrete architectural boundaries, recurring
failure modes and required evidence. These instructions guide advisors without
being copied into the main agent's ordinary context. Preserve existing rules;
use `WATCHDOG.yml` only when a specialist roster is justified, and confirm the
effective roster with `/advisor status`. Read-only review needs no write tools.
Keep priorities scoped to the task and verify loaded guidance rather than
assuming the nearest file replaces inherited guidance.

## Event hooks for deterministic checks

Prefer existing project checks for repeated, judgment-free restrictions. If OMP
hook setup is requested, bind the installed extension API's actual event and
filter the tool explicitly: the `pre/` and `post/` directory names do not select
an event or tool. A pre-call guard can block a prohibited action; result handlers
can redact output; lifecycle handlers can run checks and retain their evidence.
Hook code runs with the user's privileges. Load trusted code only and inspect
the effective extension set through `/extensions`; do not run an installer just
to obtain these features. Verify each guard in a disposable fixture with an
allowed control and a denied control proving zero prohibited effects. A loaded
hook or completed turn is not a passing gate: record the real check result and
stop dependent work on failure. Hooks preserve the task's approval boundaries.

Sources (checked 2026-10-23):
- https://omp.sh/docs/advisor
- https://omp.sh/docs/hooks
