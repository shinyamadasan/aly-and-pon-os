# Scripts

This folder stores approved automation entrypoints.

`notion_connection_test.py` is a minimal Notion connectivity test. It loads local `.env` values with `python-dotenv` before reading the process environment. Dry-run is the default. Live writes require `--apply` and are limited to idempotently creating one direct child page named `Aly & Pon Connection Test`.

Future scripts may include:

- Schema validation.
- Documentation checks.
- Controlled Notion sync after approval.
