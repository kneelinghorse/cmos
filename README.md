# CMOS Starter

CMOS (Context + Mission Orchestration System) is a lightweight starter kit for teams that want to run Mission Protocol projects with high confidence. It provides a ready-to-ship repository structure, batteries-included automation, and security guardrails so human developers and AI agents can collaborate through mission-driven workflows.

---

## What You Get

- **Mission Protocol alignment** – Build/Research mission templates, domain packs, and worker manifests wired for RSIP, delegation, and boomerang orchestration patterns.
- **Agent-ready guidance** – A comprehensive `agents.md` contract plus empty context files that teams can populate with their own history.
- **Guardrails & validation** – Security, quality, and integration harnesses (JavaScript + Python) that enforce OWASP guidance and regression testing.
- **Optional SQLite canonical store** – Schema, seed script, and parity validator for teams that want transactional mission state in addition to file mirrors.
- **Packaging workflow** – Automation to produce distributable starter archives without leaking local tooling artefacts.

---

## Prerequisites

- **Node.js** 20.x (tooling, tests, optional automation)
- **Python** 3.11+ (SQLite utilities and validation scripts)
- **npm** (for running the provided scripts and test suites)

Optional:
- SQLite client (CLI or GUI) if you plan to inspect `db/cmos.sqlite`
- Git (recommended for version control)

---

## Quick Start

```bash
# Install Node.js dependencies
npm install

# Run linting or formatting as needed
npm run lint
npm run format

# Execute the default test suite
npm test
```

Once dependencies are installed:

1. Open `agents.md` to understand coding standards, communication rules, and security guardrails.
2. Populate `PROJECT_CONTEXT.json` and `context/MASTER_CONTEXT.json` with facts relevant to your project (both ship empty by design).
3. Create your backlog by copying `missions/backlog.yaml` into your planning workspace or populating it directly.
4. Build missions from `missions/templates/` or import Mission Protocol packs from `templates/`.

---

## Working With Mission Protocol

The starter is designed to plug directly into Mission Protocol v2 workflows.

- **Mission templates**: Use the YAML files under `missions/templates/` as starting points for Build, Research, and Planning missions. Each template includes orchestration configuration and structured prompting scaffolds.
- **Mission execution**: Run `python scripts/mission_runtime.py --help` to see commands for marking missions as started or completed. The CLI keeps `missions/backlog.yaml`, `SESSIONS.jsonl`, and the SQLite mirror in sync.
- **Worker delegation**: Additional workers live in `workers/`. Update `workers/manifest.yaml` to register new delegates and reference them within mission templates.
- **Advanced orchestration**: The starter ships with RSIP, delegation, and boomerang patterns wired into mission templates. Adjust `runtime/` assets to tweak checkpoints or iteration policies.

When integrating with a Mission Protocol server, point it at this repository’s root. The starter already conforms to the required directory structure and schema expectations.

---

## Optional SQLite Runtime

The file system remains the source of truth, but some teams prefer transactional mission storage.

- **Generate a database**  
  ```bash
  python scripts/seed_sqlite.py
  ```
  This applies `db/schema.sql`, writes an empty `db/cmos.sqlite`, and stores copies of `PROJECT_CONTEXT.json` and `context/MASTER_CONTEXT.json` in the `contexts` table.

- **Validate parity**  
  ```bash
  python scripts/validate_parity.py
  ```
  Confirms that mission statuses, context files, and session events in the database match the file mirrors.

- **Environment variables**  
  ```
  NODE_ENV=development
  DEBUG=true
  DB_PATH=db/cmos.sqlite
  ```
  Adjust `DB_PATH` if you embed the starter into another deployment layout.

---

## Repository Tour

- `agents.md` – Canonical instructions for AI collaborators (read this first).
- `context/` – Master context template and validation utilities (`integration_test_runner.js`, `security_validation.js`, `quality_assurance.js`, SQLite helpers).
- `missions/` – Mission templates plus an empty `backlog.yaml` scaffold.
- `templates/` – Mission Protocol domain packs ready for import.
- `workers/` – Worker definitions and manifest used by delegation patterns.
- `runtime/` – Assets for boomerang checkpoints and orchestration state.
- `scripts/` – Automation (`seed_sqlite.py`, `validate_parity.py`, `mission_runtime.py`, `package_starter.sh`, etc.).
- `telemetry/` – Event schemas and sample JSONL streams for monitoring.
- `tests/` – Guardrail fixtures for integration, security, quality, performance, and backward compatibility.
- `foundational-docs/` – Roadmap and technical architecture templates to clone into your own documentation.
- `db/` – SQLite schema and generated database artefacts.

---

## Automation & Tooling

| Script | Description |
| ------ | ----------- |
| `scripts/mission_runtime.py` | CLI for promoting missions, logging sessions, and syncing the SQLite store. |
| `scripts/seed_sqlite.py` | Rebuilds `db/cmos.sqlite` from the file mirrors (empty by default). |
| `scripts/validate_parity.py` | Verifies mission statuses and context files match between SQLite and YAML/JSON. |
| `scripts/validate_foundational_refs.py` | Ensures references target `foundational-docs/` instead of vendor-specific docs. |
| `scripts/package_starter.sh` | Produces a `cmos-starter-<UTC>.tar.gz` bundle in `dist/`. |

---

## Testing & Guardrails

- **JavaScript test suites** – Run `npm run test:unit`, `npm run test:integration`, or `npm run test:e2e` for focused coverage. Use `npm run test:coverage` to generate reports.
- **Security validation** – `context/security_validation.js` scans mission outputs and fixtures against OWASP-aligned rules.
- **Quality assurance** – `context/quality_assurance.js` reviews generated code for common pitfalls.
- **Integration harness** – `context/integration_test_runner.js` orchestrates the full guardrail suite.
- **Telemetry** – Append-only logs under `telemetry/events/` capture mission runtime results and database health checks (`telemetry/events/database-health.jsonl`).

Keep coverage above 80% and run guardrails whenever missions modify runtime assets, orchestration scripts, or security-sensitive templates.

---

## Packaging & Distribution

Create a distributable archive with:

```bash
./scripts/package_starter.sh
```

The script normalises from repo root, strips transient artefacts, and produces a tarball in `dist/`. Share the archive with downstream teams or automation pipelines to bootstrap new Mission Protocol projects quickly.

---

## Recommended Next Steps

1. **Clone the templates** – Copy `foundational-docs/roadmap_template.md` and `foundational-docs/tech_arch_template.md` into your documentation.
2. **Customise workers and missions** – Tailor `workers/manifest.yaml`, `missions/templates/`, and `backlog.yaml` to reflect your domain.
3. **Extend guardrails** – Add project-specific tests under `tests/` and wire them into the integration runner.
4. **Document context** – Keep `PROJECT_CONTEXT.json` and `context/MASTER_CONTEXT.json` updated as missions complete to give agents the context they need.

For questions or improvements, open an issue in your fork or update the starter locally and regenerate the archive. Happy mission building!
