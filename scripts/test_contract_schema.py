"""Tests for contract_schema.py — schema validation with a local `$ref` registry.

Stdlib unittest, same style as test_showcase.py. Run it with:

    python scripts/test_contract_schema.py
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import contract_schema as cs

DASHBOARD = Path(__file__).resolve().parent.parent / "dashboard"
PROBLEM_SCHEMA = DASHBOARD / "showcase-problem.schema.json"
SAMPLE = DASHBOARD / "showcase" / "733.json"
DANGLING_SCHEMA = {"$schema": "http://json-schema.org/draft-07/schema#",
                   "$ref": "https://unknown.invalid/missing.v1.json"}


def _without_entry_key(payload: dict) -> dict:
    entries = [{k: v for k, v in entry.items() if k != "key"} for entry in payload["entries"]]
    return {**payload, "entries": entries}


class ValidateTest(unittest.TestCase):
    def test_cross_file_ref_resolves_locally_and_dangling_ref_raises(self) -> None:
        committed = json.loads(SAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(cs.validate(committed, PROBLEM_SCHEMA), [])
        self.assertTrue(cs.validate(_without_entry_key(committed), PROBLEM_SCHEMA))

        with tempfile.TemporaryDirectory() as tmp:
            schema_path = Path(tmp) / "dangling.schema.json"
            schema_path.write_text(json.dumps(DANGLING_SCHEMA), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unresolvable"):
                cs.validate({}, schema_path)

    def test_missing_jsonschema_blocks_with_the_install_hint(self) -> None:
        unimportable = {"jsonschema": None, "jsonschema.validators": None}
        stderr = io.StringIO()
        with mock.patch.dict(sys.modules, unimportable), contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as raised:
                cs.validate({}, PROBLEM_SCHEMA)
        self.assertEqual(raised.exception.code, cs.SCHEMA_EXIT_CODE)
        self.assertIn(cs.INSTALL_HINT, stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
