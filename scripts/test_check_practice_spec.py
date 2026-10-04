"""Tests for check_practice_spec.py — runs a solution against a practice spec.

Stdlib unittest. Run it with:

    python scripts/test_check_practice_spec.py
"""
from __future__ import annotations

import json
import math
import tempfile
import unittest
from pathlib import Path

import check_practice_spec as cps

SPEC_NUMBER = 7
SPEC_FILENAME = f"{SPEC_NUMBER}_fixture.yml"


def _spec(signature: str, cases: list, compare: str = "exact", **extra) -> dict:
    """A method-kind spec; `extra` adds or replaces top-level keys."""
    return {
        "number": SPEC_NUMBER, "title": "Fixture", "url": "https://example.test/",
        "entry": {"class": "Solution", "method": "f"}, "signature": signature,
        "compare": compare, "cases": cases, **extra,
    }


def _case(args: list, expected, example: bool = False) -> dict:
    return {"args": args, "expected": expected, "example": example}


def _run(spec: dict, source: str, method: str | None = None) -> list[tuple[bool, str]]:
    """Write the fixture pair to a temp dir and return the checker's report lines."""
    with tempfile.TemporaryDirectory() as directory:
        spec_path, solution_path = Path(directory) / SPEC_FILENAME, Path(directory) / "s.py"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")  # JSON is valid YAML
        solution_path.write_text(source, encoding="utf-8")
        return cps.report_lines(cps.load_problem(spec_path, solution_path), method)


PLAIN = _spec("n: int -> bool", [_case([3], True, True), _case([4], False)])
PLAIN_SOURCE = "class Solution:\n    def f(self, n):\n        return n % 2 == 1\n"

LIST_NODE_SOURCE = """
class Solution:
    def f(self, head):
        previous = None
        while head:
            head.next, previous, head = previous, head, head.next
        return previous
"""

CYCLE_SOURCE = """
class Solution:
    def f(self, head):
        seen = set()
        while head:
            if id(head) in seen:
                return True
            seen.add(id(head))
            head = head.next
        return False
"""

RANDOM_SOURCE = """
class Solution:
    def f(self, head):
        copies, node = {None: None}, head
        while node:
            copies[node] = Node(node.val)
            node = node.next
        node = head
        while node:
            copies[node].next = copies[node.next]
            copies[node].random = copies[node.random]
            node = node.next
        return copies[head]
"""

INVERT_SOURCE = """
class Solution:
    def f(self, root):
        if root:
            root.left, root.right = self.f(root.right), self.f(root.left)
        return root
"""

LCA_SOURCE = """
class Solution:
    def f(self, root, p, q):
        if root is None or root is p or root is q:
            return root
        left, right = self.f(root.left, p, q), self.f(root.right, p, q)
        return root if left and right else left or right
"""

CLONE_SOURCE = """
class Solution:
    def f(self, node):
        copies = {}
        def clone(original):
            if original not in copies:
                copies[original] = Node(original.val)
                copies[original].neighbors = [clone(n) for n in original.neighbors]
            return copies[original]
        return clone(node) if node else None
"""

DEDUPE_SOURCE = """
class Solution:
    def f(self, nums):
        kept = sorted(set(nums))
        nums[:len(kept)] = kept
        return len(kept)
"""

OPS_SOURCE = """
class Counter:
    def __init__(self, start):
        self.total = start
    def add(self, amount):
        self.total += amount
    def read(self):
        return self.total
"""

ROUND_TRIP_SOURCE = """
class Codec:
    def encode(self, values):
        return ",".join(map(str, values))
    def decode(self, text):
        return [int(part) for part in text.split(",")]
"""

OPS_SPEC = {
    **_spec("", [{"ops": ["Counter", "add", "read"], "args": [[1], [4], []],
                  "expected": [None, None, 5], "example": True}],
            entry={"class": "Counter", "kind": "ops"},
            methods=["__init__(start: int)", "add(amount: int) -> None", "read() -> int"]),
}
del OPS_SPEC["signature"]

ROUND_TRIP_SPEC = _spec(
    "values: List[int] -> str", [_case([[1, 2, 3]], [1, 2, 3], True)],
    entry={"class": "Codec", "kind": "round-trip", "encode": "encode", "decode": "decode"},
    decodeSignature="text: str -> List[int]")

TREE_LCA_SPEC = _spec(
    "root: TreeNode, p: int, q: int -> int",
    [_case([[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 1], 3, True)],
    types={"args": ["tree-node", "tree-value", "tree-value"], "result": "tree-value"})

GRAPH = [[2, 4], [1, 3], [2, 4], [1, 3]]

ROWS = [
    ("plain pass", PLAIN, PLAIN_SOURCE, None, [(True, "PASS f (2/2)")]),
    ("plain fail reports the case",
     _spec("n: int -> bool", [_case([3], True, True), _case([4], False)]),
     "class Solution:\n    def f(self, n):\n        return True\n", None,
     [(False, "FAIL f (1/2): case 1 expected false got true")]),
    ("unordered", _spec("n: int -> List[int]", [_case([0], [1, 2], True)], "unordered"),
     "class Solution:\n    def f(self, n):\n        return [2, 1]\n", None,
     [(True, "PASS f (1/1)")]),
    ("unordered-nested",
     _spec("n: int -> List[List[int]]", [_case([0], [[1, 2], [3]], True)],
           "unordered-nested"),
     "class Solution:\n    def f(self, n):\n        return [[3], [2, 1]]\n", None,
     [(True, "PASS f (1/1)")]),
    ("list-node",
     _spec("head: ListNode -> ListNode", [_case([[1, 2, 3]], [3, 2, 1], True),
                                          _case([[]], [])],
           types={"args": ["list-node"], "result": "list-node"}),
     LIST_NODE_SOURCE, None, [(True, "PASS f (2/2)")]),
    ("list-node-cycle",
     _spec("head: ListNode -> bool",
           [_case([[[3, 2, 0, -4], 1]], True, True), _case([[[1], -1]], False)],
           types={"args": ["list-node-cycle"], "result": None}),
     CYCLE_SOURCE, None, [(True, "PASS f (2/2)")]),
    ("random-list",
     _spec("head: Node -> Node",
           [_case([[[7, None], [13, 0], [11, 1]]], [[7, None], [13, 0], [11, 1]], True)],
           types={"args": ["random-list"], "result": "random-list"}),
     RANDOM_SOURCE, None, [(True, "PASS f (1/1)")]),
    ("tree-node",
     _spec("root: TreeNode -> TreeNode",
           [_case([[4, 2, 7, 1, 3, 6, 9]], [4, 7, 2, 9, 6, 3, 1], True)],
           types={"args": ["tree-node"], "result": "tree-node"}),
     INVERT_SOURCE, None, [(True, "PASS f (1/1)")]),
    ("tree-value", TREE_LCA_SPEC, LCA_SOURCE, None, [(True, "PASS f (1/1)")]),
    ("graph-node",
     _spec("node: Node -> Node", [_case([GRAPH], GRAPH, True), _case([[]], [])],
           types={"args": ["graph-node"], "result": "graph-node"}),
     CLONE_SOURCE, None, [(True, "PASS f (2/2)")]),
    ("result arg",
     _spec("nums: List[int] -> None", [_case([[3, 1, 2]], [1, 2, 3], True)],
           result={"arg": 0}),
     "class Solution:\n    def f(self, nums):\n        nums.sort()\n", None,
     [(True, "PASS f (1/1)")]),
    ("result arg-prefix",
     _spec("nums: List[int] -> int", [_case([[1, 1, 2]], [1, 2], True)],
           result={"argPrefix": 0}),
     DEDUPE_SOURCE, None, [(True, "PASS f (1/1)")]),
    ("ops", OPS_SPEC, OPS_SOURCE, None, [(True, "PASS Counter (1/1)")]),
    ("round-trip", ROUND_TRIP_SPEC, ROUND_TRIP_SOURCE, None,
     [(True, "PASS Codec (1/1)")]),
    ("dated method names are all picked up", PLAIN,
     "class Solution:\n"
     "    def f_20261001(self, n):\n        return n % 2 == 1\n"
     "    def f_20261002(self, n):\n        return True\n", None,
     [(True, "PASS f_20261001 (2/2)"),
      (False, "FAIL f_20261002 (1/2): case 1 expected false got true")]),
    ("a tuple result compares as the JSON array the site sees",
     _spec("n: int -> List[List[int]]", [_case([0], [[1, 2]], True)]),
     "class Solution:\n    def f(self, n):\n        return [(1, 2)]\n", None,
     [(True, "PASS f (1/1)")]),
    ("a module-level unittest.main() does not stop the load", PLAIN,
     "import unittest\n"
     "class Solution:\n    def f(self, n):\n        return n % 2 == 1\n"
     "unittest.main()\n", None,
     [(True, "PASS f (2/2)")]),
    ("--method picks one", PLAIN,
     "class Solution:\n"
     "    def f_a(self, n):\n        return n % 2 == 1\n"
     "    def f_b(self, n):\n        return True\n", "f_a",
     [(True, "PASS f_a (2/2)")]),
]


class CheckPracticeSpecTests(unittest.TestCase):
    def test_each_shape_passes_and_a_wrong_answer_names_its_case(self):
        for label, spec, source, method, expected in ROWS:
            with self.subTest(label):
                self.assertEqual(_run(spec, source, method), expected)


class DecodeNumberInfTests(unittest.TestCase):
    def test_infinities_become_the_sites_strings_and_everything_else_passes_through(self):
        original = [math.inf, [-math.inf, 3]]
        rows = [
            ("+inf", [math.inf], ["Infinity"]),
            ("-inf", [-math.inf], ["-Infinity"]),
            ("an int", [5, True], [5, True]),
            ("a nested list mixing them", [[math.inf, 2], -math.inf, [[-4]]],
             [["Infinity", 2], "-Infinity", [[-4]]]),
        ]
        for label, value, expected in rows:
            with self.subTest(label):
                self.assertEqual(cps.decode_value(value, "number-inf"), expected)
        with self.subTest("the input list is not mutated"):
            cps.decode_value(original, "number-inf")
            self.assertEqual(original, [math.inf, [-math.inf, 3]])
        with self.subTest("NaN passes through and never matches"):
            decoded = cps.decode_value([math.nan], "number-inf")
            self.assertFalse(cps.values_match(decoded, ["Infinity"], "exact"))


REAL_9001_SPEC = (Path(__file__).resolve().parent.parent / "dsa" / "tests"
                  / "9001_single_source_shortest_path_negative_weights.yml")

BELLMAN_FORD_SOURCE = """
import math

class Solution:
    def shortestPaths(self, n, edges, s, queries):
        dist = [math.inf] * n
        dist[s] = 0
        for _ in range(n - 1):
            for u, v, w in edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        for _ in range(n):
            for u, v, w in edges:
                if dist[u] != math.inf and dist[u] + w < dist[v]:
                    dist[v] = -math.inf
        return [dist[q] for q in queries]
"""


class Real9001SpecTests(unittest.TestCase):
    def test_a_bellman_ford_returning_math_inf_passes_the_real_spec(self):
        with tempfile.TemporaryDirectory() as directory:
            solution_path = Path(directory) / "s.py"
            solution_path.write_text(BELLMAN_FORD_SOURCE, encoding="utf-8")
            lines = cps.report_lines(cps.load_problem(REAL_9001_SPEC, solution_path), None)
        self.assertEqual([is_passing for is_passing, _ in lines], [True], lines)


if __name__ == "__main__":
    unittest.main(verbosity=2)
