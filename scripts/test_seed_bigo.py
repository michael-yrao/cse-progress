"""Tests for seed_bigo.py — the one-off dashboard/bigo.yml seeder.

Stdlib unittest, mirroring test_showcase.py's style (`write_bytes` fixtures,
`mock.patch.object`, `redirect_stdout`/`redirect_stderr`). Run it with:

    python scripts/test_seed_bigo.py

Runs against the REAL export_bigo module (COMPLEXITY_POOL / TODO_LABEL /
_validate_entry_shape) rather than a stub, so a pool change here is caught immediately.
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

import export_bigo
import seed_bigo as sb


def _write(path: Path, text: str) -> None:
    """Write `text` as literal UTF-8 bytes — matches test_showcase.py's own EOL warning:
    `Path.write_text` would translate `\\n` to the platform line ending on Windows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


# ── normalise_label: the full site spelling-map contract ────────────────────────────────

class NormaliseLabelTests(unittest.TestCase):
    MAPPED = [
        ("O(m × n)", "O(m·n)"),
        ("O(m×n)", "O(m·n)"),
        ("O(V + E)", "O(V+E)"),
        ("O(n + e)", "O(V+E)"),
        ("O(n+e)", "O(V+E)"),
        ("O(m+n)", "O(n + m)"),
        ("O(m + n)", "O(n + m)"),
        ("O(n+m)", "O(n + m)"),
        ("O(n · 2ⁿ)", "O(n·2ⁿ)"),
        ("O(n · α(n))", "O(n·α(n))"),
        ("O(k · E)", "O(k·E)"),
        ("O(n · L²)", "O(n·L²)"),
        ("O(min(n,k))", "O(min(n, k))"),
        ("O(max(m,n))", "O(max(m, n))"),
    ]

    def test_every_known_spelling_maps_to_its_canonical_pool_label(self):
        for raw, expected in self.MAPPED:
            with self.subTest(raw=raw):
                canonical, _qualifier = sb.normalise_label(raw)
                self.assertEqual(canonical, expected)
                self.assertIn(expected, export_bigo.COMPLEXITY_POOL)

    def test_qualifier_is_extracted_and_stripped(self):
        self.assertEqual(sb.normalise_label("O(1) amortized"), ("O(1)", "amortized"))
        self.assertEqual(sb.normalise_label("O(log k) per add"), ("O(log k)", "per add"))
        self.assertEqual(sb.normalise_label("O(1) per operation"), ("O(1)", "per operation"))
        self.assertEqual(sb.normalise_label("O(1) — at most 26 tasks"),
                          ("O(1)", "at most 26 tasks"))

    def test_already_canonical_label_passes_through_with_no_qualifier(self):
        self.assertEqual(sb.normalise_label("O(n)"), ("O(n)", ""))
        self.assertEqual(sb.normalise_label("O(n²)"), ("O(n²)", ""))

    def test_unmappable_problem_specific_label_is_none(self):
        for raw in ("O(D + S)", "O(capacity)", "O(total chars)", "O(NK log NK)",
                    "O(min(n, alphabet))"):
            with self.subTest(raw=raw):
                canonical, _qualifier = sb.normalise_label(raw)
                self.assertIsNone(canonical)

    def test_method_prefixed_label_is_unmappable(self):
        canonical, _qualifier = sb.normalise_label("getNewsFeed O(t log t)")
        self.assertIsNone(canonical)

    def test_no_o_paren_at_all_returns_none(self):
        canonical, qualifier = sb.normalise_label("linear time")
        self.assertIsNone(canonical)
        self.assertEqual(qualifier, "linear time")


class BuildQualifierNoteTests(unittest.TestCase):
    def test_shared_qualifier_used_once(self):
        self.assertEqual(sb.build_qualifier_note("per operation", "per operation"),
                          "per operation")

    def test_differing_qualifiers_labeled_by_axis(self):
        self.assertEqual(sb.build_qualifier_note("per add", "amortized"),
                          "time: per add; space: amortized")

    def test_single_axis_qualifier(self):
        self.assertEqual(sb.build_qualifier_note("per operation", ""), "per operation")
        self.assertEqual(sb.build_qualifier_note("", "per operation"), "per operation")

    def test_no_qualifiers_is_none(self):
        self.assertIsNone(sb.build_qualifier_note("", ""))


# ── parse_steps_file: problem-level pair wins over a variant pair before it ─────────────

class ParseStepsFileTests(unittest.TestCase):
    TASK_SCHEDULER_STYLE = """\
const simVariant: SolutionVariant = {
  label: 'Max-Heap Simulation',
  variant: 'heap-simulation',
  generateSteps: generateSimSteps,
  timeComplexity: 'O(total intervals)',
  spaceComplexity: 'O(1) — at most 26 tasks',
};

export const taskSchedulerMeta: AlgorithmMeta = {
  id: 'task-scheduler',
  lcNumber: 621,
  title: 'Task Scheduler',
  difficulty: 'Medium',
  category: 'greedy',
  timeComplexity: 'O(n)',
  spaceComplexity: 'O(1)',
  solutions: [simVariant],
};
"""

    def test_problem_level_pair_wins_over_a_preceding_variant_pair(self):
        parsed = sb.parse_steps_file(self.TASK_SCHEDULER_STYLE)
        self.assertEqual(parsed["lcNumber"], 621)
        self.assertEqual(parsed["difficulty"], "Medium")
        self.assertEqual(parsed["time"], "O(n)")
        self.assertEqual(parsed["space"], "O(1)")
        self.assertEqual(parsed["variants"], [("O(total intervals)", "O(1) — at most 26 tasks")])

    INLINE_SOLUTIONS_STYLE = """\
export const minStackMeta: AlgorithmMeta = {
  id: 'min-stack',
  lcNumber: 155,
  title: 'Min Stack',
  difficulty: 'Medium',
  timeComplexity: 'O(1) per operation',
  spaceComplexity: 'O(n)',
  solutions: [
    {
      label: 'Pair Min',
      variant: 'pair-min',
      timeComplexity: 'O(1) per operation',
      spaceComplexity: 'O(n)',
    },
  ],
};
"""

    def test_problem_level_pair_wins_when_the_variant_pair_follows_inside_solutions(self):
        parsed = sb.parse_steps_file(self.INLINE_SOLUTIONS_STYLE)
        self.assertEqual(parsed["lcNumber"], 155)
        self.assertEqual(parsed["time"], "O(1) per operation")
        self.assertEqual(parsed["space"], "O(n)")
        self.assertEqual(parsed["variants"], [("O(1) per operation", "O(n)")])

    def test_missing_lc_number_raises(self):
        with self.assertRaises(sb.SeedError):
            sb.parse_steps_file("export const x = { title: 'no lc here' };")

    def test_no_pair_after_lc_number_raises(self):
        with self.assertRaises(sb.SeedError):
            sb.parse_steps_file("export const x = { lcNumber: 1, title: 'no pair' };")


# ── parse_questions: two blocks, including two for the same lc (the LC 206 shape) ───────

class ParseQuestionsTests(unittest.TestCase):
    TEXT = """\
export const BIG_O_QUESTIONS: BigOQuestion[] = [
  {
    id: 'two-sum',
    context: 'Find two indices whose values sum to a target.',
    code: `def two_sum(nums, target):
    return []`,
    timeOptions: ['O(1)', 'O(n)'],
    spaceOptions: ['O(1)', 'O(n)'],
    correctTime: 'O(n)',
    correctSpace: 'O(n)',
    timeExplanation:
      'One pass through n elements.',
    spaceExplanation:
      'The hash map stores at most n entries.',
    category: 'arrays-hash',
    linkedProblemLcNumber: 1,
  },
  {
    id: 'reverse-linked-list-iterative',
    context: 'Reverse a singly linked list in-place (iterative).',
    code: `def reverse_list(head):
    return head`,
    timeOptions: ['O(1)', 'O(n)'],
    spaceOptions: ['O(1)', 'O(n)'],
    correctTime: 'O(n)',
    correctSpace: 'O(1)',
    timeExplanation:
      'Each node visited once.',
    spaceExplanation:
      'Only pointer variables.',
    category: 'linked-list',
    linkedProblemLcNumber: 206,
  },
  {
    id: 'reverse-linked-list-recursive',
    context: 'Reverse a singly linked list in-place (recursive).',
    code: `def reverse_list(head):
    return head`,
    timeOptions: ['O(1)', 'O(n)'],
    spaceOptions: ['O(1)', 'O(n)'],
    correctTime: 'O(n)',
    correctSpace: 'O(n)',
    timeExplanation:
      'n recursive calls.',
    spaceExplanation:
      'n stack frames.',
    category: 'linked-list',
    linkedProblemLcNumber: 206,
  },
];
"""

    def setUp(self):
        self.by_lc = sb.parse_questions(self.TEXT)

    def test_every_linked_lc_number_is_a_key(self):
        self.assertEqual(set(self.by_lc), {1, 206})

    def test_single_block_fields_extracted(self):
        block = self.by_lc[1][0]
        self.assertEqual(block["note"], "Find two indices whose values sum to a target.")
        self.assertEqual(block["correctTime"], "O(n)")
        self.assertEqual(block["correctSpace"], "O(n)")
        self.assertEqual(block["whyTime"], "One pass through n elements.")
        self.assertEqual(block["whySpace"], "The hash map stores at most n entries.")

    def test_two_blocks_for_the_same_lc_both_collected_in_order(self):
        blocks = self.by_lc[206]
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0]["correctSpace"], "O(1)")   # iterative, listed first
        self.assertEqual(blocks[1]["correctSpace"], "O(n)")   # recursive, listed second

    def test_empty_question_array_yields_empty_map(self):
        self.assertEqual(sb.parse_questions("export const BIG_O_QUESTIONS = [];"), {})


class PickQuestionBlockTests(unittest.TestCase):
    ITERATIVE = {"correctTime": "O(n)", "correctSpace": "O(1)"}
    RECURSIVE = {"correctTime": "O(n)", "correctSpace": "O(n)"}

    def test_no_blocks_returns_none(self):
        self.assertEqual(sb.pick_question_block([], "O(n)", "O(1)"), (None, False))

    def test_single_block_is_used_unambiguously(self):
        block, ambiguous = sb.pick_question_block([self.ITERATIVE], "O(n)", "O(1)")
        self.assertIs(block, self.ITERATIVE)
        self.assertFalse(ambiguous)

    def test_matching_pair_disambiguates_lc_206(self):
        block, ambiguous = sb.pick_question_block(
            [self.ITERATIVE, self.RECURSIVE], "O(n)", "O(n)")
        self.assertIs(block, self.RECURSIVE)
        self.assertFalse(ambiguous)

    def test_no_unique_match_falls_back_to_the_first_and_flags_ambiguous(self):
        block, ambiguous = sb.pick_question_block(
            [self.ITERATIVE, self.RECURSIVE], "O(n²)", "O(n²)")
        self.assertIs(block, self.ITERATIVE)
        self.assertTrue(ambiguous)


# ── _site_fields: "seeded-both" vs "seeded-partial" — export_bigo skips a whole entry ───
# when EITHER axis is TODO, so these must stay distinct events, not one flat "seeded".

class SiteFieldsSummaryEventTests(unittest.TestCase):
    def _kinds(self, events) -> list[str]:
        return [e.kind for e in events]

    def test_both_axes_mapped_is_seeded_both_only(self):
        steps_by_lc = {1: {"path": "x.steps.ts", "time": "O(n)", "space": "O(1)"}}
        site = sb._site_fields(1, "1", steps_by_lc, {})
        kinds = self._kinds(site.events)
        self.assertIn("seeded-both", kinds)
        self.assertNotIn("seeded-partial", kinds)
        self.assertNotIn("todo-unmappable", kinds)

    def test_one_unmappable_axis_is_seeded_partial_plus_unmappable(self):
        steps_by_lc = {1: {"path": "x.steps.ts", "time": "O(n)", "space": "O(capacity)"}}
        site = sb._site_fields(1, "1", steps_by_lc, {})
        kinds = self._kinds(site.events)
        self.assertIn("seeded-partial", kinds)
        self.assertNotIn("seeded-both", kinds)
        self.assertIn("todo-unmappable", kinds)
        self.assertEqual(site.entry_fields["time"], "O(n)")
        self.assertEqual(site.entry_fields["space"], export_bigo.TODO_LABEL)

    def test_no_site_match_is_neither_seeded_kind(self):
        site = sb._site_fields(999, "999", {}, {})
        kinds = self._kinds(site.events)
        self.assertIn("todo-no-site-match", kinds)
        self.assertNotIn("seeded-both", kinds)
        self.assertNotIn("seeded-partial", kinds)


class PrintSummaryTests(unittest.TestCase):
    def test_seeded_both_and_partial_are_reported_as_separate_lines(self):
        events = [
            sb.SummaryEvent("seeded-both", "1"),
            sb.SummaryEvent("seeded-partial", "2"),
        ]
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            sb.print_summary(events)
        output = err.getvalue()
        self.assertIn("seeded (both axes): 1 — 1", output)
        self.assertIn("partially seeded (one axis TODO", output)
        self.assertIn(": 1 — 2", output)


# ── render_yaml: round-trips through yaml.safe_load + export_bigo's own shape check ─────

class RenderYamlTests(unittest.TestCase):
    def _result(self, **overrides) -> sb.SeedResult:
        base = dict(entry={"lc": 1, "time": "O(n)", "space": "O(n)"}, folder="arrays_and_hash",
                    verify_comment="seeded from site — verify (two-sum.steps.ts: O(n)/O(n))",
                    time_todo_reason=None, space_todo_reason=None)
        base.update(overrides)
        return sb.SeedResult(**base)

    def test_round_trips_and_passes_export_bigo_shape_validation(self):
        results = [
            self._result(),
            self._result(entry={"lc": 2, "time": "O(n)", "space": "O(1)",
                                 "note": "per operation",
                                 "whyTime": "Each node is visited exactly once, so the work is linear.",
                                 "whySpace": "Only a constant number of pointers are kept."},
                          folder="linked_list", verify_comment=None,
                          time_todo_reason=None, space_todo_reason=None),
            self._result(entry={"lc": 1216, "variant": "backtracking",
                                 "file": "dsa/leetcode/backtracking/1216_valid_palindrome_iii.py",
                                 "symbol": "kPalindrome",
                                 "time": export_bigo.TODO_LABEL, "space": export_bigo.TODO_LABEL},
                          folder="backtracking", verify_comment=None,
                          time_todo_reason="no site match — fill in",
                          space_todo_reason="no site match — fill in"),
        ]
        rendered = sb.render_yaml(results)
        parsed = yaml.safe_load(rendered)

        self.assertEqual(parsed["schemaVersion"], 1)
        self.assertEqual(len(parsed["entries"]), 3)
        for raw_entry in parsed["entries"]:
            export_bigo._validate_entry_shape(raw_entry)

        by_lc = {e["lc"]: e for e in parsed["entries"]}
        self.assertEqual(by_lc[1]["time"], "O(n)")
        self.assertEqual(by_lc[2]["note"], "per operation")
        self.assertEqual(by_lc[2]["whyTime"],
                          "Each node is visited exactly once, so the work is linear.")
        self.assertEqual(by_lc[1216]["variant"], "backtracking")
        self.assertEqual(by_lc[1216]["symbol"], "kPalindrome")
        self.assertEqual(by_lc[1216]["time"], export_bigo.TODO_LABEL)

    def test_seeded_verify_comment_is_present_in_the_text(self):
        rendered = sb.render_yaml([self._result()])
        self.assertIn("seeded from site — verify (two-sum.steps.ts: O(n)/O(n))", rendered)

    def test_todo_reason_comment_is_present_on_its_field_line(self):
        result = self._result(
            entry={"lc": 3, "time": export_bigo.TODO_LABEL, "space": "O(n)"},
            verify_comment="seeded from site — verify (x.steps.ts: weird/O(n))",
            time_todo_reason="site said 'weird'")
        rendered = sb.render_yaml([result])
        self.assertIn("time: TODO  # site said 'weird'", rendered)

    def test_folder_grouping_comment_appears_once_per_folder(self):
        rendered = sb.render_yaml([
            self._result(entry={"lc": 1, "time": "O(n)", "space": "O(n)"}, folder="arrays_and_hash"),
            self._result(entry={"lc": 2, "time": "O(n)", "space": "O(n)"}, folder="arrays_and_hash"),
            self._result(entry={"lc": 3, "time": "O(n)", "space": "O(n)"}, folder="stack"),
        ])
        self.assertEqual(rendered.count("arrays_and_hash"), 1)
        self.assertEqual(rendered.count("── stack ──"), 1)

    def test_container_null_is_rendered_for_a_top_level_design_class(self):
        result = self._result(
            entry={"lc": 155, "symbol": "MinStack", "container": None,
                   "time": "O(1)", "space": "O(n)"},
            verify_comment=None)
        rendered = sb.render_yaml([result])
        self.assertIn("container: null", rendered)
        parsed = yaml.safe_load(rendered)
        self.assertIsNone(parsed["entries"][0]["container"])


# ── CLI: --out refuses to overwrite an existing file without --force ────────────────────

class MainCliOverwriteGuardTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.site = Path(self._tmp.name) / "site"
        self.site.mkdir()
        self.out = Path(self._tmp.name) / "bigo.yml"
        _write(self.out, "schemaVersion: 1\nentries: []\n")

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", argv), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                sb.main()
                code = 0
            except SystemExit as exc:
                code = exc.code or 0
        return out.getvalue(), err.getvalue(), code

    def test_refuses_to_overwrite_without_force(self):
        before = self.out.read_text(encoding="utf-8")
        _out, err, code = self._run(
            ["seed_bigo.py", "--site", str(self.site), "--out", str(self.out)])
        self.assertEqual(code, 1)
        self.assertIn("already exists", err)
        self.assertIn("--force", err)
        self.assertEqual(self.out.read_text(encoding="utf-8"), before)

    def test_nonexistent_site_directory_is_a_clean_error(self):
        _out, err, code = self._run(
            ["seed_bigo.py", "--site", str(Path(self._tmp.name) / "no-such-site"),
             "--out", str(self.out), "--force"])
        self.assertEqual(code, 1)
        self.assertIn("not a directory", err)


if __name__ == "__main__":
    unittest.main()
