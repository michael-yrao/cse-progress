"""Tests for `.claude/hooks/rating_gate.py`'s COMFORT regex hyphen fix.

Stdlib unittest, same style as test_gamify.py. rating_gate.py lives under `.claude/hooks/`
(not `scripts/`, and not on `sys.path` as a package), so it is loaded by file path via
`importlib` rather than a normal import — the pattern any test for a hook script needs.

This is the first test file for rating_gate.py. It targets one regression: `\\bclean\\b`
treated a hyphen as a word boundary, so the comfort-word alternation matched "spec-clean"
and "clean-ish" as if they were the standalone word "clean". That false-fired the Stop hook
on the 2026-09-22 agent-portability plan summary turn (no rep, no rating, no learner in the
loop) — see `.claude/memory/self_eval_log.md` 2026-09-22 and
`docs/cse-coach/AGENT_PORTABILITY_PLAN.md` §2.6.

    python -m pytest scripts/test_rating_gate.py
    python scripts/test_rating_gate.py
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOOK_PATH = REPO / ".claude" / "hooks" / "rating_gate.py"


def _load_hook():
    """Import rating_gate.py by file path — it is not a package under scripts/."""
    spec = importlib.util.spec_from_file_location("rating_gate", HOOK_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rating_gate = _load_hook()


class ComfortRegexHyphenTests(unittest.TestCase):
    """Direct regex tests: a hyphen-joined token must not read as the bare word."""

    def test_spec_clean_does_not_match(self):
        self.assertIsNone(rating_gate.COMFORT.search("the frontmatter is spec-clean now"))

    def test_clean_ish_does_not_match(self):
        self.assertIsNone(rating_gate.COMFORT.search("that trace looks clean-ish to me"))

    def test_non_clean_does_not_match(self):
        self.assertIsNone(rating_gate.COMFORT.search("a non-clean run of the build"))

    def test_standalone_word_still_matches(self):
        self.assertIsNotNone(rating_gate.COMFORT.search("I'd rate this clean."))

    def test_standalone_word_at_line_start_still_matches(self):
        self.assertIsNotNone(rating_gate.COMFORT.search("Clean, no hints needed."))

    def test_shaky_and_blank_get_the_same_hyphen_exclusion(self):
        self.assertIsNone(rating_gate.COMFORT.search("a half-shaky read on this one"))
        self.assertIsNone(rating_gate.COMFORT.search("not quite blank-page territory"))
        self.assertIsNotNone(rating_gate.COMFORT.search("that felt shaky throughout"))


class ProposesRatingHyphenTests(unittest.TestCase):
    """Integration level: the false-fire reproduced through the full turn-level function."""

    def test_hyphen_joined_comfort_word_is_not_a_proposal(self):
        turn = (
            "Status: approved 2026-09-22 — spec-clean frontmatter, no mirror. "
            "Confirm the layout?"
        )
        self.assertFalse(rating_gate.proposes_rating(turn))

    def test_genuine_proposal_with_standalone_word_still_trips(self):
        turn = "I'd rate this clean. Confirm?"
        self.assertTrue(rating_gate.proposes_rating(turn))


if __name__ == "__main__":
    unittest.main()
