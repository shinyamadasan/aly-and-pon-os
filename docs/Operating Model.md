# Operating Model

## Purpose

This document explains how Aly & Pon separates business knowledge, operational data, assets, and automation.

## System Roles

| System | Role |
| --- | --- |
| Notion | Business Knowledge Base for brand strategy, product positioning, content planning, and business decisions. |
| Product Lab App | Operational source of truth for inventory, recipes, costing, purchases, production, and sales. |
| Google Drive | Asset store for files such as images, documents, contracts, exports, and media. |
| Git | Source of truth for code, schemas, documentation, standards, and automation. |
| Codex | Repository maintainer that proposes and implements changes under human direction. |

## Governance Model

- Humans approve major business and architecture changes.
- Codex may maintain documentation, schemas, and automation when asked.
- Major decisions should be recorded as conclusions, not raw conversations.
- Every knowledge-base page and database must have one clear purpose.
- Business ownership defines responsibility for meaning and quality, not a specific person.

## Knowledge Flow

1. Brand strategy lives in the Brand Bible.
2. Product positioning lives in Product Catalog entries.
3. Content planning lives in the Content Library.
4. Business decisions live in the Decision Log.
5. Operational data lives in the Product Lab App.
6. Repository documentation is updated when approved decisions change architecture.
7. Notion may be updated manually today, and by controlled automation in the future.

## Business Knowledge Base v1 Scope

The approved Notion databases are:

- Product Catalog.
- Content Library.
- Decision Log.

The approved Brand pages are:

- Brand Bible.
- Inspiration.
- Visual Identity.
- Packaging.

## Explicit Exclusions

The Business Knowledge Base v1 must not add CRM, Finance, Inventory, Recipes, Suppliers, Projects, Tasks, Operations, Website CMS, SEO management, Employee management, or Production.

## Automation Safety

Automation must default to dry-run behavior. Live writes require an explicit `--apply` flag, must be idempotent, must never expose secrets, and must stop on unexpected live-schema conflicts. No automation may delete or archive Notion content automatically.

The Notion connectivity test may only verify access to the configured parent page and, in explicit apply mode, idempotently create one direct child page named `Aly & Pon Connection Test`.

The Business Knowledge Base database builder is approved as a guarded command. In dry-run it validates the environment and schema without contacting Notion. In inspect mode it reads live Notion state but performs no writes. In explicit apply mode it may create only the three approved Business Knowledge Base databases under the configured parent page or repair missing approved one-way relation properties.

