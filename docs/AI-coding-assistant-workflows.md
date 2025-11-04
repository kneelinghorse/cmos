# AI Coding Assistant Operations Guide

This guide documents how CMOS maintains predictable, auditable behaviour from AI coding assistants. All practices assume the SQLite-backed runtime is authoritative and that every session follows the backlog-driven mission lifecycle.

## Purpose
- Align agent prompts, mission orchestration logic, and validation commands with CMOS guardrails.
- Provide operators with deterministic steps for managing context, delegation patterns, and failure recovery.
- Ensure all automation honours security, quality, and telemetry requirements before missions are marked complete.

## Functional Domains

### Context Stewardship
- **agents.md compliance**: Load the root `agents.md` before any mission, then honour directory-specific overrides when editing submodules. Treat it as non-optional configuration.
- **Working memory sync**: Mirror mission selection, session count, and last-session markers between `PROJECT_CONTEXT.json`, the `contexts` table, and `SESSIONS.jsonl`.
- **Sensitive data handling**: Follow OWASP rules; never echo secrets in prompts or logs. Use provided repositories/env vars instead of embedding credentials.

### Mission Orchestration
- **Status precedence**: Query missions in the order `In Progress -> Current -> Queued`. Promote only one mission at a time and append start/complete events to `SESSIONS.jsonl`.
- **Pattern selection**: Choose a single orchestration mode (`none`, `rsip`, `delegation`, `boomerang`) per mission and document the decision in mission notes.
- **Failure escalation**: Apply the tiered policy - automatic retry, pattern-specific retry limits, fallback to linear execution, then human review flagging.

### Quality & Security Gates
- **Validation scripts**: Run `python scripts/validate_parity.py` after any mission that touches SQLite, backlog lifecycle, or telemetry. For documentation updates, run `python scripts/validate_foundational_refs.py`.
- **Testing cadence**: Use `node cmos/context/integration_test_runner.js` for guardrail coverage and targeted `npm run test:*` commands based on the subsystem touched.
- **Security posture**: Ensure prepared statements for DB access, apply rate limiting guidance in runtime assets, and update the security checklist if controls change.

### Telemetry & Feedback
- **Session events**: Maintain append-only logs in both SQLite (`session_events`) and `cmos/SESSIONS.jsonl`, including summaries, next hints, and blockers.
- **Database health**: Monitor `telemetry/events/database-health.jsonl` for anomalies after each mission and document follow-up actions in mission notes.
- **Knowledge capture**: Record new operational patterns or deviations within `cmos/MASTER_CONTEXT.json` and update this guide when behaviour changes persist.

## Operating Procedure
1. **Pre-flight**: Load `agents.md`, review the backlog entry for the candidate mission, and confirm database parity via `python scripts/validate_parity.py --check`.
2. **Selection**: Promote the highest-priority mission, append the start event, and set mission status to `In Progress` in both SQLite and YAML.
3. **Execution**: Follow the relevant functional playbooks (runtime, documentation, testing). Keep operations scoped to the active mission.
4. **Validation**: Run required tests, parity checks, and link validators. Document outcomes and remediation steps if guardrails fail.
5. **Closure**: Update mission status to `Completed`, note outcomes, append completion events, and refresh `PROJECT_CONTEXT.json`.

## Validation Checklist
- [ ] `SESSIONS.jsonl` entry created for start and completion.
- [ ] Mission status transitions recorded in `missions/backlog.yaml` and SQLite.
- [ ] Required scripts/tests executed with documented results.
- [ ] Parity validation confirms file <-> database sync.
- [ ] Telemetry updated or explicitly noted as unchanged.
- [ ] Mission notes capture orchestration mode and follow-up actions.

## Reference Links
- Folder guardrails: `README.md`
- Roadmap template: `../foundational-docs/roadmap_template.md`
- Technical architecture template: `../foundational-docs/tech_arch_template.md`
- Parity validator: `scripts/validate_parity.py`
