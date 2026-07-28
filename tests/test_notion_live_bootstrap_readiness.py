import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.notion_live_bootstrap_readiness import run_readiness


VALID_ENV = {
    "NOTION_TOKEN": "secret_readiness_token_should_not_appear",
    "NOTION_PARENT_PAGE_ID": "1234567890abcdef1234567890abcdef",
}
BASE_SCHEMA = json.loads(Path("notion/workspace-schema.json").read_text(encoding="utf-8"))


def write_json(data):
    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    with handle:
        json.dump(data, handle)
    return Path(handle.name)


def text(result):
    return "\n".join(result.messages)


class NotionLiveBootstrapReadinessTest(unittest.TestCase):
    def tearDown(self):
        for path in getattr(self, "paths", []):
            path.unlink(missing_ok=True)

    def schema_path(self, schema):
        path = write_json(schema)
        self.paths = getattr(self, "paths", []) + [path]
        return path

    def state_path(self, state):
        path = write_json(state)
        self.paths = getattr(self, "paths", []) + [path]
        return path

    def empty_state_path(self):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        handle.close()
        path = Path(handle.name)
        path.unlink()
        self.paths = getattr(self, "paths", []) + [path]
        return path

    def test_dry_run_performs_no_write_calls_or_network_calls(self):
        result = run_readiness(
            VALID_ENV,
            schema_path=self.schema_path(BASE_SCHEMA),
            state_path=self.empty_state_path(),
        )

        output = text(result)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("no live Notion reads or writes", output)
        self.assertIn("Writes performed: 0", output)

    def test_missing_token_handling(self):
        env = {**VALID_ENV, "NOTION_TOKEN": ""}
        result = run_readiness(env, schema_path=self.schema_path(BASE_SCHEMA), state_path=self.empty_state_path())

        self.assertEqual(result.exit_code, 1)
        self.assertIn("Missing required environment variable: NOTION_TOKEN", text(result))

    def test_missing_parent_page_handling(self):
        env = {**VALID_ENV, "NOTION_PARENT_PAGE_ID": ""}
        result = run_readiness(env, schema_path=self.schema_path(BASE_SCHEMA), state_path=self.empty_state_path())

        self.assertEqual(result.exit_code, 1)
        self.assertIn("Missing required environment variable: NOTION_PARENT_PAGE_ID", text(result))

    def test_secret_redaction(self):
        result = run_readiness(
            VALID_ENV,
            schema_path=self.schema_path(BASE_SCHEMA),
            state_path=self.empty_state_path(),
        )

        output = text(result)
        self.assertIn("NOTION_TOKEN: <redacted>", output)
        self.assertNotIn(VALID_ENV["NOTION_TOKEN"], output)

    def test_deterministic_creation_order(self):
        result = run_readiness(
            VALID_ENV,
            schema_path=self.schema_path(BASE_SCHEMA),
            state_path=self.empty_state_path(),
        )

        self.assertIn("Creation order: Product Catalog, Content Library, Decision Log", text(result))

    def test_relation_dependency_handling(self):
        result = run_readiness(
            VALID_ENV,
            schema_path=self.schema_path(BASE_SCHEMA),
            state_path=self.empty_state_path(),
        )

        output = text(result)
        self.assertIn("- Content Library.Related Product -> Product Catalog", output)
        self.assertIn("- Decision Log.Related Product -> Product Catalog", output)
        self.assertIn("- Decision Log.Related Content -> Content Library", output)
        self.assertIn("Relations phase: skipped until all database IDs are known.", output)

    def test_duplicate_prevention_from_state(self):
        state = {
            "pages": {"Home": {"id": "page-home"}},
            "databases": {"Product Catalog": {"id": "database-product-catalog"}},
        }
        result = run_readiness(
            VALID_ENV,
            schema_path=self.schema_path(BASE_SCHEMA),
            state_path=self.state_path(state),
        )

        output = text(result)
        self.assertIn("- page Home: matched", output)
        self.assertIn("- database Product Catalog: matched", output)
        self.assertIn("- database Content Library: would create", output)

    def test_partial_state_recovery(self):
        state = {
            "pages": {
                "Home": {"id": "page-home"},
                "Brand": {"id": "page-brand"},
            },
            "databases": {
                "Product Catalog": {"id": "database-product-catalog"},
            },
        }
        result = run_readiness(
            VALID_ENV,
            schema_path=self.schema_path(BASE_SCHEMA),
            state_path=self.state_path(state),
        )

        output = text(result)
        self.assertIn("- page Home: matched", output)
        self.assertIn("- page Brand: matched", output)
        self.assertIn("- page Brand/Brand Bible: would create", output)
        self.assertIn("- database Product Catalog: matched", output)
        self.assertIn("- database Decision Log: would create", output)

    def test_operational_databases_are_excluded(self):
        schema = deepcopy(BASE_SCHEMA)
        schema["databases"].append({"name": "Inventory", "properties": [{"name": "Name", "type": "title"}]})
        result = run_readiness(
            VALID_ENV,
            schema_path=self.schema_path(schema),
            state_path=self.empty_state_path(),
        )

        self.assertEqual(result.exit_code, 1)
        output = text(result)
        self.assertIn("Unexpected active database is not approved", output)
        self.assertIn("Operational databases are active: Inventory.", output)

    def test_expected_tree_and_content_are_displayed(self):
        result = run_readiness(
            VALID_ENV,
            schema_path=self.schema_path(BASE_SCHEMA),
            state_path=self.empty_state_path(),
        )

        output = text(result)
        self.assertIn("Aly & Pon", output)
        self.assertIn("|-- Home", output)
        self.assertIn("|   |-- Brand Bible", output)
        self.assertIn("Product Catalog properties:", output)
        self.assertIn("Content Library properties:", output)
        self.assertIn("Decision Log properties:", output)
        self.assertIn("Brand Bible metadata:", output)
        self.assertIn("Home page planned content:", output)


if __name__ == "__main__":
    unittest.main()

