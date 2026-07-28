# Notion Live Bootstrap Readiness

## Purpose

This phase prepares the repository to safely bootstrap the approved Aly & Pon Business Knowledge Base v1.0 into a live Notion workspace.

This is not live deployment authorization. No Notion write calls should be made during readiness.

## Required Environment Variables

| Variable | Purpose |
| --- | --- |
| `NOTION_TOKEN` | Internal integration token used by later authorized Notion commands. |
| `NOTION_PARENT_PAGE_ID` | Parent Notion page where the Aly & Pon knowledge base will be created. |

Secrets must be supplied through environment variables or local `.env` files. They must never be committed.

## Share The Parent Page With The Integration

Before any later authorized live deployment:

1. Create or choose the parent Notion page for `Aly & Pon`.
2. Open the page in Notion.
3. Use Notion's share menu to invite the internal integration.
4. Copy the parent page ID into `NOTION_PARENT_PAGE_ID`.
5. Keep the integration token in `NOTION_TOKEN`.

Readiness dry-run validates only that required configuration is present and correctly shaped. It does not verify live Notion access.

## Schema Validation

Run:

```powershell
python scripts/build_notion_phase1.py
```

This validates `notion/workspace-schema.json`, creation order, database properties, select options, and relation targets without live Notion reads or writes.

## Live Bootstrap Readiness Dry Run

Run:

```powershell
python scripts/notion_live_bootstrap_readiness.py
```

The readiness dry-run:

- Makes no Notion API write calls.
- Makes no live Notion reads.
- Validates required configuration.
- Validates the workspace schema.
- Calculates deterministic creation order.
- Displays the exact proposed workspace tree.
- Displays Product Catalog, Content Library, and Decision Log properties.
- Displays intended relationships.
- Displays Brand Bible metadata.
- Displays Home page planned content.
- Reports objects that would be created, matched, updated, or skipped.
- Redacts credentials.
- Reports blocking errors.

Expected tree:

```text
Aly & Pon
|-- Home
|-- Brand
|   |-- Brand Bible
|   |-- Inspiration
|   |-- Visual Identity
|   `-- Packaging
|-- Product Catalog
|-- Content Library
|-- Decision Log
`-- Aly & Pon Operating Principles
```

## Review The Deployment Plan

Before live deployment, review dry-run output for:

- `Blocking errors: none`.
- `Writes performed: 0`.
- The expected workspace tree.
- The three approved databases only.
- The approved database properties and select options.
- The approved relationships.
- No operational databases or records.

## Deployment State

Live deployment should persist generated Notion IDs in the ignored local state file:

```text
.notion-state.json
```

Use `notion/deployment-state.example.json` as the shape reference.

The state file should retain:

- Parent page ID.
- Generated page IDs.
- Generated database container IDs.
- Generated data source IDs.
- Generated view IDs.

The state file must not contain credentials. It is intentionally ignored by Git.

## Later Live Deployment Authorization

Live deployment must be a separate, explicit authorization step. The authorized command may use `--apply`, but only after the dry-run plan has been reviewed.

Readiness work alone does not authorize:

- Creating Notion pages.
- Creating Notion databases.
- Updating schemas.
- Adding relations.
- Creating views.
- Archiving or deleting content.

## Rollback And Partial Failures

Automation must never delete or archive Notion content automatically.

If a later live deployment partially succeeds:

- Stop on the first unexpected conflict or API failure.
- Preserve `.notion-state.json`.
- Re-run dry-run to classify matched and missing objects.
- Resume only after reviewing the updated plan.
- Manually inspect Notion before any corrective live run.

Rollback is manual in Notion unless a future rollback design is explicitly approved.

