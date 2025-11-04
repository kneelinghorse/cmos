"""Mission runtime utilities backed by the canonical SQLite store."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .db_client import SQLiteClient


def utc_now() -> str:
    return datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_metadata(metadata: Optional[str]) -> Dict[str, Any]:
    if not metadata:
        return {}
    try:
        parsed = json.loads(metadata)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def _format_metadata(metadata: Dict[str, Any]) -> Optional[str]:
    return json.dumps(metadata, ensure_ascii=False) if metadata else None


def _format_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    return json.dumps(value, ensure_ascii=False)


def _load_inline_mapping(line: str) -> Dict[str, Any]:
    start = line.index("{")
    end = line.rindex("}") + 1
    return yaml.safe_load(line[start:end])


def _update_inline_line(line: str, updates: Dict[str, Any]) -> str:
    indent = line[: len(line) - len(line.lstrip())]
    mapping = _load_inline_mapping(line)
    order: List[str] = list(mapping.keys())

    for key, value in updates.items():
        if value is None:
            if key in mapping:
                mapping.pop(key)
                if key in order:
                    order.remove(key)
            continue
        mapping[key] = value
        if key not in order:
            order.append(key)

    formatted = ", ".join(f"{key}: {_format_value(mapping[key])}" for key in order if key in mapping)
    return f"{indent}- {{ {formatted} }}"


@dataclass
class MissionEventResult:
    raw_event: str
    event: Dict[str, Any]
    next_mission: Optional[str] = None


class MissionRuntimeError(RuntimeError):
    """Raised when mission runtime operations fail."""


class MissionRuntime:
    """Coordinates mission selection, status transitions, and logging via SQLite."""

    def __init__(
        self,
        *,
        repo_root: Path | str | None = None,
        db_path: Path | str | None = None
    ) -> None:
        self.repo_root = Path(repo_root) if repo_root else Path(__file__).resolve().parents[1]
        self.db_path = Path(db_path) if db_path else self.repo_root / "db" / "cmos.sqlite"
        self.schema_path = self.repo_root / "db" / "schema.sql"
        self.backlog_path = self.repo_root / "missions" / "backlog.yaml"
        self.sessions_path = self.repo_root / "SESSIONS.jsonl"
        self.telemetry_dir = self.repo_root / "telemetry" / "events"
        self.client = SQLiteClient(self.db_path, schema_path=self.schema_path)

    def close(self) -> None:
        self.client.close()

    def ensure_database(self) -> None:
        status = self.client.health_check()
        self._write_health_event(status)
        if not status.ok:
            raise MissionRuntimeError(f"Database health check failed: {status.message}")

    def fetch_next_candidate(self) -> Optional[Dict[str, Any]]:
        rows = self.client.fetchall(
            """
            SELECT id, name, status, completed_at, notes, metadata
              FROM missions
             WHERE status IN ('Queued', 'Current', 'In Progress')
             ORDER BY CASE status
                      WHEN 'In Progress' THEN 0
                      WHEN 'Current' THEN 1
                      WHEN 'Queued' THEN 2
                      ELSE 3
                    END,
                    rowid
             LIMIT 1
            """
        )
        return rows[0] if rows else None

    def start_mission(
        self,
        mission_id: str,
        *,
        agent: str,
        summary: str,
        ts: Optional[str] = None,
        append_to_file: bool = True
    ) -> MissionEventResult:
        ts = ts or utc_now()
        row = self.client.fetchone(
            "SELECT status, metadata FROM missions WHERE id = :id",
            {"id": mission_id}
        )
        if not row:
            raise MissionRuntimeError(f"Mission {mission_id} not found in database")

        metadata = _parse_metadata(row.get("metadata"))
        metadata["started_at"] = ts

        with self.client.transaction() as conn:
            conn.execute(
                """
                UPDATE missions
                   SET status = 'In Progress',
                       metadata = :metadata
                 WHERE id = :id
                """,
                {"id": mission_id, "metadata": _format_metadata(metadata)}
            )

            event = {
                "ts": ts,
                "agent": agent,
                "mission": mission_id,
                "action": "start",
                "status": "in_progress",
                "summary": summary
            }
            raw_event = self._insert_session_event(conn, event)

        if append_to_file:
            self._append_session_event(raw_event)

        self._update_backlog_entry(mission_id, {"status": "In Progress", "started_at": ts})
        return MissionEventResult(raw_event=raw_event, event=event)

    def complete_mission(
        self,
        mission_id: str,
        *,
        agent: str,
        summary: str,
        notes: str,
        ts: Optional[str] = None,
        next_hint: Optional[str] = None,
        promote_next: bool = True,
        immediate: bool = False,
        append_to_file: bool = True
    ) -> MissionEventResult:
        ts = ts or utc_now()
        row = self.client.fetchone(
            "SELECT metadata FROM missions WHERE id = :id",
            {"id": mission_id}
        )
        if not row:
            raise MissionRuntimeError(f"Mission {mission_id} not found in database")
        metadata = _parse_metadata(row.get("metadata"))
        metadata["completed_at"] = ts

        next_mission_id: Optional[str] = None

        with self.client.transaction() as conn:
            conn.execute(
                """
                UPDATE missions
                   SET status = 'Completed',
                       completed_at = :completed_at,
                       notes = :notes,
                       metadata = :metadata
                 WHERE id = :id
                """,
                {
                    "id": mission_id,
                    "completed_at": ts,
                    "notes": notes,
                    "metadata": _format_metadata(metadata)
                }
            )

            if promote_next:
                next_mission_id = self._promote_next_queued(conn, immediate=immediate, started_at=ts if immediate else None)
                if next_mission_id and not next_hint:
                    next_status = "In Progress" if immediate else "Current"
                    next_hint = f"{next_mission_id} is now {next_status}"

            event = {
                "ts": ts,
                "agent": agent,
                "mission": mission_id,
                "action": "complete",
                "status": "completed",
                "summary": summary,
                "next_hint": next_hint
            }
            raw_event = self._insert_session_event(conn, event)

        if append_to_file:
            self._append_session_event(raw_event)

        backlog_updates = {
            "status": "Completed",
            "completed_at": ts,
            "notes": notes
        }
        self._update_backlog_entry(mission_id, backlog_updates)
        if next_mission_id:
            next_updates = {"status": "In Progress" if immediate else "Current"}
            if not immediate:
                next_updates["started_at"] = None
            else:
                next_updates["started_at"] = ts
            self._update_backlog_entry(next_mission_id, next_updates)

        return MissionEventResult(raw_event=raw_event, event=event, next_mission=next_mission_id)

    def block_mission(
        self,
        mission_id: str,
        *,
        agent: str,
        summary: str,
        reason: str,
        needs: Optional[List[str]] = None,
        ts: Optional[str] = None,
        next_hint: Optional[str] = None,
        append_to_file: bool = True
    ) -> MissionEventResult:
        ts = ts or utc_now()
        row = self.client.fetchone(
            "SELECT metadata FROM missions WHERE id = :id",
            {"id": mission_id}
        )
        if not row:
            raise MissionRuntimeError(f"Mission {mission_id} not found in database")
        metadata = _parse_metadata(row.get("metadata"))
        metadata["blocked_at"] = ts
        metadata["blocked_reason"] = reason
        if needs:
            metadata["blocked_needs"] = needs
        else:
            metadata.pop("blocked_needs", None)

        with self.client.transaction() as conn:
            conn.execute(
                """
                UPDATE missions
                   SET status = 'Blocked',
                       completed_at = NULL,
                       notes = :notes,
                       metadata = :metadata
                 WHERE id = :id
                """,
                {
                    "id": mission_id,
                    "notes": reason,
                    "metadata": _format_metadata(metadata)
                }
            )
            event = {
                "ts": ts,
                "agent": agent,
                "mission": mission_id,
                "action": "blocked",
                "status": "blocked",
                "summary": summary,
                "next_hint": next_hint,
                "needs": needs or [],
                "reason": reason
            }
            raw_event = self._insert_session_event(conn, event)

        if append_to_file:
            self._append_session_event(raw_event)

        self._update_backlog_entry(mission_id, {"status": "Blocked", "notes": reason})
        return MissionEventResult(raw_event=raw_event, event=event)

    def _insert_session_event(self, connection: Any, event: Dict[str, Any]) -> str:
        raw_event = json.dumps(event, ensure_ascii=False)
        connection.execute(
            """
            INSERT INTO session_events (ts, agent, mission, action, status, summary, next_hint, raw_event)
            VALUES (:ts, :agent, :mission, :action, :status, :summary, :next_hint, :raw_event)
            """,
            {
                "ts": event.get("ts"),
                "agent": event.get("agent"),
                "mission": event.get("mission"),
                "action": event.get("action"),
                "status": event.get("status"),
                "summary": event.get("summary"),
                "next_hint": event.get("next_hint"),
                "raw_event": raw_event
            }
        )
        return raw_event

    def _append_session_event(self, raw_event: str) -> None:
        self.sessions_path.parent.mkdir(parents=True, exist_ok=True)
        with self.sessions_path.open("a", encoding="utf-8") as handle:
            handle.write(raw_event)
            handle.write("\n")

    def _promote_next_queued(
        self,
        connection: Any,
        *,
        immediate: bool,
        started_at: Optional[str]
    ) -> Optional[str]:
        row = connection.execute(
            """
            SELECT id, metadata
              FROM missions
             WHERE status = 'Queued'
             ORDER BY rowid
             LIMIT 1
            """
        ).fetchone()
        if not row:
            return None

        metadata = _parse_metadata(row["metadata"])
        if immediate and started_at:
            metadata["started_at"] = started_at
        else:
            metadata.pop("started_at", None)

        new_status = "In Progress" if immediate else "Current"
        connection.execute(
            """
            UPDATE missions
               SET status = :status,
                   metadata = :metadata
             WHERE id = :id
            """,
            {
                "id": row["id"],
                "status": new_status,
                "metadata": _format_metadata(metadata)
            }
        )
        return row["id"]

    def _update_backlog_entry(self, mission_id: str, updates: Dict[str, Any]) -> None:
        if not self.backlog_path.exists():
            return

        lines = self.backlog_path.read_text(encoding="utf-8").splitlines()
        updated = False
        for index, line in enumerate(lines):
            if line.strip().startswith("- {") and f'id: "{mission_id}"' in line:
                formatted_updates = {}
                for key, value in updates.items():
                    if key in {"status", "notes", "completed_at", "started_at"}:
                        formatted_updates[key] = value
                lines[index] = _update_inline_line(line, formatted_updates)
                updated = True
                break

        if not updated:
            return

        self.backlog_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _write_health_event(self, status: Any) -> None:
        payload = {
            "ts": utc_now(),
            "source": "mission_runtime",
            "status": "ok" if status.ok else "error",
            "message": status.message,
            "details": status.details
        }
        self.telemetry_dir.mkdir(parents=True, exist_ok=True)
        health_path = self.telemetry_dir / "database-health.jsonl"
        with health_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False))
            handle.write("\n")


__all__ = ["MissionRuntime", "MissionRuntimeError", "MissionEventResult", "utc_now"]
