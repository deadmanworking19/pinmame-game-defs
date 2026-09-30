# Claude Code instructions

@docs/INSTRUCTIONS.md
@docs/CURRENT-STATE.md

## Model roles

- Use the latest Opus (`opus`) at `high` effort for primary high-tier curation, escalation, and promotion decisions.
- Delegate bounded mid-tier work to the latest Sonnet (`sonnet`) at `high` effort.
- Delegate bounded low-tier and mechanical work to the latest Haiku (`haiku`) at `high` effort.
- Use the latest GPT Sol at `xhigh` through the Codex CLI for the mandatory independent read-only review. Start a fresh reviewer session against the exact proposed tree and follow the cross-provider review requirements in the imported runbook.
- Resolve the latest available model in each named family from current provider model metadata before invoking it; do not pin a version or substitute a different tier. Follow the runbook's selection and smoke-check requirements.
- Do not use the reviewing model to author or repair the contribution it is reviewing. Independently verify its findings, make fixes with the appropriate curation model, rerun the gates, and obtain a fresh review after material changes.
