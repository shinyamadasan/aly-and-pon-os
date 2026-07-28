# Aly & Pon OS

This repository is the operating system for Aly & Pon, a coffee and bakery business built to become one of the most trusted brands in its category.

It does not contain the product app, inventory system, or recipes. It contains the documentation, templates, schemas, standards, and future automation foundation that help humans and AI preserve the business architecture with consistency.

## Philosophy

- Notion stores business knowledge, not business operations.
- The Product Lab App runs inventory, recipes, costing, purchases, production, and sales.
- Google Drive stores brand, media, legal, finance, and operating assets.
- Git stores code, documentation, templates, schemas, and automation.
- Codex maintains the repository under human direction.
- Humans approve major changes.
- Every major decision should be documented.
- The repository should be understandable to someone joining the company five years from now.

## Repository Map

| Path | Purpose |
| --- | --- |
| `docs/` | Durable business documentation and architecture notes. |
| `templates/` | Reusable document templates for decisions, SOPs, projects, and change proposals. |
| `notion/` | Notion workspace architecture, schema definitions, and future seed data. |
| `scripts/` | Future automation entrypoints. No scripts are implemented yet. |
| `tests/` | Future validation checks for schemas, documentation standards, and automation. |
| `AGENTS.md` | Operating rules for AI agents working in this repository. |
| `ROADMAP.md` | Sequenced plan for building the business operating system. |
| `CHANGELOG.md` | Human-readable record of meaningful repository changes. |

Start with `docs/BUSINESS_KNOWLEDGE_BASE_ARCHITECTURE.md` for the current Business Knowledge Base architecture.

## Current Scope

The current repository foundation focuses on:

- Brand and operating principles.
- Documentation standards.
- Google Drive mapping.
- Notion Business Knowledge Base planning.
- An approved Notion Business Knowledge Base schema.
- Templates for repeatable business documentation.

## Notion Commands

Human approval is required before running any write-capable Notion command. Dry-run is the default and does not perform live Notion writes.

Install:

```powershell
python -m pip install -r requirements.txt
```

Test:

```powershell
python -m unittest discover -s tests
```

Connectivity dry-run:

```powershell
python scripts/notion_connection_test.py
```

Connectivity apply:

```powershell
python scripts/notion_connection_test.py --apply
```

The script loads local `.env` values with `python-dotenv`, then reads `NOTION_TOKEN` and `NOTION_PARENT_PAGE_ID` from the process environment. Existing process environment variables are not overwritten by default. It never prints the token. In apply mode it only verifies parent-page access and idempotently creates a direct child page named `Aly & Pon Connection Test` if that page does not already exist.

Business Knowledge Base dry-run:

```powershell
python scripts/build_notion_phase1.py
```

Business Knowledge Base inspect:

```powershell
python scripts/build_notion_phase1.py --inspect
```

Business Knowledge Base apply:

```powershell
python scripts/build_notion_phase1.py --apply
```

The Business Knowledge Base builder reads `notion/workspace-schema.json` and may create only the approved `Product Catalog`, `Content Library`, and `Decision Log` databases when `--apply` is explicitly provided. Offline dry-run performs no Notion reads or writes. Inspect mode performs read-only planning. Apply mode inspects all three databases before writing, stops on hard schema conflicts, and can safely resume a partial build by adding only missing approved one-way relation properties.

Business Knowledge Base shell dry-run:

```powershell
python scripts/bootstrap_notion_phase2.py
```

Business Knowledge Base shell inspect:

```powershell
python scripts/bootstrap_notion_phase2.py --inspect
```

Business Knowledge Base shell apply:

```powershell
python scripts/bootstrap_notion_phase2.py --apply
```

The Business Knowledge Base shell command may create only approved Home, Brand, Brand child pages, and database views. Inspect reports approved database completion, each approved view target, layout, filters, sorts, visible property configuration, and the apply endpoint. Apply performs full preflight before writing and creates database views before pages. It does not create operational records or business facts.

## Out of Scope

- Product application code.
- Inventory management.
- Recipe databases.
- Future-module Notion database creation.
- GitHub workflow changes.

## Working Agreement

Use this repository as the source of truth for architecture and operating standards. Use Notion for business knowledge once the workspace is connected. Use the Product Lab App for operations. Use Google Drive for files and assets that should not live in Git.
