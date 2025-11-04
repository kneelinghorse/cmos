# CMOS Starter Packaging Guide

Mission **B2.7 – Root Starter Packaging** reorganized the project so the distributable starter aligns with the repository root.

## Starter Layout

The starter bundle now includes:

- `agents.md`
- `context/`
- `db/`
- `docs/`
- `missions/`
- `PROJECT_CONTEXT.json`
- `runtime/`
- `scripts/`
- `templates/`
- `telemetry/`
- `tests/`
- `workers/`

Planning artefacts, research, and session telemetry now live in your external workspace (for example `/Users/systemsystems/portfolio/cmos-current-dev-pm/`). The starter package intentionally excludes that workspace.

## Creating an Archive

```bash
./scripts/package_starter.sh
```

The script emits a timestamped `cmos-starter-<UTC>.tar.gz` archive in `dist/`. It:

- Normalizes to repository root
- Excludes git metadata, transient telemetry archives, and any external planning workspace you keep alongside the starter
- Ensures the starter bundle always contains the curated layout above

## Next Steps

- Commit the generated `dist/` artifact to release branches as needed.
- Share the tarball with downstream teams or automation pipelines.
- Update this guide when additional directories or exclusion rules are required.
