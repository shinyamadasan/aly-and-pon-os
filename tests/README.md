# Tests

This folder stores validation tests.

Current tests use Python `unittest`, mock Notion API behavior, and verify `.env` loading with temporary files. They do not require live Notion access.

Future tests should verify:

- JSON schema validity.
- Required documentation files.
- Notion schema compatibility.
- Automation behavior after scripts are approved.
