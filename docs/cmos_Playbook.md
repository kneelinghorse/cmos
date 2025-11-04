# CMOS Operations Playbook

This playbook consolidates the procedures maintainers follow when operating CMOS. Each section is organized by workflow rather than timeline so teams can jump directly to the capability they need.

## Context Intake Workflow
1. **Load core context**: Confirm `agents.md`, `cmos/PROJECT_CONTEXT.json`, and `cmos/context/MASTER_CONTEXT.json` are accessible. Update the `agents_md_loaded` flag once parsed.
2. **Validate session state**: Run `python scripts/validate_parity.py --check` to confirm SQLite <-> file parity before promoting a mission.
3. **Assess mission readiness**: Inspect `cmos/missions/backlog.yaml` and ensure prerequisites are completed or explicitly waived in `MASTER_CONTEXT.json`.
4. **Document assumptions**: If new constraints surface, append them to `MASTER_CONTEXT.json` under `constraints` for traceability.

## Mission Lifecycle Workflow
1. **Select mission**: Apply status precedence (`In Progress`, `Current`, `Queued`). Promote the chosen mission and log a start event in both SQLite and `SESSIONS.jsonl`.
2. **Scope control**: Keep edits bound to the mission objective. If work exceeds mission scope, split the backlog entry rather than expanding deliverables.
3. **Execution logging**: Capture intermediate decisions in mission notes or `MASTER_CONTEXT.json` so future sessions inherit context.
4. **Completion**: Run verification commands, update mission status to `Completed`, stamp `completed_at`, and promote the next eligible mission.

## Runtime Operations Workflow
- **SQLite canonical usage**: Treat `db/cmos.sqlite` as the primary datastore. Use the shared clients under `cmos/context/` for read/write operations and mirror results back to files.
- **Seeding and regeneration**: When schema or baseline data changes, run `python scripts/seed_sqlite.py` and rerun parity validation before resuming missions.
- **Telemetry hygiene**: Write runtime events to `telemetry/events/<mission-id>.jsonl` and review `telemetry/events/database-health.jsonl` for anomalies after each mission.
- **Failure handling**: Roll back partial writes if parity fails; log blockers with `status: Blocked` plus required follow-up in the backlog.

## Quality & Telemetry Workflow
- **Automated checks**: Execute `node cmos/context/integration_test_runner.js` after changes to templates, guardrails, or mission orchestration assets. Record results in mission notes.
- **Security validation**: Leverage fixtures under `tests/security/` to confirm OWASP coverage whenever security guidance changes.
- **Performance monitoring**: Update `tests/performance/benchmarks.json` when runtime characteristics shift (e.g., new telemetry collectors, heavier orchestration).
- **Telemetry updates**: Ensure completion events include summaries and `next_hint` guidance. Mirror the same data in the `session_events` table.

## Documentation Governance Workflow
- **Internal vs external**: Store maintainer-only procedures here. Any material intended for downstream starters belongs under `docs/` or `foundational-docs/`.
- **Cross-references**: Replace duplicated roadmap or architecture content with links to `../foundational-docs/roadmap_template.md` and `../foundational-docs/tech_arch_template.md`.
- **Review cadence**: Re-evaluate each document when orchestration patterns, database schema, or telemetry targets change. Use the checklist in `README.md`.

## Escalation & Fallback
- **Tiered recovery**: Follow automatic retry -> pattern-specific limits -> linear fallback -> human review escalation.
- **Blocked missions**: Set backlog status to `Blocked`, append a `needs` array in `SESSIONS.jsonl`, and document unblock criteria in mission notes.
- **Knowledge capture**: For recurring incidents, add a `decisions_made` entry to `MASTER_CONTEXT.json` and update relevant workflow sections above.

## Quick Commands
| Purpose | Command |
| --- | --- |
| Validate parity | `python scripts/validate_parity.py` |
| Seed SQLite | `python scripts/seed_sqlite.py` |
| Integration suite | `node cmos/context/integration_test_runner.js` |
| Guardrail refs | `python scripts/validate_foundational_refs.py` |
| Inspect backlog | `cat cmos/missions/backlog.yaml` |
