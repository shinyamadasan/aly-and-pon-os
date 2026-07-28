# Notion Architecture

## Purpose

Notion is the planned business brain for Aly & Pon. This document defines the architecture direction without creating or modifying any Notion workspace.

## Architecture Principles

- Notion stores active business knowledge.
- GitHub stores schema definitions, templates, standards, and automation.
- Google Drive stores assets.
- Every important Notion database should have a clear purpose, owner, and review cadence.
- Automation should be added only after the manual architecture is approved.

## Phase 1 Databases

| Database | Purpose |
| --- | --- |
| Areas | Accountable business areas that organize work and governance. |
| Tasks | Accountable work items across areas. |
| Decisions | Major business, brand, operating, and architecture decisions. |
| Meetings | Meeting records, notes, and resulting tasks or decisions. |
| Approvals | Human review records for tasks and decisions requiring approval. |

## Phase 1 Builder

`scripts/build_notion_phase1.py` builds only the five approved Phase 1 databases from `notion/workspace-schema.json`. Dry-run is the default.

The builder targets Notion API version `2025-09-03`. In that version, a database is a container and schema properties belong to the database's primary data source. The installed Python client does not expose a dedicated `data_sources` endpoint helper, so the builder uses the client's generic request method for `/v1/data_sources` reads and updates.

Apply mode may only:

- Verify access to the configured parent page.
- Inspect direct child databases.
- Match existing databases by exact title.
- Resolve each database container ID and primary data source ID.
- Retrieve schemas from primary data sources.
- Create missing approved Phase 1 databases.
- Add only missing relation properties explicitly defined in `workspace-schema.json`.
- Build one-way relation properties with the related data source ID and `single_property`.
- Skip existing databases whose schemas match.
- Stop safely on same-title schema conflicts.

The builder must not create SOPs, Projects, Assets, Vendors, Brand Standards, or any other future-module database.

Missing approved relation properties are treated as resumable incomplete state. Wrong property types, wrong relation targets, incompatible select options, missing non-relation properties, and unexpected properties are hard conflicts.

Relation repair updates are sent to `PATCH /v1/data_sources/{data_source_id}` with this property shape:

```json
{
  "properties": {
    "Area": {
      "type": "relation",
      "relation": {
        "data_source_id": "<target data source id>",
        "single_property": {}
      }
    }
  }
}
```

The builder does not add `dual_property` unless it is explicitly defined in `notion/workspace-schema.json`, and it does not invent reciprocal relation properties.

## Relationships

- A Task may relate to one Area.
- A Decision may relate to one Area.
- A Meeting may relate to one Area.
- An Approval may relate to one Area.
- A Task may relate to one or more Decisions.
- A Meeting may reference resulting Tasks and Decisions.
- An Approval may reference a Task or Decision.

## Status Systems

Use consistent statuses where practical:

| Status Set | Values | Used By |
| --- | --- | --- |
| Work status | Not Started, In Progress, Blocked, Done, Canceled | Tasks, Meetings |
| Decision status | Proposed, Approved, Rejected, Superseded | Decisions |
| Approval status | Submitted, Approved, Rejected, Changes Requested, Canceled | Approvals |
| Area status | Active, Paused, Archived | Areas |
| Priority | High, Medium, Low | Tasks |

## Future Modules

These modules are intentionally excluded from the Phase 1 workspace schema. They are preserved for later phases after the core operating loop is stable.

| Future Module | Why Later |
| --- | --- |
| SOPs | Standard procedures should follow after tasks, decisions, meetings, and approvals are stable. |
| Projects | Project tracking should be added after task and meeting workflows prove the operating model. |
| Assets | Asset indexing depends on approved Google Drive mapping and naming standards. |
| Vendors | Vendor records should wait until ownership and approval rules are stable. |
| Brand Standards | Brand governance should follow after the brand book and approval flow mature. |

## Integration Status

The repository includes a minimal Notion connectivity test. It does not create databases, modify the parent page, delete content, archive content, or write local state. Dry-run is the default.

Future database integration should begin only after:

- The workspace schema is reviewed.
- Required Notion permissions are documented.
- Seed data is approved.
- Sync rules are defined.

## Safety Rules

- Never delete or archive Notion content automatically.
- Dry-run is the default for write-capable commands.
- Live writes require an explicit `--apply` flag.
- Never expose secrets.
- Operations must be idempotent.
- Stop on unexpected live-schema conflicts.
- Seed data is not approved unless explicitly marked approved.
