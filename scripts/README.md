# Scripts

This folder stores approved automation entrypoints.

`notion_connection_test.py` is a minimal Notion connectivity test. It loads local `.env` values with `python-dotenv` before reading the process environment. Dry-run is the default. Live writes require `--apply` and are limited to idempotently creating one direct child page named `Aly & Pon Connection Test`.

`build_notion_phase1.py` builds or repairs the approved Phase 1 Notion databases from `notion/workspace-schema.json`. Dry-run is the default and performs no Notion reads or writes. `--inspect` performs read-only live planning. Live writes require `--apply` and are limited to the `Areas`, `Tasks`, `Decisions`, `Meetings`, and `Approvals` databases plus their approved one-way relation properties.

Relation repairs use `PATCH /v1/data_sources/{data_source_id}` and send relation properties with `type: relation`, the target `relation.data_source_id`, and `relation.single_property: {}`. The script does not add `dual_property` or reciprocal properties unless the schema explicitly defines them.

Commands:

```powershell
python scripts/build_notion_phase1.py
python scripts/build_notion_phase1.py --inspect
python scripts/build_notion_phase1.py --apply
```

Future scripts may include:

- Schema validation.
- Documentation checks.
- Controlled Notion sync after approval.
