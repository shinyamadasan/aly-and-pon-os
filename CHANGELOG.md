# Changelog

All meaningful changes to the Aly & Pon OS repository should be documented here.

The format follows a simple date-based log. This repository is currently pre-release.

## 2026-07-28

### Added

- Created the initial repository foundation for Aly & Pon OS.
- Added core business architecture documentation under `docs/`.
- Added Notion workspace planning files under `notion/`.
- Added reusable documentation templates under `templates/`.
- Added placeholders for future scripts and tests.
- Added AI agent operating instructions in `AGENTS.md`.
- Added a safe, idempotent Notion connectivity test script with dry-run default behavior.
- Added mocked tests for dry-run, environment validation, existing-page detection, page creation, API failures, and secret redaction.
- Added the minimum Notion Python client dependency declaration.
- Added `python-dotenv` so the connectivity test can load local `.env` values without exposing secrets.

### Changed

- Expanded `README.md` from a short description into a repository guide.
- Narrowed the Phase 1 Notion schema to Areas, Tasks, Decisions, Meetings, and Approvals.
- Moved SOPs, Projects, Assets, Vendors, and Brand Standards into future-module planning.
- Updated Notion architecture and operating model documentation to match the Phase 1 schema.
- Added Notion safety rules to `AGENTS.md` and the workspace schema.
- Documented Notion connectivity setup, test, dry-run, and apply commands in `README.md`.
- Documented `.env` loading behavior for the Notion connectivity test.
