"""Prepare a dry-run-only live bootstrap plan for the Business Knowledge Base."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from dotenv import load_dotenv

try:
    from build_notion_phase1 import (
        APPROVED_DATABASES,
        SCHEMA_PATH,
        load_workspace_schema,
        select_options,
        validate_env,
    )
except ModuleNotFoundError:
    from scripts.build_notion_phase1 import (
        APPROVED_DATABASES,
        SCHEMA_PATH,
        load_workspace_schema,
        select_options,
        validate_env,
    )


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / ".notion-state.json"
WRITE_METHODS = {"POST", "PATCH", "DELETE"}
EXCLUDED_OPERATIONAL_TERMS = {
    "CRM",
    "Finance",
    "Inventory",
    "Recipes",
    "Suppliers",
    "Projects",
    "Tasks",
    "Operations",
    "Website CMS",
    "SEO management",
    "Employee management",
    "Production",
    "Costing",
    "Purchases",
    "Sales",
}


@dataclass
class ReadinessResult:
    exit_code: int = 0
    messages: list[str] = field(default_factory=list)
    blocking_errors: list[str] = field(default_factory=list)


def load_state(path: Path = STATE_PATH) -> tuple[dict[str, Any], list[str]]:
    if not path.exists():
        return {}, []
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return {}, [f"Malformed deployment state JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}."]
    except OSError as exc:
        return {}, [f"Could not read deployment state: {exc.__class__.__name__}."]


def schema_database(schema: dict[str, Any], name: str) -> dict[str, Any]:
    return next(database for database in schema["databases"] if database["name"] == name)


def database_state(state: dict[str, Any], name: str) -> dict[str, Any]:
    return state.get("databases", {}).get(name, {})


def page_state(state: dict[str, Any], name: str) -> dict[str, Any]:
    return state.get("pages", {}).get(name, {})


def stable_status(item_state: dict[str, Any]) -> str:
    stable_keys = {"id", "databaseId", "dataSourceId", "viewId"}
    return "matched" if any(item_state.get(key) for key in stable_keys) else "would create"


def tree_lines() -> list[str]:
    return [
        "Aly & Pon",
        "|-- Home",
        "|-- Brand",
        "|   |-- Brand Bible",
        "|   |-- Inspiration",
        "|   |-- Visual Identity",
        "|   `-- Packaging",
        "|-- Product Catalog",
        "|-- Content Library",
        "|-- Decision Log",
        "`-- Aly & Pon Operating Principles",
    ]


def relation_lines(schema: dict[str, Any]) -> list[str]:
    approved = {
        "Content Library.Related Product",
        "Decision Log.Related Product",
        "Decision Log.Related Content",
    }
    lines: list[str] = []
    for relation in schema.get("relationships", []):
        if relation["from"] in approved:
            lines.append(f"- {relation['from']} -> {relation['to']}")
    return lines


def property_lines(schema: dict[str, Any], database: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for prop in database["properties"]:
        detail = prop["type"]
        if prop["type"] == "select":
            detail += " [" + ", ".join(select_options(prop, schema)) + "]"
        if prop["type"] == "relation":
            detail += f" -> {prop['relatedDatabase']}"
        lines.append(f"- {prop['name']}: {detail}")
    return lines


def planned_action_lines(schema: dict[str, Any], state: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for page in ["Home", "Brand", "Aly & Pon Operating Principles"]:
        lines.append(f"- page {page}: {stable_status(page_state(state, page))}")
    for page in schema["brand"]["pages"]:
        lines.append(f"- page Brand/{page}: {stable_status(page_state(state, f'Brand/{page}'))}")
    for database_name in APPROVED_DATABASES:
        action = stable_status(database_state(state, database_name))
        lines.append(f"- database {database_name}: {action}")
    return lines


def relation_dependency_errors(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for database in schema["databases"]:
        for prop in database["properties"]:
            if prop["type"] == "relation" and prop["relatedDatabase"] not in APPROVED_DATABASES:
                errors.append(f"{database['name']}.{prop['name']} relates to unapproved database {prop['relatedDatabase']}.")
        seen.add(database["name"])
    if [database["name"] for database in schema["databases"]] != APPROVED_DATABASES:
        errors.append("Database creation order does not match approved deterministic order.")
    return errors


def operational_exclusion_errors(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    active_names = {database["name"] for database in schema.get("databases", [])}
    excluded = active_names & EXCLUDED_OPERATIONAL_TERMS
    if excluded:
        errors.append("Operational databases are active: " + ", ".join(sorted(excluded)) + ".")
    return errors


def append_plan(
    result: ReadinessResult,
    schema: dict[str, Any],
    state: dict[str, Any],
    env: Mapping[str, str],
    state_path: Path,
) -> None:
    result.messages.extend(
        [
            "Aly & Pon Business Knowledge Base live-bootstrap readiness dry run",
            "Mode: dry-run only; no live Notion reads or writes will be performed.",
            "Required environment variables are present.",
            "NOTION_PARENT_PAGE_ID format is valid.",
            "NOTION_TOKEN: <redacted>",
            f"Deployment state file: {state_path.name} ({'present' if state_path.exists() else 'not present; first run would create state during later authorized apply'})",
            "workspace-schema.json is valid for Aly & Pon Business Knowledge Base v1.",
            "Creation order: " + ", ".join(APPROVED_DATABASES),
            "Workspace tree:",
        ]
    )
    result.messages.extend(tree_lines())
    result.messages.append("Home page planned content:")
    result.messages.extend(f"- {section}" for section in schema["home"]["sections"])
    metadata = schema["brand"]["brandBibleMetadata"]
    result.messages.append("Brand Bible metadata:")
    result.messages.append(f"- Version: {metadata['version']}")
    result.messages.append(f"- Last Updated: {metadata['lastUpdated']}")
    result.messages.append(f"- Owner: {metadata['owner']}")
    for database_name in APPROVED_DATABASES:
        database = schema_database(schema, database_name)
        result.messages.append(f"{database_name} properties:")
        result.messages.extend(property_lines(schema, database))
    result.messages.append("Intended relationships:")
    result.messages.extend(relation_lines(schema))
    result.messages.append("Object action plan:")
    result.messages.extend(planned_action_lines(schema, state))
    result.messages.extend(
        [
            "Relations phase: skipped until all database IDs are known.",
            "Updates planned: none in dry-run.",
            "Skipped operational databases: CRM, Finance, Inventory, Recipes, Suppliers, Projects, Tasks, Operations, Website CMS, SEO management, Employee management, Production, Costing, Purchases, Sales.",
            "Blocking errors: none",
            "Credentials redacted: yes",
            "Writes performed: 0",
        ]
    )


def run_readiness(
    env: Mapping[str, str],
    *,
    schema_path: Path = SCHEMA_PATH,
    state_path: Path = STATE_PATH,
) -> ReadinessResult:
    result = ReadinessResult()
    values, env_errors = validate_env(env)
    schema, schema_errors = load_workspace_schema(schema_path)
    state, state_errors = load_state(state_path)
    errors = env_errors + schema_errors + state_errors
    if schema is not None:
        errors.extend(relation_dependency_errors(schema))
        errors.extend(operational_exclusion_errors(schema))
    if errors or schema is None:
        result.exit_code = 1
        result.blocking_errors = errors
        result.messages.append("Aly & Pon Business Knowledge Base live-bootstrap readiness dry run")
        result.messages.append("Mode: dry-run only; no live Notion reads or writes will be performed.")
        result.messages.append("Blocking errors:")
        result.messages.extend(f"- {error}" for error in errors)
        result.messages.append("NOTION_TOKEN: <redacted>" if env.get("NOTION_TOKEN") else "NOTION_TOKEN: <missing>")
        result.messages.append("Writes performed: 0")
        return result
    append_plan(result, schema, state, values, state_path)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dry-run live-bootstrap readiness for the Aly & Pon Business Knowledge Base.")
    parser.add_argument("--state-file", default=str(STATE_PATH), help="Path to the ignored deployment state file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    load_dotenv()
    result = run_readiness(os.environ, state_path=Path(args.state_file))
    for message in result.messages:
        print(message)
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
