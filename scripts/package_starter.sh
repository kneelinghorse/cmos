#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"
TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
ARCHIVE_NAME="cmos-starter-${TIMESTAMP}.tar.gz"
ARCHIVE_PATH="${DIST_DIR}/${ARCHIVE_NAME}"

mkdir -p "${DIST_DIR}"

EXCLUDES=(
  "--exclude=cmos"
  "--exclude=dist"
  "--exclude=.git"
  "--exclude=.gitignore"
  "--exclude=SESSIONS.jsonl"
  "--exclude=*.log"
  "--exclude=telemetry/events/*.tmp"
  "--exclude=telemetry/archive"
)

cd "${ROOT_DIR}"
tar -czf "${ARCHIVE_PATH}" "${EXCLUDES[@]}" \
  agents.md \
  context \
  db \
  docs \
  PROJECT_CONTEXT.json \
  scripts \
  templates \
  telemetry \
  tests \
  runtime \
  workers \
  missions

echo "Starter package created at ${ARCHIVE_PATH}"
