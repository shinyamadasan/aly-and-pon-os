# Scripts

This folder stores approved automation entrypoints.

`notion_connection_test.py` is a minimal Notion connectivity test. It loads local `.env` values with `python-dotenv` before reading the process environment. Dry-run is the default. Live writes require `--apply` and are limited to idempotently creating one direct child page named `Aly & Pon Connection Test`.

`build_notion_phase1.py` builds or repairs the approved Business Knowledge Base Notion databases from `notion/workspace-schema.json`. Dry-run is the default and performs no Notion reads or writes. `--inspect` performs read-only live planning. Live writes require `--apply` and are limited to the `Product Catalog`, `Content Library`, and `Decision Log` databases plus their approved one-way relation properties.

Relation repairs use `PATCH /v1/data_sources/{data_source_id}` and send relation properties with `type: relation`, the target `relation.data_source_id`, and `relation.single_property: {}`. The script does not add `dual_property` or reciprocal properties unless the schema explicitly defines them.

Commands:

```powershell
python scripts/build_notion_phase1.py
python scripts/build_notion_phase1.py --inspect
python scripts/build_notion_phase1.py --apply
```

`bootstrap_notion_phase2.py` is retained as a guarded bootstrap entrypoint. It must stay aligned with the approved Business Knowledge Base model before live use.

Inspect reports approved database state, approved view target IDs in shortened form, layout, filters, sorts, visible properties, matching/missing/conflict status, and zero planned records for excluded operational systems. Apply performs a complete preflight first.

View comparison normalizes optional empty API values before comparison. Missing, `null`, and `[]` all mean no sorts or visible/display properties; missing and `null` mean no filter. Non-empty differences still conflict.

Commands:

```powershell
python scripts/bootstrap_notion_phase2.py
python scripts/bootstrap_notion_phase2.py --inspect
python scripts/bootstrap_notion_phase2.py --apply
```

`notion_live_bootstrap_readiness.py` is a dry-run-only readiness command for the live deployment phase. It validates configuration and schema, prints the proposed workspace tree, database properties, relationships, object action plan, and deployment-state expectations. It does not instantiate a Notion client and performs no live reads or writes.

Commands:

```powershell
python scripts/notion_live_bootstrap_readiness.py
python scripts/notion_live_bootstrap_readiness.py --state-file .notion-state.json
```

Future scripts may include:

- Schema validation.
- Documentation checks.
- Controlled Notion sync after approval.
