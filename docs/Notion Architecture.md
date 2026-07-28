# Notion Architecture

## Purpose

Notion is the planned Business Knowledge Base for Aly & Pon. It preserves brand strategy, product positioning, content planning, and business decisions. It is not an operational system.

Guiding rule: **The app runs the business. Notion explains the business. Git preserves the system.**

## Approved v1 Structure

Top-level pages:

- Home
- Brand

Brand pages:

- Brand Bible
- Inspiration
- Visual Identity
- Packaging

Approved databases:

| Database | Purpose | Business Owner |
| --- | --- | --- |
| Product Catalog | Brand-facing product documentation. | Product |
| Content Library | Content planning and reusable content knowledge. | Marketing |
| Decision Log | Durable business memory. | Business |

## Builder

`scripts/build_notion_phase1.py` builds only the three approved Business Knowledge Base databases from `notion/workspace-schema.json`. Dry-run is the default.

The builder targets Notion API version `2025-09-03`. In that version, a database is a container and schema properties belong to the database's primary data source. The builder uses the client's generic request method for `/v1/data_sources` reads and updates.

Apply mode may only:

- Verify access to the configured parent page.
- Inspect direct child databases.
- Match existing databases by exact title.
- Resolve each database container ID and primary data source ID.
- Retrieve schemas from primary data sources.
- Create missing approved Business Knowledge Base databases.
- Add only missing relation properties explicitly defined in `workspace-schema.json`.
- Build one-way relation properties with the related data source ID and `single_property`.
- Skip existing databases whose schemas match.
- Stop safely on same-title schema conflicts.

The builder must not create CRM, Finance, Inventory, Recipes, Suppliers, Projects, Tasks, Operations, Website CMS, SEO management, Employee management, or Production databases.

Missing approved relation properties are treated as resumable incomplete state. Wrong property types, wrong relation targets, incompatible select options, missing non-relation properties, and unexpected properties are hard conflicts.

## Relationships

- Content Library may relate to Product Catalog through `Related Product`.
- Decision Log may relate to Product Catalog through `Related Product`.
- Decision Log may relate to Content Library through `Related Content`.
- Product Catalog and Content Library may relate back to Decision Log through `Related Decisions`.

Relations exist for context and memory, not workflow management.

## Status Systems

| Status Set | Values | Used By |
| --- | --- | --- |
| Catalog status | Draft, Active, Retired | Product Catalog |
| Content status | Idea, Draft, Ready, Scheduled, Published | Content Library |
| Decision status | Proposed, Approved, Rejected, Superseded | Decision Log |
| Content type | Photo, Reel, Carousel, Story, Caption, Blog, Email | Content Library |

## Safety Rules

- Never delete or archive Notion content automatically.
- Dry-run is the default for write-capable commands.
- Live writes require an explicit `--apply` flag.
- Never expose secrets.
- Operations must be idempotent.
- Stop on unexpected live-schema conflicts.
- Seed data is not approved unless explicitly marked approved.

