# Integration & Testing Control Guide

This guide defines the continuous validation strategy for CMOS. Use it whenever templates, orchestration assets, or runtime scripts change.

## Objectives
- Confirm that required directories, templates, and guardrail fixtures exist and remain executable.
- Validate security, quality, and performance protections through targeted suites.
- Keep telemetry and reporting aligned with the SQLite-first workflow.

## Test Suite Matrix
| Suite | Focus | Assets | Execute |
| --- | --- | --- | --- |
| Integration | Presence and wiring of mission templates, context files, orchestration assets | `cmos/context/integration_test_runner.js`, `cmos/tests/integration/test_manifest.json` | `node cmos/context/integration_test_runner.js` |
| Security Guardrails | OWASP coverage, context protection, forbidden patterns | `cmos/tests/security/*.yaml` | `npm run test:integration -- security` (or targeted runner) |
| Quality Assurance | LLM output validation and style enforcement | `tests/quality/` fixtures | `npm run test:quality` |
| Performance Benchmarks | Regression checks for runtime throughput | `tests/performance/benchmarks.json` | `npm run test:performance` |
| Backward Compatibility | Legacy mission scenarios and workflows | `tests/backward_compatibility/` | `npm run test:integration -- backward` |

## Execution Workflow
1. **Plan**: Determine which suites apply based on modified files. Use git diff to scope.
2. **Run**: Execute relevant commands from the matrix. Pass `--output` to the integration runner when telemetry needs to be archived.
3. **Review**: Inspect failures, root cause them, and document remediation in mission notes.
4. **Record**: Append summaries to `telemetry/events/testing-summary.json` or the specified `.jsonl` stream.

## Reporting & Telemetry
- Use `node cmos/context/integration_test_runner.js --output telemetry/events/testing-summary.json` to update the canonical summary.
- When generating a `.jsonl` report, append results only; do not overwrite historical data.
- Reflect critical failures in `MASTER_CONTEXT.json` under `constraints` until mitigated.

## Maintenance Guidelines
- Refresh performance benchmarks after major runtime changes (e.g., new telemetry collectors, orchestration modes).
- Add fixtures for new security rules or mission templates as they are introduced.
- Keep manifests and runner options in sync; update this guide whenever commands change.

## Validation Checklist
- [ ] Applicable suites executed with current commands.
- [ ] Telemetry reports updated or run logged as intentionally skipped.
- [ ] Mission notes capture failures, mitigations, and follow-up tasks.
- [ ] No references to calendar dates or sprint milestones remain in test documentation.
