# Tests

This folder stores validation tests.

Current tests use Python `unittest`, mock Notion API behavior, verify `.env` loading with temporary files, and validate the Phase 1 database builder. They cover offline dry-run, read-only inspect mode, data source schema retrieval, one-way relation payloads, relation repair, hard conflicts, idempotency, and sanitized API failures. They do not require live Notion access.

Future tests should verify:

- JSON schema validity.
- Required documentation files.
- Notion schema compatibility.
- Automation behavior after scripts are approved.
