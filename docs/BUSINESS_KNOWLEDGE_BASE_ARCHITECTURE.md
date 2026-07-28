# Business Knowledge Base Architecture

## Purpose

The Aly & Pon Business Knowledge Base preserves business meaning: brand strategy, product positioning, content planning, and decision history.

It is not an operational system.

Guiding rule: **The app runs the business. Notion explains the business. Git preserves the system.**

## System Boundaries

| Information | Owner |
| --- | --- |
| Brand strategy | Notion |
| Product positioning | Notion |
| Content planning | Notion |
| Business decisions | Notion |
| Inventory | Product Lab App |
| Recipes | Product Lab App |
| Costing | Product Lab App |
| Purchases | Product Lab App |
| Production | Product Lab App |
| Sales | Product Lab App |
| Code | Git |
| Knowledge base schema | Git |
| Automation | Git |

## What Belongs In Notion

Notion stores knowledge that helps Aly & Pon understand and explain the business:

- Brand Bible.
- Inspiration.
- Visual Identity.
- Packaging.
- Product Catalog entries.
- Content Library entries.
- Decision Log entries.
- Operating Principles.

Notion relations should improve context and memory. They should not recreate operational workflows.

## What Belongs In The Product Lab App

The Product Lab App is the operational source of truth. It owns:

- Inventory.
- Recipes.
- Costing.
- Purchases.
- Production.
- Sales.

Operational data should not be copied into Notion for convenience. If a future Notion page references operational work, it should explain the business context, not become the source of record.

## What Belongs In Git

Git owns system definition and automation:

- Code.
- Workspace schema.
- Documentation.
- Operating principles.
- Automation scripts.
- Tests.
- Change history.

Changes to the Business Knowledge Base structure should start in Git, be reviewed, and then be applied to Notion through approved manual changes or guarded automation.

## Automation Model

The approved automation reads `notion/workspace-schema.json`.

The database builder may create or repair only:

- Product Catalog.
- Content Library.
- Decision Log.

The shell bootstrap may create only:

- Home.
- Brand.
- Aly & Pon Operating Principles.
- Brand Bible.
- Inspiration.
- Visual Identity.
- Packaging.
- Approved database views.

Live-deployment readiness is handled by `scripts/notion_live_bootstrap_readiness.py`. It is dry-run only, makes no live Notion reads or writes, and prints the exact proposed workspace tree, database properties, relationships, object action plan, and deployment-state expectations.

Automation rules:

- Dry-run is the default.
- Live writes require `--apply`.
- Inspect mode is read-only.
- Automation must be idempotent.
- Automation must stop on schema conflicts.
- Automation must never delete or archive Notion content automatically.
- Automation must never create operational records.

Deployment state is stored locally in `.notion-state.json`, using `notion/deployment-state.example.json` as the committed shape reference. The state file retains generated Notion IDs for safe matching and resumability, and must not contain credentials.

## Future Schema Changes

Future schema changes should follow this sequence:

1. Confirm the change passes the Aly & Pon Operating Principles.
2. Update `notion/workspace-schema.json`.
3. Update the relevant documentation in `docs/`.
4. Update builder or bootstrap automation only if the schema requires it.
5. Update tests for the approved behavior.
6. Run the full test suite.
7. Record the change in `CHANGELOG.md`.

Add new databases only when recurring work demonstrates a real need for database behavior.

## Release Milestone

Milestone: Business Knowledge Base v1.0  
Status: Implemented

Completed:

- Workspace schema.
- Documentation.
- Builder automation.
- Bootstrap automation.
- Tests.
- Operating principles.
- Knowledge-over-operations architecture.

Pending:

- Create implementation PR.
- Merge to main.

