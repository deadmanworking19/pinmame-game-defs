# Codex instructions

## Required runbook

Before planning, delegation, curation, or repository changes, open and read `docs/INSTRUCTIONS.md` completely. If a read is truncated, continue until EOF. Treat that file as the authoritative operational runbook for this repository and follow all prerequisite, evidence, workflow, validation, model-allocation, and review requirements in it.

Codex does not provide a documented inline include directive for `AGENTS.md`; this explicit read is mandatory and must not be replaced by a summary or assumed prior knowledge.

## Model roles

- Use the latest GPT Sol at `xhigh` for primary high-tier curation, escalation, and promotion decisions.
- Delegate bounded mid-tier work to the latest GPT Terra at `xhigh`.
- Delegate bounded low-tier and mechanical work to the latest GPT Luna at `xhigh`.
- Use the latest Opus (`opus`) at `high` effort through the Claude Code CLI for the mandatory independent read-only review. Start a fresh reviewer session against the exact proposed tree and follow the cross-provider review requirements in `docs/INSTRUCTIONS.md`.
- Resolve the latest available model in each named family from current provider model metadata before invoking it; do not pin a version or substitute a different tier. Follow the runbook's selection and smoke-check requirements.
- Do not use the reviewing model to author or repair the contribution it is reviewing. Independently verify its findings, make fixes with the appropriate curation model, rerun the gates, and obtain a fresh review after material changes.
