"""Tests for export_practice.py — the practice-runner contract generator.

Stdlib unittest, same style as test_showcase.py. Run it with:

    python scripts/test_export_practice.py
"""
from __future__ import annotations

import copy
import datetime as dt
import unittest

import export_practice as ep

TODAY = dt.date(2026, 10, 1)
FILENAME = "90_subsets_ii.yml"

VALID_SPEC = {
    "number": 90,
    "title": "Subsets II",
    "url": "https://leetcode.com/problems/subsets-ii/",
    "statement": "Return the power set.\n",
    "entry": {"class": "Solution", "method": "subsetsWithDup"},
    "signature": "nums: List[int] -> List[List[int]]",
    "compare": "unordered-nested",
    "cases": [
        {"args": [[1, 2, 2]], "expected": [[], [1]], "example": True},
        {"args": [[0]], "expected": [[], [0]]},
    ],
}


def _spec(**overrides) -> dict:
    """VALID_SPEC with `overrides` applied; a value of `...` deletes the key."""
    spec = copy.deepcopy(VALID_SPEC)
    for key, value in overrides.items():
        if value is ...:
            del spec[key]
        else:
            spec[key] = value
    return spec


class ValidationTests(unittest.TestCase):
    def test_every_validation_error_raises_and_a_valid_spec_passes(self):
        rows = [
            ("missing required key", FILENAME, _spec(statement=...)),
            ("number differs from filename", "91_subsets_ii.yml", _spec()),
            ("entry.method missing", FILENAME, _spec(entry={"class": "Solution"})),
            ("entry.method empty", FILENAME,
             _spec(entry={"class": "Solution", "method": "  "})),
            ("compare not a known mode", FILENAME, _spec(compare="sorted")),
            ("cases empty", FILENAME, _spec(cases=[])),
            ("case args not a list", FILENAME,
             _spec(cases=[{"args": "x", "expected": 1, "example": True}])),
            ("case with no expected", FILENAME,
             _spec(cases=[{"args": [1], "example": True}])),
            ("no example case", FILENAME,
             _spec(cases=[{"args": [1], "expected": 1}])),
            ("figure.kind unknown", FILENAME,
             _spec(figure={"kind": "tree", "edgesArg": 0})),
            ("figure arg index not an integer", FILENAME,
             _spec(figure={"kind": "graph", "edgesArg": "0"})),
            ("figure arg index beyond an example case's args", FILENAME,
             _spec(figure={"kind": "grid", "gridArg": 1})),
        ]
        for label, filename, spec in rows:
            with self.subTest(label):
                with self.assertRaises(ep.PracticeError) as ctx:
                    ep.build_payload([(filename, spec)], TODAY)
                self.assertIn(filename, str(ctx.exception))

        with self.subTest("duplicate number across specs"):
            with self.assertRaises(ep.PracticeError):
                ep.build_payload(
                    [(FILENAME, _spec()), ("90_other_title.yml", _spec())], TODAY)

        with self.subTest("valid spec passes"):
            payload = ep.build_payload([(FILENAME, _spec())], TODAY)
            self.assertEqual([p["number"] for p in payload["problems"]], [90])
            self.assertEqual([c["example"] for c in payload["problems"][0]["cases"]],
                             [True, False])
            self.assertIsNone(payload["problems"][0]["figure"])


class RenderStubTests(unittest.TestCase):
    def test_single_and_multi_argument_signatures(self):
        preamble = "from typing import List, Optional\n\n\n"
        rows = [
            ("single arg, no return", "n: int",
             preamble + "class Solution:\n    def isHappy(self, n: int):\n        pass\n"),
            ("multi arg with return", "n: int, edges: List[List[int]] -> List[str]",
             preamble + "class Solution:\n"
             "    def isHappy(self, n: int, edges: List[List[int]]) -> List[str]:\n"
             "        pass\n"),
        ]
        for label, signature, expected in rows:
            with self.subTest(label):
                self.assertEqual(ep.render_stub("Solution", "isHappy", signature), expected)


class StaleReasonsTests(unittest.TestCase):
    def setUp(self):
        self.payload = ep.build_payload([(FILENAME, _spec())], TODAY)

    def test_expected_drift_is_stale_and_generated_at_alone_is_not(self):
        changed_expected = copy.deepcopy(self.payload)
        changed_expected["problems"][0]["cases"][0]["expected"] = [[], [9]]
        changed_date = {**copy.deepcopy(self.payload), "generatedAt": "2026-01-01"}

        self.assertTrue(ep.stale_reasons(self.payload, changed_expected))
        self.assertEqual(ep.stale_reasons(self.payload, changed_date), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
