# SQLite Prompt Execution Guide

The CMOS starter now treats `db/cmos.sqlite` as the single source of truth for missions, context, sessions, and telemetry. This guide explains how agents should satisfy master context and mission lifecycle prompts without emitting SQL. All actions route through the provided Python helpers and automation scripts so that the database stays synchronised with the optional file mirrors.

---

## Core Principles

- **Database first** – Read and write mission state through `db/cmos.sqlite`. Files such as `context/MASTER_CONTEXT.json`, `PROJECT_CONTEXT.json`, `missions/backlog.yaml`, and `SESSIONS.jsonl` are mirrors for human review or packaging.
- **Plain language** – Never send raw SQL to the agent. Reference tables and columns by name, and use the helper commands in this guide to perform updates.
- **Guardrails** – Respect OWASP guardrails, keep telemetry append-only, and document blockers or fallbacks immediately.

---

## Canonical Data Map

| Table / View      | Purpose                                                                 | Key Columns                                        |
| ----------------- | ----------------------------------------------------------------------- | ------------------------------------------------- |
| `contexts`        | JSON payloads for master/project context, stored by `id`                | `id`, `content`, `updated_at`, `source_path`      |
| `missions`        | Mission backlog with status, notes, and metadata                        | `id`, `status`, `completed_at`, `notes`, `metadata`, `sprint_id` |
| `session_events`  | Append-only session log mirroring `SESSIONS.jsonl`                      | `ts`, `agent`, `mission`, `action`, `status`, `summary`, `next_hint`, `raw_event` |
| `sprints`         | Sprint registry (title, focus, status, mission counts)                  | `id`, `title`, `status`, `total_missions`, `completed_missions` |
| `mission_dependencies` | Directed edges between missions                                   | `from_id`, `to_id`, `type`                        |
| `telemetry_events`| Structured telemetry payloads, including database health events         | `mission`, `source_path`, `ts`, `payload`         |
| `metadata`        | Global flags (e.g., `seeded_at`)                                        | `key`, `value`                                    |
| `active_missions` (view) | Convenience projection for missions in flight                   | inherits columns from `missions` and `sprints`    |

---

## Quick Reference – Old Files → New DB Prompts

| Legacy instruction                                                      | New prompt (database-first)                                                                                                                                                                                                                                                                                                     |
|-------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| “Read master context at `context/MASTER_CONTEXT.json`.”                 | “Open `db/cmos.sqlite` and load the `contexts` row where `id = 'master_context'`. Treat that JSON as canonical; update the mirror after changes.”                                                                                                                                                                                |
| “Update master context in `context/MASTER_CONTEXT.json`.”               | “Persist updates by calling the context helper to overwrite `contexts.content` for `id = 'master_context'`, then refresh the JSON mirror once the transaction commits.”                                                                                                                                                         |
| “Manipulate missions/backlog.yaml and SESSIONS.jsonl during execution.” | “Use the mission runtime helper to promote missions, log session events inside `session_events`, and keep the `missions` table in sync. Regenerate file mirrors only when you need a human-readable export.”                                                                                                                    |
| “Maintain backlog in `missions/backlog.yaml`.”                          | “Inspect and edit the backlog directly through `missions`, `mission_dependencies`, and `sprints`. Use the helper CLI for mission promotion to maintain ordering.”                                                                                                                                                               |
| “Create new sprint folder under `cmos/missions/sprint-xx`.”             | “Insert a new sprint record into `sprints` and seed its missions inside `missions`. Optional narrative notes can live in a docs folder, but the sprint definition itself belongs in the database.”                                                                                                                              |

---

## Tooling Overview

- `python scripts/mission_runtime.py status` – Lists candidate missions in priority order (In Progress → Current → Queued → Blocked).
- `python scripts/mission_runtime.py start --mission <id> ...` – Marks a mission In Progress and logs the session start.
- `python scripts/mission_runtime.py complete --mission <id> ...` – Marks a mission Completed, records notes, promotes the next mission, and appends the completion event.
- `context.db_client.SQLiteClient` – Low-level helper for context operations (`get_context`, `set_context`); used in the examples below.
- `python scripts/validate_parity.py` – Confirms database and mirrors match after changes.
- `python scripts/seed_sqlite.py` – Rebuilds an empty database from the schema (useful for tests or resetting mirrors).
- `telemetry/events/database-health.jsonl` – Append-only log generated by mission runtime health checks.

---

## Master Context & Project Context Workflows

1. **Reading**  
   - Instantiate `SQLiteClient` (see Appendix A) and call `get_context("master_context")` or `get_context("project_context")`. This returns the JSON payload as a Python dictionary without exposing SQL.
   - If the row is missing, create an initial payload and persist it with `set_context`.

2. **Updating**  
   - Merge your changes into the dictionary returned by `get_context`.  
   - Call `set_context("master_context", updated_payload, source_path="context/MASTER_CONTEXT.json")`. The helper records the timestamp and keeps `source_path` aligned with the mirror.  
   - After committing, write the same JSON to the file mirror so humans can inspect it.

3. **Guardrails**  
   - Keep context payloads compact. Store session counters, last mission, and critical facts—avoid redundant mission history that already lives in `missions`.  
   - Capture major architectural decisions in `MASTER_CONTEXT` and update `metadata` or `telemetry_events` when they affect runtime guardrails.

---

## Mission Lifecycle (Start → Execute → Complete)

1. **Select the target mission**  
   - Run `python scripts/mission_runtime.py status` to list candidates.  
   - The helper prioritises statuses in this order: `In Progress`, `Current`, then `Queued`. If the top candidate is `Queued`, the helper automatically promotes it to `In Progress` when you call `start`.

2. **Start the mission**  
   ```bash
   python scripts/mission_runtime.py start \
     --mission S4.1 \
     --agent codex \
     --summary "Kick-off database adoption work"
   ```
   - This updates `missions.status`, stamps `metadata.started_at`, bumps `project_context.working_memory.session_count`, refreshes `active_mission`, and captures a transactional snapshot of both contexts (including `context_health.last_update`).

3. **Execute deliverables**  
   - Follow mission instructions, run guardrail suites under `context/` or `npm run test:*`, and capture artefacts as needed.

4. **Complete or block**  
   - Completion:
     ```bash
     python scripts/mission_runtime.py complete \
       --mission S4.1 \
       --agent codex \
       --summary "Database helpers promoted" \
       --notes "Runtime helpers relocated; parity script updated."
     ```
     - Sets `missions.status = 'Completed'`, populates `completed_at`, writes notes, promotes the next mission, and logs the completion event.
     - Updates `project_context`/`master_context` session counters, clears any blocker reminders for the mission, and records the completion in `working_memory.session_history`.
  - Blocked:
    ```bash
    python scripts/mission_runtime.py block \
      --mission S4.1 \
      --agent codex \
      --summary "Blocked on schema decision" \
      --reason "Waiting on schema approval" \
      --need "Approve revised schema" \
      --next-hint "Ping architecture team for review"
    ```
     - Provide one or more `--need` flags to capture unblock requirements. The helper sets `missions.status = 'Blocked'`, records the reason/needs in metadata, pushes a structured blocker entry into `master_context.next_session_context`, and appends a blocked session event without promoting another mission.

5. **Telemetry & health**  
   - Mission runtime emits a health event into `telemetry/events/database-health.jsonl` each time it touches the database. Review the log if parity or schema issues appear.

---

## Backlog & Sprint Maintenance

- **Adding missions** – Insert mission rows through your preferred scripting workflow (e.g., Python using `SQLiteClient.executemany`). Keep mission IDs unique and align them with the sprint identifier (e.g., `S5.1` belongs to `sprint_id = 'Sprint 05'`).  
- **Dependencies** – Record relationships by inserting rows into `mission_dependencies`. Provide `type` values such as `Blocks`, `Requires`, or `InformedBy` to match your planning conventions.  
- **Sprint updates** – Update the `sprints` table when missions move between statuses so metrics (total vs. completed) remain accurate.  
- **Mirrors** – Regenerate `missions/backlog.yaml` only when you need to export the plan. The canonical data remains in SQLite.

---

## Telemetry & Logging

- **Session logs** – The mission runtime helper writes to `session_events` and the file mirror simultaneously. Treat `session_events` as canonical; only append new entries.  
- **Custom telemetry** – Use `telemetry_events` to record pattern-specific metrics (e.g., RSIP iterations, delegation worker failures). Each payload should include `mission`, `status`, optional `fallbackTriggered`, and a nested `details` object.  
- **Database health** – Monitor `telemetry/events/database-health.jsonl` and corresponding `telemetry_events` rows. Investigate repeated failures before continuing.

---

## Guardrails & Best Practices

- **Do**
  - Keep the database and file mirrors in lockstep by running `python scripts/validate_parity.py` after major updates.  
  - Record blockers immediately and include clear `needs` lists in the session payload.  
  - Store notes and metadata in JSON form inside `missions.metadata` for easy retrieval.

- **Do Not**
  - Expose raw SQL in user-facing prompts or documentation.  
  - Manually edit `db/cmos.sqlite` with GUI tools without recording the change in the mission log.  
  - Forget to update `project_context` when missions complete; agents depend on the session counters and last mission pointers.

---

## Appendix A – Example Helper Snippets

### Reading master context

```bash
python - <<'PY'
from context.db_client import SQLiteClient

client = SQLiteClient("db/cmos.sqlite", create_missing=False)
payload = client.get_context("master_context")
print(payload or "master context is empty")
client.close()
PY
```

### Updating master context

```bash
python - <<'PY'
from context.db_client import SQLiteClient

client = SQLiteClient("db/cmos.sqlite", create_missing=False)
payload = client.get_context("master_context") or {}
payload.setdefault("working_memory", {})["last_reviewed"] = "2025-11-05"
client.set_context("master_context", payload, source_path="context/MASTER_CONTEXT.json")
client.close()
PY
```

These helpers rely on the `get_context` and `set_context` methods, so the snippets remain SQL-free. Mirror updates occur after the database transaction completes.

---

## Appendix B – Schema Checklist

- **contexts** – Must contain at least `master_context` and `project_context`. Keep JSON valid and compact.  
- **missions** – Status values limited to `Queued`, `Current`, `In Progress`, `Completed`, `Blocked`. Use ISO 8601 timestamps for `completed_at`.  
- **session_events** – Store complete JSON payloads (the mission runtime keeps the original in `raw_event`).  
- **telemetry_events** – Payloads should include `mission` and `status`. Guard against storing secrets or personal data.  
- **metadata** – Ensure `seeded_at` reflects the latest run of `scripts/seed_sqlite.py`.  
- **sprints** – Update `completed_missions` each time a mission crosses to `Completed` to maintain accurate progress metrics.

Follow this guide whenever prompts reference the SQLite runtime. By keeping operations inside the provided helpers, agents stay compliant with guardrails, and the starter remains safe to replicate across projects.***
