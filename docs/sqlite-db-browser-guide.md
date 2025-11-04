# DB Browser Quickstart for CMOS

The canonical SQLite runtime lives at `db/cmos.sqlite`. Use the following workflow to inspect or validate data with DB Browser for SQLite (or any equivalent tool) without breaking file <-> database parity.

## Opening the Database
1. Launch DB Browser for SQLite.
2. Click **Open Database** and select `db/cmos.sqlite` from the project root.
3. Confirm that the `Table` view lists `sprints`, `missions`, `mission_dependencies`, `contexts`, `session_events`, `telemetry_events`, and `prompt_mappings`.

## Browsing Data
- **Missions**: Open the `missions` table to view status, completion timestamps, and notes per mission. Use the filter box to jump to active work (status `In Progress` or `Current`).
- **Backlog Ordering**: Switch to the `active_missions` view to confirm promotion order mirrors `missions/backlog.yaml`.
- **Contexts**: The `contexts` table stores JSON payloads for `PROJECT_CONTEXT.json` and `MASTER_CONTEXT.json`. Use the **Browse Data** tab with the built-in JSON viewer to inspect formatted content.
- **Sessions**: `session_events` records start/complete/blocked actions with the original JSON payload preserved in `raw_event`.

## Running Queries
Open the **Execute SQL** tab and run queries such as:
```sql
SELECT sprint_id, status, COUNT(*)
  FROM missions
 GROUP BY sprint_id, status
 ORDER BY sprint_id, status;
```
Use the **Save** feature to export results as CSV for lightweight reporting.

## Keeping Files and DB in Sync
- After modifying data through the UI, export the executed statements and replay them via the CLI to ensure deterministic history.
- Run `python3 scripts/seed_sqlite.py` whenever the file-based sources change and you need to regenerate a clean database.
- Avoid editing JSON blobs directly in the UI; prefer exporting, editing with a JSON-aware editor, and re-importing to prevent formatting drift.
- After UI edits, run `python scripts/validate_parity.py` to confirm mirrors remain synchronized.

## Troubleshooting
- If tables appear empty, re-run the seeding script to regenerate the database.
- For schema changes, update `db/schema.sql` first, then re-run the seeder to apply migrations.
- Use the `File -> Compact Database` option after large data loads to reclaim disk space.
