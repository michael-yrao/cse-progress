"""Emit an honest-progress data contract (progress.json) for the practice log.

This is the source-tier half of the gamification feature: it reads the records
that already exist — the DSA tracker, the weekly schedules, the technique-coverage
view — and emits ONE machine-readable file that a viewer (progressiveoverflow.com)
renders as a dashboard. Per the intervention ladder, a tool that emits the value
outranks a rule that asks someone to compute it.

    dsa_progress.md  +  schedules/*.md  +  technique_coverage.md  ->  progress.json

Design constraints this file honours (see docs/ARCHITECTURE.md and CLAUDE.md):

  * HONEST PROCESS ONLY. Every number here is earnable only by genuine learning —
    showing up (streak), problems maturing up the ladder (pipeline / trophy case),
    technique breadth (coverage). Nothing rewards raw volume or a self-reported
    rating, so nothing here creates pressure to inflate a comfort call.

  * SINGLE SOURCE OF TRUTH. Tuned thresholds are read from cse.config.yml's
    `gamification:` block; a DEFAULT_CONFIG fallback exists only for a pre-config
    run and ANNOUNCES itself when it fires. The badge CATALOG (names / icons /
    descriptions) is content, not a tuned number, so it lives here.

  * CURATED / NON-SENSITIVE. progress.json carries aggregate stats, per-problem
    status and a comfort timeline, and links — never solution code, never
    stuck-log prose. The source repo can be public without exposing struggle notes.

  * FAIL-SOFT. A parse gap degrades to partial output with a visible note; it never
    raises out of the hook. Windows cp1252 consoles get force_utf8() like every
    other script here.

Usage:
    python scripts/gamify.py                 # write progress.json + progress-summary.json (+ README badge)
    python scripts/gamify.py --validate       # compute + validate schema, write nothing
    python scripts/gamify.py --banner         # one honest line for the SessionStart hook
    python scripts/gamify.py --stdout         # print the JSON instead of writing it
    python scripts/gamify.py --date 2026-09-20  # override the resolved session date

Two files, one build. progress.json is the full contract (includes `problems[]`, the
144 KB heavy part). progress-summary.json is the same payload minus `problems[]`, with a
COMPACT trophyCase (graduated entries drop their timeline/repDates) — a few KB, cheap
enough for a dashboard landing to fetch on every page view without mounting per-problem
components. See summary_of().
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import json
import re
import sys
from pathlib import Path

import _console

# effort_budget already solves tracker parsing and schedule discovery; reuse it rather
# than re-deriving the same regexes (DRY, and it keeps the two in lockstep).
import effort_budget as eb

# A session that runs past midnight keeps its START date — see session_date.py and
# feedback_session_dating. main() resolves "today" through it instead of dt.date.today()
# so gamify doesn't silently roll a late-night regeneration onto the next calendar day.
import session_date

# "Which file is problem N" comes from links.solution_files() (keyed by the leading number,
# same walk as links.find_file) — reused rather than re-globbed here so a problem's `file`
# field can never disagree with the `[file]` link the coach pastes in chat. (seed_bigo.py
# still carries its own one-off glob; folding it onto links is a follow-up.)
import links

_console.force_utf8()

REPO = Path(__file__).resolve().parent.parent
TRACKER = REPO / "docs/foundations/dsa/mastery/dsa_progress.md"
COVERAGE = REPO / "docs/foundations/dsa/mastery/technique_coverage.md"
TECHNIQUES_YML = REPO / "docs/foundations/dsa/mastery/techniques.yml"
PROBES_README = REPO / "dsa/probes/README.md"
LEETCODE = REPO / "dsa/leetcode"
# The generated contract lives under dashboard/ (moved out of the repo root Sep 21, 2026 to
# keep root uncluttered). The website fetches dashboard/progress-summary.json first, with the
# old root path as a fallback, so this relocation is backward-compatible.
DASHBOARD = REPO / "dashboard"
OUT = DASHBOARD / "progress.json"
OUT_SUMMARY = DASHBOARD / "progress-summary.json"
README = REPO / "README.md"
CONFIG = REPO / "cse.config.yml"

SCHEMA_VERSION = 1
SITE = "https://progressiveoverflow.com"

# The summary's studyDays is a ROLLING WINDOW, not the lifetime list: it exists only to draw
# the site's streak-calendar heatmap (~20 weeks visible), and without a cap it grows by one
# entry per practice day forever. The lifetime COUNT already lives in streak.studyDays and
# streak.longest — nothing is lost by trimming the date list itself. 183 days (~26 weeks)
# gives the calendar a little slack beyond what it renders.
SUMMARY_STUDY_DAYS_WINDOW = 183

# The comfort ladder as an ordinal, so a timeline can be plotted as a step chart.
# Keyed by glyph, never by the words blank/shaky/clean/graduated (the config scrape
# hazard — see cse.config.yml). 🏆 Retired is terminal, above 🎓.
LEVEL = {"🔴": 0, "🟡": 1, "🟢": 2, "🎓": 3, "🏆": 4}

# graduatedCount's bar (Sep 26, 2026): a technique's problem counts once it reaches 🎓 or
# better. UNTRACKED_LEVEL is below LEVEL's own floor (🔴 = 0) so an LC number with no
# tracker row (comfort_by_number has nothing for it) never accidentally counts as graduated.
GRADUATED_LEVEL = LEVEL["🎓"]
UNTRACKED_LEVEL = -1

# Announced fallback — used only when cse.config.yml has no `gamification:` block or
# PyYAML is unavailable. Neutral key names on purpose: none contains the substrings
# blank/shaky/clean/graduated, which a word-keyed config scrape searches for.
DEFAULT_CONFIG = {
    "streak_rest_day_allowance": 1,   # missed days tolerated before a streak breaks
    "streak_milestones": [7, 30, 100],
    "trophy_milestones": [1, 10, 25, 50],   # 🎓 + 🏆 combined
    "on_schedule_target": 0.9,        # fraction of active rows not overdue
}


# ── config ────────────────────────────────────────────────────────────────────────

def load_config() -> tuple[dict, bool]:
    """Return (gamification config, used_fallback). Tolerant like effort_budget's."""
    try:
        import yaml  # noqa: PLC0415
        loaded = yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}
        cfg = loaded.get("gamification")
        if not cfg:
            return dict(DEFAULT_CONFIG), True
        merged = {**DEFAULT_CONFIG, **cfg}
        return merged, False
    except Exception:  # noqa: BLE001 — a missing config is a normal state, not an error
        return dict(DEFAULT_CONFIG), True


# ── retired list + category map (data the tracker table alone does not carry) ───────

RETIRED_ENTRY = re.compile(r"^\s*-\s*(\d+)\.\s*(.+?)\s*(?:—|--)\s*retired\s*(\d{4}-\d{2}-\d{2})",
                           re.MULTILINE)


def parse_retired() -> list[dict]:
    """The `## 🏆 Retired` plain-bullet list at the tail of the tracker.

    Retired rows leave the 7-column table, so parse_rows() never sees them; they are
    the terminal trophy tier and belong in the trophy case. `_None yet._` -> [].
    """
    try:
        text = TRACKER.read_text(encoding="utf-8")
    except OSError:
        return []
    m = re.search(r"##\s*🏆\s*Retired(.*)$", text, re.S)
    if not m:
        return []
    return [{"lcNumber": int(n), "title": t.strip(), "retiredOn": d}
            for n, t, d in RETIRED_ENTRY.findall(m.group(1))]


PROBLEM_URL = re.compile(r"\[(\d+)\.[^\]]*\]\((https?://[^)]+)\)")


def problem_urls() -> dict[int, str]:
    """LeetCode number -> its canonical URL, from the tracker's markdown links.

    parse_rows() drops the URL; the dashboard wants it to deep-link each problem, so
    read it here rather than guessing a slug from the (method-suffixed) title.
    """
    try:
        text = TRACKER.read_text(encoding="utf-8")
    except OSError:
        return {}
    return {int(n): url for n, url in PROBLEM_URL.findall(text)}


def category_map() -> dict[int, str]:
    """LeetCode number -> technique folder, scanned from the solution tree.

    The folder name is the technique (the site's algorithm categories mirror these
    exactly), so this is how a problem gets grouped and deep-linked to its visualizer.
    """
    out: dict[int, str] = {}
    if not LEETCODE.is_dir():
        return out
    for path in LEETCODE.rglob("*.py"):
        m = re.match(r"(\d+)_", path.name)
        if m:
            out.setdefault(int(m.group(1)), path.parent.name)
    return out


# ── schedule index: date -> {problem number -> comfort glyph earned that rep} ───────

def build_schedule_index() -> dict[str, dict[int, str]]:
    """Reconstruct the comfort EARNED per rep, per problem, from the weekly schedules.

    The tracker stores only a problem's CURRENT comfort; the per-rep history lives in
    the schedules' End column (`🟢 s1 → 🎓`). Scan every week (live + archive), resolve
    each daily block's real date from the filename stamp, and record the End glyph
    (falling back to Start) for each problem number. A rep date with no schedule (the
    pre-archive era) simply gets no entry — the timeline degrades to an activity dot,
    it is never fabricated.
    """
    index: dict[str, dict[int, str]] = {}
    for folder in (eb.SCHEDULES, eb.SCHEDULES / "archive"):
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*_schedule.md")):
            stamp = path.name.split("_")[0]
            if len(stamp) != 8 or not stamp.isdigit():
                continue
            try:
                week_start = dt.date(int(stamp[:4]), int(stamp[4:6]), int(stamp[6:]))
            except ValueError:
                continue
            _scan_week(path, week_start, index)
    return index


def build_workload(rows: list[dict], cfg: dict) -> list[dict]:
    """One entry per scheduled day (live + archive) with a header or priced rows.

    `done`/`built` are priced under the CURRENT cse.config.yml weights, not whatever
    a day was billed at when it was built — so the series is comparable to today's
    numbers, never to what a schedule's own Start column implied at build time (see
    decisions.yml `workload-series`). A day with no header AND no rows (the
    pre-2026-08-10 one-row-per-day era, or a week not yet built) contributes no
    entry rather than a fabricated zero.
    """
    workload: list[dict] = []
    for folder in (eb.SCHEDULES, eb.SCHEDULES / "archive"):
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*_schedule.md")):
            stamp = path.name.split("_")[0]
            if len(stamp) != 8 or not stamp.isdigit():
                continue
            try:
                week_start = dt.date(int(stamp[:4]), int(stamp[4:6]), int(stamp[6:]))
            except ValueError:
                continue
            for offset in range(7):
                day = week_start + dt.timedelta(days=offset)
                items, stated = eb.parse_schedule_day(path, day)
                if stated is None and not items:
                    continue
                p = eb.price_day_items(day, items, rows, cfg)
                workload.append({
                    "date": day.isoformat(),
                    "planned": stated,
                    "done": round(p["done"], 1),
                    "built": round(p["built"], 1),
                    "partial": bool(p["unpriced"] or p["guessed"]),
                })
    workload.sort(key=lambda w: w["date"])
    return workload


def _weekday_lookup(week_start: dt.date) -> dict[tuple[str, str, int], str]:
    return {(d.strftime("%a"), d.strftime("%b"), d.day): d.isoformat()
            for d in (week_start + dt.timedelta(days=o) for o in range(7))}


def _end_glyph(cell: str | None) -> str | None:
    """The first comfort glyph (🔴🟡🟢🎓) in a schedule cell, or None for a glyph-less one
    (`unrated`, `—`, `✅ delivered`, empty). Self-contained (only eb.GLYPH) so it ports
    verbatim wherever a schedule cell needs the same read — the comfort timeline's End
    column here, and the board slice's endComfort in _schedule_item_outcome below."""
    if not cell:
        return None
    match = eb.GLYPH.search(cell)
    return match.group(0) if match else None


def _scan_week(path: Path, week_start: dt.date, index: dict[str, dict[int, str]]) -> None:
    lookup = _weekday_lookup(week_start)
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        header = eb.DAY_HEADER.search(line)
        if header:
            current = lookup.get((header["wd"], header["mon"], int(header["day"])))
            continue
        if current is None:
            continue
        row = eb.SCHED_ROW.match(line)
        if not row:
            continue
        num = eb.SCHED_NUM.search(row["c1"] or "")
        if not num:
            continue
        glyph = _end_glyph(row["c3"]) or _end_glyph(row["c2"])
        if glyph:
            index.setdefault(current, {})[int(num.group(1))] = glyph


# ── this week's board (the "what do I do today" drill) ──────────────────────────────

# The legend's tag glyphs (see any schedule file's "Tags:" line) — stripped from a title's
# front so the dashboard shows the problem name, not the build-time tag. → is a real arrow,
# not emoji, but it prefixes a moved row the same way, so it's in the same strip set.
_SCHEDULE_TAGS = "⚠️🔥🆕🎯⚙️🔤→"
_LEADING_TAGS = re.compile(rf"^[{re.escape(_SCHEDULE_TAGS)}\s]+")
_LEADING_NUM = re.compile(r"^\d+\.?\s*")
DAY_LABEL = re.compile(r"units\s*—\s*(?P<label>[^|]+)")

# Same legend, named this time (not just stripped): a dashboard row that shows only the
# cleaned title loses WHY a problem is on today's board, so each glyph also becomes a
# machine-readable tag string. Some of these glyphs are two codepoints (a base symbol plus
# a U+FE0F variation selector, e.g. ⚠️/⚙️) — a `for ch in text` scan would split one of
# those in two and match neither half, so _leading_tags() below matches whole tokens.
TAG_PROTECTED = "protected"
TAG_BACKFILL = "backfill"
TAG_NEW = "new"
TAG_PROBE = "probe"
TAG_VARIANT = "variant"
TAG_PRIMER = "primer"
TAG_MOVED = "moved"
TAG_BY_GLYPH = {
    "⚠️": TAG_PROTECTED,
    "🔥": TAG_BACKFILL,
    "🆕": TAG_NEW,
    "🎯": TAG_PROBE,
    "⚙️": TAG_VARIANT,
    "🔤": TAG_PRIMER,
    "→": TAG_MOVED,
}
# Longest-first so a two-codepoint glyph is never accidentally matched by its own leading
# codepoint alone.
_TAG_TOKEN = re.compile("|".join(re.escape(g) for g in sorted(TAG_BY_GLYPH, key=len, reverse=True)))
# A row's tag glyph is sometimes written struck (`~~`) or bolded (`**`) rather than plain
# — several older archived weeks do this (e.g. `~~🆕 39 ...~~`, `~~**🎯 Probe #3**~~`, even
# stacking both markers). `+` so a run of either marker, in either order, is consumed in
# one go.
_LEADING_EMPHASIS = re.compile(r"^(?:~~|\*\*)+")

KIND_REP = "rep"
KIND_COMPLEXITY = "complexity"
# KIND_NEW/KIND_PRIMER/KIND_PROBE deliberately don't exist: those three `kind` values are
# always exactly the TAG_NEW/TAG_PRIMER/TAG_PROBE tag word, so reusing the tag constant
# keeps the two in lockstep instead of two literals that could drift apart.
TECHNIQUE_COMPLEXITY = "complexity"


def _leading_tags(cell: str) -> list[str]:
    """The row's build-time tags, read off the Problem cell's leading glyph run (see the
    legend on any schedule file's "Tags:" line) and named via TAG_BY_GLYPH.

    Matches whole glyph tokens left-to-right rather than iterating characters, because a
    two-codepoint glyph (⚠️, ⚙️) would otherwise be split into a base codepoint plus a
    stray U+FE0F variation selector that matches nothing.

    A glyph is sometimes struck or bolded rather than written plain — a row may be
    written `~~🆕 39 ...~~` (the whole row struck ahead of its tag) or, stacked with
    another tag, `🔥 ~~🎯 ...~~` — so a leading `~~`/`**` run is stripped (_LEADING_EMPHASIS)
    before EVERY glyph match attempt, not just once at the very front of the cell.
    """
    tags: list[str] = []
    rest = cell.lstrip()
    while True:
        rest = _LEADING_EMPHASIS.sub("", rest).lstrip()
        token = _TAG_TOKEN.match(rest)
        if not token:
            break
        tags.append(TAG_BY_GLYPH[token.group(0)])
        rest = rest[token.end():].lstrip()
    return tags


def _schedule_item_kind(technique: str | None, tags: list[str]) -> str:
    """rep|new|probe|complexity|primer for one schedule item.

    `complexity` is checked BEFORE any tag: the three Sunday complexity re-ask rows are
    both 🎯-tagged (they're still a cold-call-style probe) AND carry `Complexity` in the
    Technique cell, and Complexity is the more specific fact about what the row actually
    tests. Checking the 🎯 tag first would silently reclassify those rows as an ordinary
    probe and lose that distinction on the dashboard.
    """
    if technique is not None and technique.strip().lower() == TECHNIQUE_COMPLEXITY:
        return KIND_COMPLEXITY
    if TAG_NEW in tags:
        return TAG_NEW
    if TAG_PRIMER in tags:
        return TAG_PRIMER
    if TAG_PROBE in tags:
        return TAG_PROBE
    return KIND_REP


_LEADING_SCHED_NUM = re.compile(r"^\s*(\d+)\b")


def _schedule_item_lc_number(cell: str, text: str) -> int | None:
    """lcNumber for one schedule item: eb.SCHED_NUM first (the same parse effort_budget.py
    prices with, so pricing and the dashboard never disagree on the common case), then a
    fallback for a bare-number 🆕 intake row, which has no `[`/`**` before its number for
    SCHED_NUM to find (by design — see effort_budget.py; that miss is fine for PRICING,
    which only needs to know a row exists, not its number).

    The fallback reads off `text` — the tag-stripped, link-unwrapped title string
    _clean_schedule_title also starts from — so a leading tag glyph never gets misread as
    part of the number.
    """
    num = eb.SCHED_NUM.search(cell)
    if num:
        return int(num.group(1))
    stripped = _LEADING_TAGS.sub("", text)
    fallback = _LEADING_SCHED_NUM.match(stripped)
    return int(fallback.group(1)) if fallback else None


_ROW_OWN_LC_URL = re.compile(r"\[LC\]\((https?://[^)]+)\)")
_ROW_OWN_NC_URL = re.compile(r"\[NC\]\((https?://[^)]+)\)")


def _schedule_item_url(cell: str, lc_number: int | None, urls: dict[int, str]) -> str | None:
    """Canonical LeetCode/NeetCode URL for one schedule item, in precedence order:

    1. The row's own `[LC](...)` link straight off the raw cell — a 🆕 row not yet in the
       tracker has no other way to get a URL, and a tracked row's own link is the more
       current fact about THIS occurrence if the two ever disagree.
    2. The tracker join by lcNumber (urls.get, from problem_urls()) — a LeetCode URL.
    3. The row's own `[NC](...)` link, LAST resort only: a NeetCode mirror is used when
       the LC problem is premium-gated (e.g. this week's 1102 build note), so it is real
       but weaker evidence than either LC source above — the dashboard renders this field
       as "LeetCode ↗", and an NC url must never win over an actual LC one.

    Honest null when none of the three has one.
    """
    lc = _ROW_OWN_LC_URL.search(cell)
    if lc:
        return lc.group(1)
    tracked = urls.get(lc_number) if lc_number else None
    if tracked:
        return tracked
    nc = _ROW_OWN_NC_URL.search(cell)
    return nc.group(1) if nc else None


def _clean_schedule_title(text: str) -> str:
    """Turn a Problem-column cell (already link-unwrapped, `~~`/`**` stripped — see
    eb.parse_schedule_day) into a display title.

    eb.parse_schedule_day stops at what PRICING needs (the text is only ever printed
    in a debug line), so it leaves the tag glyphs, the LC number, and the second link's
    unwrapped anchor text ("· LC") sitting in the string. A dashboard row shows the
    number and comfort separately, so all three would just be noise here: split off
    everything from the first " · " on (that is always the `[LC](...)` link, sometimes
    followed by a build note — neither belongs in the title), then strip a leading tag
    glyph and a leading LC-number prefix.
    """
    first = text.split(" · ")[0]
    first = _LEADING_TAGS.sub("", first)
    first = _LEADING_NUM.sub("", first)
    return re.sub(r"\s+", " ", first).strip()


# The E cell's outcome note (`s0`/`s1`/`s2`/`prov`/`dropped`) is written after the glyph,
# sometimes with a leading arrow (`🟡→dropped`) rather than a space — both are stripped
# before the note is kept.
_NOTE_LEADING_STRIP = re.compile(r"^[\s→—]+")
_WHITESPACE_RUN = re.compile(r"\s+")
# The Next cell counts only when it is NOTHING BUT an ISO date — a free-form note
# ("Sep 14 phase") is not a schedulable review date.
_FULL_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# Matches the scheduleItem.endNote schema maxLength (dashboard/progress.schema.json) —
# the real vocabulary (s0/s1/s2/prov/dropped) never approaches this, so a cap is simpler
# than a truncation policy that never actually fires.
END_NOTE_MAX_LENGTH = 16


def _schedule_item_outcome(end_cell: str | None, next_cell: str | None) -> dict:
    """The per-rep outcome earned on a schedule row, for the board slice: `{endComfort,
    endNote, nextReview}` (all None for a glyph-less/blank row).

    endComfort: the first comfort glyph in the E cell — UNLIKE the comfort-timeline read
    (_scan_week), this never falls back to the Start glyph, so the board shows only what
    was actually earned this rep, never the start comfort carried forward as if earned.
    endNote: only set when endComfort is non-null — the E cell with that glyph removed, a
    leading arrow/dash/space run stripped, internal whitespace collapsed to one space,
    lowercased, and capped at END_NOTE_MAX_LENGTH chars. nextReview: the Next cell iff,
    once stripped, it is nothing but an ISO date.
    """
    end_comfort = _end_glyph(end_cell)
    end_note = None
    if end_comfort:
        remainder = (end_cell or "").replace(end_comfort, "", 1)
        remainder = _NOTE_LEADING_STRIP.sub("", remainder)
        remainder = _WHITESPACE_RUN.sub(" ", remainder).strip().lower()
        end_note = remainder[:END_NOTE_MAX_LENGTH] if remainder else None
    stripped_next = (next_cell or "").strip()
    next_review = stripped_next if _FULL_ISO_DATE.fullmatch(stripped_next) else None
    return {"endComfort": end_comfort, "endNote": end_note, "nextReview": next_review}


def _parse_schedule_day_full(
    path: Path, day: dt.date, difficulty_by_num: dict[int, str], urls: dict[int, str],
    files: dict[int, list[Path]] | None = None,
) -> tuple[list[dict], str | None, float | None]:
    """Like eb.parse_schedule_day, but keeps the day's label and each item's technique,
    tags, kind, a display-clean title, and the per-rep outcome (endComfort/endNote/
    nextReview, from _schedule_item_outcome) — eb's own version only needs the number,
    the start comfort, and whether a row is done, because that is all effort pricing ever
    reads.

    `difficulty_by_num` joins each item's intrinsic Easy/Medium/Hard from the TRACKER (the
    schedule file itself carries no difficulty column) — a number the tracker doesn't have
    yet honestly gets null rather than a guess. `urls` (from problem_urls()) is the
    fallback source for each item's canonical LeetCode URL — see _schedule_item_url,
    which prefers the row's own link first; the site's own AlgorithmMeta.id is a
    shortened route slug, not the LC slug, so it cannot build a correct link itself.
    `files` (from links.solution_files()) gives each item its `file` — the learner's own
    solution path (see solution_path) — null for a row with no number or no file yet.
    """
    wanted = (day.strftime("%a"), day.strftime("%b"), day.day)
    files = files or {}
    items: list[dict] = []
    label: str | None = None
    units: float | None = None
    inside = False
    for line in path.read_text(encoding="utf-8").splitlines():
        header = eb.DAY_HEADER.search(line)
        if header:
            hit = (header["wd"], header["mon"], int(header["day"])) == wanted
            if hit:
                inside = True
                units = float(header["units"]) if header["units"] else None
                lbl = DAY_LABEL.search(line)
                label = lbl["label"].strip() if lbl else None
            elif inside:
                break          # the next day's header ends this day's block
            continue
        if not inside:
            continue
        if not line.lstrip().startswith("|"):
            break              # the daily table ended (see eb.parse_schedule_day's note
                               # on why this guard matters for the LAST day of a week)
        m = eb.SCHED_ROW.match(line)
        if not m:
            continue
        cell = m["c1"]
        if not cell.strip() or set(cell.strip()) <= {"-", ":"}:
            continue           # blank separator row, or a markdown rule
        # text is computed before lcNumber because _schedule_item_lc_number's fallback
        # (a bare-number 🆕 row) reads off this same tag-stripped, link-unwrapped string.
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell)
        text = re.sub(r"~~|\*\*", "", text)
        lc_number = _schedule_item_lc_number(cell, text)
        start = eb.GLYPH.search(m["c2"] or "")
        technique = (m["c5"] or "").strip() or None
        tags = _leading_tags(cell)
        items.append({
            # lcNumber is honestly null only when NEITHER eb.SCHED_NUM nor the bare-number
            # fallback finds one (see _schedule_item_lc_number) — the dashboard then omits
            # that row's Visualize/LeetCode deep links.
            "lcNumber": lc_number,
            "title": _clean_schedule_title(text),
            "technique": technique,
            "startComfort": start.group(0) if start else None,
            "difficulty": difficulty_by_num.get(lc_number) if lc_number else None,
            "url": _schedule_item_url(cell, lc_number, urls),
            "file": solution_path(lc_number, files) if lc_number else None,
            "tags": tags,
            "kind": _schedule_item_kind(technique, tags),
            "done": "~~" in cell,
            **_schedule_item_outcome(m["c3"], m["c4"]),
        })
    return items, label, units


def parse_current_week_schedule(today: dt.date, urls: dict[int, str],
                                files: dict[int, list[Path]] | None = None) -> dict | None:
    """The CURRENT week's `## Daily Schedule` table -> {weekOf, days:[...]} — the compact
    slice behind the dashboard's Today's-board drill.

    Emits ALL 7 days; it never bakes a server-side "today" into the payload, because the
    summary is generated on commit but can be VIEWED days later — the client picks its
    own day by comparing its local date against each day's `date`. Fail-soft: no current
    schedule file -> None (the caller adds a warning). `urls` (from problem_urls()) and
    `files` (from links.solution_files()) are threaded through to each item — see
    _parse_schedule_day_full.
    """
    path = eb.find_schedule(today)
    if path is None:
        return None
    try:
        week_start = dt.date(int(path.name[:4]), int(path.name[4:6]), int(path.name[6:8]))
    except (ValueError, IndexError):
        return None

    # num -> Easy/Medium/Hard, joined from the tracker (the schedule file itself has no
    # difficulty column). A number with several tracker rows (method variants) just takes
    # the last one parse_rows() yields — difficulty is intrinsic to the LC problem, not the
    # method, so they should always agree in practice.
    try:
        difficulty_by_num = {int(r["num"]): r["diff"] for r in eb.parse_rows()}
    except OSError:
        difficulty_by_num = {}

    days: list[dict] = []
    for offset in range(7):
        day_date = week_start + dt.timedelta(days=offset)
        items, label, units = _parse_schedule_day_full(path, day_date, difficulty_by_num,
                                                       urls, files)
        days.append({
            "date": day_date.isoformat(),
            "weekday": day_date.strftime("%A"),
            "label": label,
            "units": units,
            "items": items,
        })
    return {"weekOf": week_start.isoformat(), "days": days}


# ── streak (SR-honest: showing up when due, with a rest-day allowance) ──────────────

def study_days(rows: list[dict]) -> list[dt.date]:
    seen: set[dt.date] = set()
    for r in rows:
        for d in eb._DATE.findall(r.get("reps") or ""):
            try:
                seen.add(dt.date.fromisoformat(d))
            except ValueError:
                continue
    return sorted(seen)


def compute_streak(days: list[dt.date], allowance: int, today: dt.date) -> dict:
    """Current + longest study-day streak.

    A streak counts DISTINCT days practiced; consecutive study days belong to the same
    run when at most `allowance` days were missed between them (the Duolingo streak-freeze
    idea — but chosen so it never pushes daily grinding against the effort budget, whose
    own rule is 'never raise the ceiling to catch up'). The current streak is live only
    if the last study day is itself within the allowance window of today.
    """
    if not days:
        return {"current": 0, "longest": 0, "lastStudyDay": None,
                "studyDays": 0, "restDayAllowance": allowance}
    gap = allowance + 1
    longest = run = 1
    for prev, cur in zip(days, days[1:]):
        run = run + 1 if (cur - prev).days <= gap else 1
        longest = max(longest, run)
    current = run if (today - days[-1]).days <= gap else 0
    return {"current": current, "longest": longest,
            "lastStudyDay": days[-1].isoformat(), "studyDays": len(days),
            "restDayAllowance": allowance}


# ── coverage header ─────────────────────────────────────────────────────────────────

COVERAGE_LINE = re.compile(
    r"\*\*(\d+)/(\d+)\*\*\s*techniques started.*?\*\*(\d+)\*\*\s*with no.*?"
    r"\*\*(\d+)\*\*\s*thin.*?\*\*(\d+)\*\*\s*unqueued variant", re.S)


def parse_coverage() -> dict | None:
    try:
        m = COVERAGE_LINE.search(COVERAGE.read_text(encoding="utf-8"))
    except OSError:
        return None
    if not m:
        return None
    started, total, no_green, thin, variant = (int(g) for g in m.groups())
    return {"total": total, "started": started, "noGreen": no_green,
            "thin": thin, "variantGaps": variant}


# ── per-technique table (the "which 56?" drill behind the coverage header) ──────────

COVERAGE_SECTION = re.compile(r"##\s*Coverage(.*?)(?:\n##\s|\Z)", re.S)
TABLE_ROW = re.compile(r"^\|(.+)\|\s*$", re.MULTILINE)
CELL_NUMBER = re.compile(r"\d+")
PARENTHETICAL = re.compile(r"\((.*?)\)")
COMFORT_GLYPH = re.compile(r"[🔴🟡🟢🎓🏆]")

# The `## Coverage` table's fixed schema: Technique, Family, Tier, Min, Problems, Best,
# 🟢, Variants, Gaps. Not a cse.config.yml value — it's technique_coverage.py's own output
# shape, not a tuned threshold.
COVERAGE_TABLE_COLUMNS = 9


def parse_techniques(warnings: list[str]) -> list[dict]:
    """The `## Coverage` per-technique table -> one dict per row.

    Reuses parse_coverage()'s file-read + regex style. The Problems cell carries both a
    count and a parenthetical of LC numbers, and can carry `*+Nv*` (extra untracked variant
    reps) or `—` (no problems yet) — handled by taking the FIRST integer in the cell as the
    count and only the integers INSIDE the parens as the problem list, so those extra tokens
    never get mistaken for a problem number. Fail-soft: an unreadable/missing table -> [].

    The HEADER row's own cell count is checked against COVERAGE_TABLE_COLUMNS before any
    row is parsed: an older technique_coverage.py emitting a different column count would
    otherwise have every row silently skipped by the per-row count check below, losing the
    whole table with no signal. That mismatch pushes one message onto `warnings` (mutated
    in place, like build_payload's own local list) and returns [] rather than a partial,
    possibly-misaligned table.

    `tier` (Sep 21, 2026) is technique_coverage.py's Tier column — "core" for every
    pre-tiering technique (the column simply never reads empty; technique_coverage.py's
    `Resolved.tier` defaults not-started-but-untiered entries to "core" too, though there
    are none). `started` is derived from the Gaps cell's `*not started*` marker rather than
    re-deriving it from problemCount, so it stays byte-for-byte in lockstep with
    `is_started` (the exact gate that keeps these techniques out of the Action list) even
    if that check's definition ever changes.

    `minProblems` (round 3) is the Min column — the per-technique coverage bar
    (`techniques.yml`'s `min_problems`, 1 for most, up to 5 for one) that makes "thin"
    self-explanatory as `problemCount / minProblems` instead of a bare, unexplained label.
    """
    try:
        text = COVERAGE.read_text(encoding="utf-8")
    except OSError:
        return []
    section = COVERAGE_SECTION.search(text)
    if not section:
        return []

    rows = TABLE_ROW.findall(section.group(1))
    if not rows:
        return []
    header_columns = len(rows[0].split("|"))
    if header_columns != COVERAGE_TABLE_COLUMNS:
        warnings.append(
            f"technique_coverage.md Coverage table has {header_columns} columns, "
            f"expected {COVERAGE_TABLE_COLUMNS} — regenerate it with "
            "scripts/technique_coverage.py; techniques omitted.")
        return []

    out: list[dict] = []
    for line in rows:
        cells = [c.strip() for c in line.split("|")]
        if len(cells) != COVERAGE_TABLE_COLUMNS:
            continue
        (name, family, tier, min_cell, problems_cell, best_cell, green_cell,
         _variants_cell, gaps_cell) = cells
        if name in ("Technique", "") or set(name) <= {"-", ":"}:
            continue  # header / markdown separator row, not data

        min_problems_match = CELL_NUMBER.search(min_cell)
        counts = CELL_NUMBER.findall(problems_cell)
        problem_count = int(counts[0]) if counts else 0
        paren = PARENTHETICAL.search(problems_cell)
        problems = [int(n) for n in CELL_NUMBER.findall(paren.group(1))] if paren else []
        best = COMFORT_GLYPH.search(best_cell)

        out.append({
            "name": name,
            "family": family,
            "tier": tier or "core",
            "started": "not started" not in gaps_cell,
            "minProblems": int(min_problems_match.group(0)) if min_problems_match else 3,
            "problemCount": problem_count,
            "problems": problems,
            "bestComfort": best.group(0) if best else None,
            "hasGreen": "✅" in green_cell,
            "thin": "thin" in gaps_cell,
            "hasVariantGap": "variant" in gaps_cell,
        })
    return out


# ── technique graph + graduation counts (builds_on / graduatedCount, Sep 26, 2026) ──

def load_technique_entries(warnings: list[str]) -> list[dict]:
    """techniques.yml's `techniques:` list, verbatim (each entry's `name` + `builds_on`
    among other keys `parse_techniques()` doesn't carry). Fail-soft to [] with a warning —
    same style as load_config(): a missing file or missing PyYAML degrades gracefully
    rather than raising out of the hook."""
    try:
        import yaml  # noqa: PLC0415
        config = yaml.safe_load(TECHNIQUES_YML.read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001 — a missing/unparsable file is a normal fail-soft state
        warnings.append(
            "techniques.yml not readable — buildsOn omitted for every technique.")
        return []
    return config.get("techniques") or []


def _resolve_builds_on(name: str, raw_by_name: dict[str, list[str]],
                       known_names: set[str], warnings: list[str]) -> list[str]:
    """One technique's raw `builds_on` list -> the edges that survive validation: an
    unknown name or a self-edge is dropped, each with one warning naming the offender.
    Cycle-breaking is a separate pass (`_break_cycles`) — it needs the whole graph, not
    one row at a time."""
    resolved = []
    for dep in raw_by_name.get(name) or []:
        if dep == name:
            warnings.append(f"techniques.yml: {name!r} lists itself in builds_on — dropped.")
            continue
        if dep not in known_names:
            warnings.append(
                f"techniques.yml: {name!r} builds_on unknown technique {dep!r} — dropped.")
            continue
        resolved.append(dep)
    return resolved


def _break_cycles(graph: dict[str, list[str]], order: list[str],
                  warnings: list[str]) -> dict[str, list[str]]:
    """DFS over `graph` in `order` (techniques.yml's own file order, so this is
    deterministic run to run). A back edge to a node still GRAY (on the current DFS
    stack) closes a cycle; only that one edge is dropped, with a warning naming it — the
    rest of both nodes' builds_on survives. Returns a NEW graph (pure, no mutation of the
    input dict's lists)."""
    cleaned = {name: list(deps) for name, deps in graph.items()}
    white, gray, black = 0, 1, 2
    color = {name: white for name in graph}

    def visit(name: str) -> None:
        color[name] = gray
        for dep in list(cleaned.get(name, [])):
            if color.get(dep) == gray:
                cleaned[name].remove(dep)
                warnings.append(
                    f"techniques.yml: builds_on cycle through {name!r} -> {dep!r} — "
                    "that edge dropped.")
            elif color.get(dep) == white:
                visit(dep)
        color[name] = black

    for name in order:
        if color.get(name) == white:
            visit(name)
    return cleaned


def _comfort_by_number(problems: list[dict], retired: list[dict]) -> dict[int, str]:
    """LC number -> its best (highest LEVEL) comfort glyph, from data build_payload already
    parsed once — never a second read of the tracker. A number can carry several tracker
    rows (21 Recursion vs Iterative), so the highest LEVEL among them wins. Retired
    problems left the 7-column table (parse_retired()'s own docstring — parse_rows() never
    sees them), so they never appear in `problems`; each is 🏆, terminal above 🎓.

    Fail-soft like build_problems() itself (LEVEL.get(r["comfort"]), never LEVEL[...]): a
    tracker comfort cell outside LEVEL's five glyphs is never stored — its UNTRACKED_LEVEL
    can't outrank a real glyph already recorded, and if it's the only row for that number,
    UNTRACKED_LEVEL == UNTRACKED_LEVEL so nothing is written at all. `build_payload` must
    never raise on a malformed cell."""
    best: dict[int, str] = {}
    for p in problems:
        num, glyph = p["lcNumber"], p["comfort"]
        if LEVEL.get(glyph, UNTRACKED_LEVEL) > LEVEL.get(best.get(num), UNTRACKED_LEVEL):
            best[num] = glyph
    for r in retired:
        num = r["lcNumber"]
        if LEVEL["🏆"] > LEVEL.get(best.get(num), UNTRACKED_LEVEL):
            best[num] = "🏆"
    return best


def enrich_techniques(rows: list[dict], yaml_entries: list[dict],
                      comfort_by_number: dict[int, str],
                      warnings: list[str]) -> list[dict]:
    """`parse_techniques()`'s rows -> new dicts (no mutation) adding `buildsOn` and
    `graduatedCount`.

    `buildsOn` is techniques.yml's own `builds_on` for that row's name, validated (an
    unknown name or a self-edge dropped, each warned) and cycle-broken (one back edge
    dropped per cycle, warned) against the same file's declared names — never against
    `rows`, since a coverage-table name with no matching YAML entry gets `[]` rather than
    silently reusing a stale graph.

    `graduatedCount` counts the row's `problems` (LC numbers) whose tracker comfort has
    reached GRADUATED_LEVEL (🎓) or better, read from `comfort_by_number` — data
    build_payload already holds, never a second read of the tracker.
    """
    known_names = {e["name"] for e in yaml_entries if e.get("name")}
    order = [e["name"] for e in yaml_entries if e.get("name")]
    raw_by_name = {e["name"]: e.get("builds_on") or []
                   for e in yaml_entries if e.get("name")}
    graph = {name: _resolve_builds_on(name, raw_by_name, known_names, warnings)
             for name in order}
    graph = _break_cycles(graph, order, warnings)

    enriched = []
    for row in rows:
        graduated = sum(
            1 for num in row["problems"]
            if LEVEL.get(comfort_by_number.get(num), UNTRACKED_LEVEL) >= GRADUATED_LEVEL)
        enriched.append({**row,
                         "buildsOn": graph.get(row["name"], []),
                         "graduatedCount": graduated})
    return enriched


# ── recognition probes (the "is the pool still teaching?" diagnostic) ───────────────

PROBE_SECTION = re.compile(r"##\s*📒\s*Probe log(.*?)(?:\n##\s|\Z)", re.S)
PROBE_PROBLEM = re.compile(r"^(\d+)\s+(.+)$")


def parse_probes(urls: dict[int, str]) -> dict | None:
    """The `dsa/probes/README.md` Probe log table -> {total, cleanRate, items:[...]}.

    Reuses TABLE_ROW/COMFORT_GLYPH (parse_techniques()'s style). Each probe is a cold,
    label-stripped, disposable rep — a clean 🟢 creates no tracker row (see the README's
    own docstring), so the tracker's own numbers never see it; this table is the ONLY
    place it's counted. `result` takes the FIRST comfort glyph in the Result cell — a row
    that later converted (`🔴 → 🟡 (re-rep Sep 16)`) is scored on what the COLD call
    actually was, not its eventual outcome. `urls` (from problem_urls()) joins each item's
    canonical LeetCode URL — see problem_urls()'s docstring for why the site can't derive
    this itself.

    Fail-soft, but the TWO empty cases mean different things and must not collapse to the
    same result: a missing file or a missing `## 📒 Probe log` section is something wrong
    (-> None, and main() warns) — but a fresh adopter checkout has the file and the
    section with a header row and NO data rows yet, which is not wrong at all, just day
    one (-> the zero payload below, no warning). Warning on day one would be the first
    thing a new user sees from an otherwise-honest tool.
    """
    try:
        text = PROBES_README.read_text(encoding="utf-8")
    except OSError:
        return None
    section = PROBE_SECTION.search(text)
    if not section:
        return None

    items: list[dict] = []
    for line in TABLE_ROW.findall(section.group(1)):
        cells = [c.strip() for c in line.split("|")]
        if len(cells) != 6:
            continue
        num, date, problem_cell, technique, result_cell, _tracker_row = cells
        if num in ("#", "") or set(num) <= {"-", ":"}:
            continue  # header / markdown separator row, not data

        m = PROBE_PROBLEM.match(problem_cell)
        glyph = COMFORT_GLYPH.search(result_cell)
        lc_number = int(m.group(1)) if m else None
        items.append({
            "date": date,
            "lcNumber": lc_number,
            "title": m.group(2).strip() if m else problem_cell,
            "technique": technique,
            "result": glyph.group(0) if glyph else None,
            "url": urls.get(lc_number) if lc_number else None,
        })

    if not items:
        # File and section both present; the table just has no data rows yet (a fresh
        # adopter checkout). That's not an error — see the docstring — so it gets the
        # zero payload, not None (which main() would report as a warning).
        return {"total": 0, "cleanRate": 0.0, "items": []}
    total = len(items)
    clean = sum(1 for it in items if it["result"] == "🟢")
    return {"total": total, "cleanRate": clean / total, "items": items}


# ── the build ───────────────────────────────────────────────────────────────────────

def solution_path(num: int, files: dict[int, list[Path]],
                  warnings: list[str] | None = None) -> str | None:
    """Repo-relative POSIX path of `num`'s solution file (from links.solution_files()),
    or None when no file exists under the configured roots. A PATH, never code —
    progress.json stays code-free (decisions.yml `showcase-contract`); the site turns it
    into a `blob/<branch>/<path>` link so every row can point at the learner's own file
    even before any curated showcase entry exists.

    A twin (two files for one number, e.g. 1216) takes the first sorted path — the same
    rule as `links.find_file` — and records one warning per number so the choice is never
    silent. The map lookup is O(1); the glob ran once, in build_payload."""
    paths = files.get(num) or []
    if not paths:
        return None
    if len(paths) > 1 and warnings is not None:
        joined = ", ".join(p.relative_to(REPO).as_posix() for p in paths)
        warnings.append(f"{num}: {len(paths)} solution files ({joined}) — `file` uses the first.")
    return paths[0].relative_to(REPO).as_posix()


def build_problems(rows: list[dict], sched: dict[str, dict[int, str]],
                   cats: dict[int, str], urls: dict[int, str],
                   files: dict[int, list[Path]] | None = None,
                   warnings: list[str] | None = None) -> list[dict]:
    # The schedule index is keyed by problem NUMBER, but a number can carry several rows
    # (different methods — 21 Recursion vs Iterative, 323 with three variants). The index
    # cannot say which variant a rep belonged to, so attaching its glyph to every row would
    # FABRICATE a timeline — the exact thing the docstring promises never to do. For a
    # multi-row number we degrade the reconstructed comfort to activity dots (null); only
    # the final point is anchored to each row's own authoritative current comfort.
    multi = {n for n, c in _count_nums(rows).items() if c > 1}
    files = files or {}
    # One twin warning per NUMBER, not per row: a multi-variant number (21 Recursion vs
    # Iterative) has several tracker rows but only one file lookup worth reporting.
    twin_warned: set[int] = set()
    problems = []
    for r in rows:
        num = int(r["num"])
        file_rel = solution_path(num, files, None if num in twin_warned else warnings)
        twin_warned.add(num)
        rep_dates = eb._DATE.findall(r.get("reps") or "")
        timeline = []
        for d in rep_dates:
            glyph = None if num in multi else sched.get(d, {}).get(num)
            timeline.append({"date": d, "comfort": glyph,
                             "level": LEVEL.get(glyph) if glyph else None})
        # The final point is anchored to the tracker's authoritative current comfort,
        # even when that rep's schedule row could not be read.
        if timeline and timeline[-1]["comfort"] is None:
            timeline[-1] = {"date": timeline[-1]["date"], "comfort": r["comfort"],
                            "level": LEVEL.get(r["comfort"])}
        problems.append({
            "lcNumber": num,
            "title": r["title"].strip(),
            "url": urls.get(num),
            "file": file_rel,
            "difficulty": r["diff"],
            "category": cats.get(num),
            "comfort": r["comfort"],
            "level": LEVEL.get(r["comfort"]),
            "streak": r["streak"],
            "nextReview": r["due"],
            "repDates": rep_dates,
            "timeline": timeline,
        })
    return problems


def _count_nums(rows: list[dict]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for r in rows:
        counts[int(r["num"])] = counts.get(int(r["num"]), 0) + 1
    return counts


def pipeline(rows: list[dict], retired: list[dict]) -> dict:
    by = {"🔴": 0, "🟡": 0, "🟢": 0, "🎓": 0}
    green = {"s0": 0, "s1": 0, "s2plus": 0}
    for r in rows:
        by[r["comfort"]] = by.get(r["comfort"], 0) + 1
        if r["comfort"] == "🟢":
            key = "s0" if r["streak"] == 0 else "s1" if r["streak"] == 1 else "s2plus"
            green[key] += 1
    return {"blank": by["🔴"], "shaky": by["🟡"],
            "clean": {**green, "total": by["🟢"]},
            "graduated": by["🎓"], "retired": len(retired)}


def difficulty_mix(rows: list[dict]) -> dict:
    mix = {"Easy": 0, "Medium": 0, "Hard": 0}
    for r in rows:
        mix[r["diff"]] = mix.get(r["diff"], 0) + 1
    return mix


def on_schedule(rows: list[dict], today: dt.date) -> dict:
    overdue = due = 0
    for r in rows:
        try:
            nxt = dt.date.fromisoformat(r["due"])
        except ValueError:
            continue
        if nxt < today:
            overdue += 1
        elif nxt == today:
            due += 1
    return {"totalActive": len(rows), "dueToday": due, "overdue": overdue}


def _had_turnaround(problems: list[dict]) -> bool:
    """Any problem whose timeline went 🔴 ... then later 🟢/🎓 — an earned comeback."""
    for p in problems:
        seen_blank = False
        for pt in p["timeline"]:
            if pt["comfort"] == "🔴":
                seen_blank = True
            elif seen_blank and pt["comfort"] in ("🟢", "🎓"):
                return True
    return False


def compute_badges(stats: dict, problems: list[dict], cfg: dict) -> list[dict]:
    """The badge CATALOG. Every trigger keys off a genuine, unfakeable event —
    a graduation (3 cold cleans across spaced intervals), a retirement, a comeback,
    a study-day streak — never a raw count of easy greens and never a rating.

    A counter badge (streak-N, trophies-N, all-green) MAY carry an additive
    `progress: {current, target}` alongside `earned` — how far toward the target,
    even when not yet earned. A one-shot event badge (first-clean, first-hard-clean,
    first-graduate, first-retire, comeback) never carries it: there is no "current/
    target" for an event that either happened or hasn't."""
    pl = stats["pipeline"]
    trophies = pl["graduated"] + pl["retired"]
    hard_clean = any(p["difficulty"] == "Hard" and p["comfort"] in ("🟢", "🎓")
                     for p in problems)
    techs = stats.get("techniques") or []
    green = sum(1 for t in techs if t.get("hasGreen"))
    cov = stats.get("coverage") or {}
    all_green_target = cov.get("total") or len(techs)

    badges: list[dict] = []

    def add(bid: str, title: str, icon: str, desc: str, earned: bool,
            progress: tuple[int, int] | None = None) -> None:
        badge = {"id": bid, "title": title, "icon": icon,
                 "description": desc, "earned": bool(earned)}
        if progress is not None:
            current, target = progress
            badge = {**badge, "progress": {"current": int(current), "target": int(target)}}
        badges.append(badge)

    add("first-clean", "First Cold Solve", "🟢",
        "Solve one problem clean from a blank page.",
        pl["clean"]["total"] + pl["graduated"] > 0)
    add("first-hard-clean", "Hard Mode", "⛰️",
        "Solve a Hard problem clean, cold.", hard_clean)
    add("first-graduate", "First Graduation", "🎓",
        "Graduate a problem — three cold cleans across spaced reviews.",
        pl["graduated"] >= 1)
    add("first-retire", "Retired It", "🏆",
        "Retire a problem — it cleared its spot checks and left rotation for good.",
        pl["retired"] >= 1)
    add("comeback", "Comeback", "🔁",
        "Turn a Blank into a Clean on the same problem.", _had_turnaround(problems))
    add("all-green", "Full Spectrum", "🌈",
        "Have at least one clean solve in every technique on the roadmap.",
        all_green_target > 0 and green >= all_green_target,
        progress=(green, all_green_target))

    for m in sorted(cfg.get("streak_milestones") or []):
        add(f"streak-{m}", f"{m}-Day Streak", "🔥",
            f"Practice on {m} study-days without letting the streak lapse.",
            stats["streak"]["longest"] >= m,
            progress=(stats["streak"]["longest"], m))
    for m in sorted(cfg.get("trophy_milestones") or []):
        add(f"trophies-{m}", f"{m} Mastered", "💎",
            f"Reach {m} problem{'s' if m != 1 else ''} graduated or retired.",
            trophies >= m, progress=(trophies, m))

    return badges


def build_payload(today: dt.date | None = None) -> tuple[dict, list[str]]:
    """Return (payload, warnings). Never raises for a missing/partial input."""
    today = today or dt.date.today()
    warnings: list[str] = []
    cfg, fell_back = load_config()
    if fell_back:
        warnings.append("cse.config.yml had no `gamification:` block (or PyYAML is "
                        "missing) — used DEFAULT_CONFIG thresholds.")

    try:
        rows = eb.parse_rows()
    except OSError as exc:
        warnings.append(f"could not read the tracker ({exc}); emitting an empty payload.")
        rows = []

    retired = parse_retired()
    cats = category_map()
    urls = problem_urls()
    files = links.solution_files()   # one glob; every row and board item reads this map
    sched = build_schedule_index()
    coverage = parse_coverage()
    if coverage is None:
        warnings.append("technique_coverage.md not readable — coverage omitted.")
    techniques = parse_techniques(warnings)
    schedule = parse_current_week_schedule(today, urls, files)
    if schedule is None:
        warnings.append("no current weekly schedule file found — schedule omitted.")
    probes = parse_probes(urls)
    if probes is None:
        warnings.append("dsa/probes/README.md Probe log not readable — probes omitted.")

    # Today's-board workload bar (Sep 21, 2026): reuse effort_budget.py's OWN config
    # reader rather than re-deriving the fallback here — it already tolerates a missing
    # `effort_budget:` block / PyYAML and returns its documented defaults for
    # `effort_budget.ceiling` / `effort_budget.floor_min` (cse.config.yml), which is the
    # single source of truth for these two numbers.
    effort_cfg = eb.load_config()

    problems = build_problems(rows, sched, cats, urls, files, warnings)
    days = study_days(rows)

    # buildsOn/graduatedCount (Sep 26, 2026): computed after build_problems() rather than
    # right after parse_techniques() because graduatedCount needs comfort_by_number, which
    # is built from build_problems()'s own output — never a second read of the tracker.
    yaml_entries = load_technique_entries(warnings)
    comfort_by_number = _comfort_by_number(problems, retired)
    techniques = enrich_techniques(techniques, yaml_entries, comfort_by_number, warnings)

    stats = {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": today.isoformat(),
        "totals": {
            "problems": len({p["lcNumber"] for p in problems}),
            "solutions": len(problems),
            "reps": sum(len(p["repDates"]) for p in problems),
        },
        "pipeline": pipeline(rows, retired),
        "difficulty": difficulty_mix(rows),
        "streak": compute_streak(days, int(cfg["streak_rest_day_allowance"]), today),
        "coverage": coverage,
        "onSchedule": on_schedule(rows, today),
        "trophyCase": {"graduated": [p for p in problems if p["comfort"] == "🎓"],
                       "retired": retired},
        "techniques": techniques,
        "studyDays": [d.isoformat() for d in days],
        "schedule": schedule,
        "workload": build_workload(rows, effort_cfg),
        "effortCeiling": float(effort_cfg["ceiling"]),
        "effortFloor": float(effort_cfg["floor_min"]),
        "probes": probes,
    }
    stats["badges"] = compute_badges(stats, problems, cfg)
    stats["problems"] = problems
    if warnings:
        stats["warnings"] = warnings
    return stats, warnings


def summary_of(payload: dict) -> dict:
    """Derive the lightweight landing contract from the full payload.

    Same aggregates, NO `problems[]` (the 144 KB heavy part) and a COMPACT `trophyCase`:
    graduated entries drop to `{lcNumber, title, difficulty}` (no timeline/repDates —
    the per-problem detail the landing never needs). `retired` entries are already
    compact in the full payload, so they pass through unchanged.

    `techniques` rides along whole (already small — a few KB for ~56 rows) and backs the
    technique-breadth drill. `studyDays` rides along CAPPED to the last
    SUMMARY_STUDY_DAYS_WINDOW days — that's all the streak-calendar drill renders, and
    without a cap this list grows by one entry per practice day forever. The lifetime total
    is untouched: it lives in `streak.studyDays` (count) and `streak.longest`, both copied
    through as-is. The full `progress.json` keeps every study day, uncapped.

    `schedule` (the current week's Today's-board slice) rides through whole too — it is
    one week of compact rows, small either way, and the summary is exactly where the
    landing's Today's-board drill reads it from (no separate fetch for "what do I do
    today"). `effortCeiling`/`effortFloor` (two numbers) back the workload bar's
    Light/Moderate/Heavy band next to it.

    `probes` (round 3) rides through whole too — the Probe log is ~1 row/week, small
    either way, and it's the ONLY place a disposable, cold recognition probe is counted
    (see parse_probes()'s docstring), so the Recognition tab needs it with no extra fetch.

    `workload` (planned vs completed effort units per scheduled day) rides through
    CAPPED to the same rolling window as `studyDays` — the workload chart is a recent
    view, not a lifetime one, and an uncapped list grows by one entry per scheduled day
    forever. The full `progress.json` keeps every scheduled day, uncapped.
    """
    trophy_case = payload.get("trophyCase") or {}
    compact_graduated = [
        {"lcNumber": p["lcNumber"], "title": p["title"], "difficulty": p.get("difficulty")}
        for p in trophy_case.get("graduated") or []
    ]
    generated_at = dt.date.fromisoformat(payload["generatedAt"])
    cutoff = (generated_at - dt.timedelta(days=SUMMARY_STUDY_DAYS_WINDOW)).isoformat()
    recent_study_days = [d for d in (payload.get("studyDays") or []) if d >= cutoff]
    summary = {
        "schemaVersion": payload["schemaVersion"],
        "generatedAt": payload["generatedAt"],
        "totals": payload["totals"],
        "pipeline": payload["pipeline"],
        "difficulty": payload["difficulty"],
        "streak": payload["streak"],
        "coverage": payload["coverage"],
        "onSchedule": payload["onSchedule"],
        "badges": payload["badges"],
        "trophyCase": {"graduated": compact_graduated,
                       "retired": trophy_case.get("retired") or []},
        "techniques": payload.get("techniques") or [],
        "studyDays": recent_study_days,
        "schedule": payload.get("schedule"),
        "workload": [w for w in payload.get("workload") or [] if w["date"] >= cutoff],
        "effortCeiling": payload.get("effortCeiling"),
        "effortFloor": payload.get("effortFloor"),
        "probes": payload.get("probes"),
    }
    if "warnings" in payload:
        summary["warnings"] = payload["warnings"]
    return summary


# ── outputs ─────────────────────────────────────────────────────────────────────────

def render_banner(stats: dict) -> str:
    s = stats["streak"]
    pl = stats["pipeline"]
    trophies = pl["graduated"] + pl["retired"]
    flame = f"🔥 {s['current']}-day streak" if s["current"] else "no active streak"
    return f"{flame} · {trophies} mastered (🎓{pl['graduated']} 🏆{pl['retired']}) · " \
           f"{stats['totals']['reps']} reps — dashboard: {SITE}/progress"


def badge_line(stats: dict, owner_repo: str | None) -> str:
    s = stats["streak"]
    pl = stats["pipeline"]
    cov = stats.get("coverage") or {}
    parts = [f"🔥 {s['current']}-day streak",
             f"🎓 {pl['graduated']} graduated",
             f"🏆 {pl['retired']} retired"]
    if cov:
        parts.append(f"{cov['started']}/{cov['total']} techniques")
    href = f"{SITE}/progress"
    if owner_repo:
        href += f"?repo={owner_repo}"
    return f"[![progress]({href}) {' · '.join(parts)}]({href})"


def update_readme_badge(line: str) -> bool:
    """Insert/replace the progress badge between marker comments in README.md.

    Returns True if README changed. No markers and no README -> no-op (never
    invents a README or clobbers content).
    """
    start, end = "<!-- progress-badge:start -->", "<!-- progress-badge:end -->"
    block = f"{start}\n{line}\n{end}"
    try:
        text = README.read_text(encoding="utf-8")
    except OSError:
        return False
    if start in text and end in text:
        new = re.sub(re.escape(start) + r".*?" + re.escape(end), block, text, flags=re.S)
    else:
        return False  # markers absent — leave README alone; opt-in by adding markers
    if new != text:
        README.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--banner", action="store_true",
                    help="print one honest line for the SessionStart hook, then exit")
    ap.add_argument("--validate", action="store_true",
                    help="compute + report; write nothing (for tests / CI)")
    ap.add_argument("--stdout", action="store_true", help="print the JSON, do not write")
    ap.add_argument("--repo", metavar="OWNER/NAME",
                    help="owner/name for the badge deep-link (default: none)")
    # --date (not --today) so it matches the flag session_date.resolve_datetime tells the
    # user to pass when it announces a guess ("Override with --date if that's wrong") —
    # --today is kept as a hidden alias so any existing caller of the old name still works.
    ap.add_argument("--date", dest="date", metavar="YYYY-MM-DD",
                    help="override the resolved session date (YYYY-MM-DD or YYYYMMDD)")
    ap.add_argument("--today", dest="date", help=argparse.SUPPRESS)
    args = ap.parse_args()

    # session_date.resolve_datetime announces its heuristic guess with a bare print() —
    # stdout, the same stream --stdout/--banner use for their own payload. Redirected to
    # stderr here so the announcement stays visible (CLAUDE.md's fallback-must-announce
    # rule) without corrupting --stdout's JSON or adding a line to --banner's one line.
    with contextlib.redirect_stdout(sys.stderr):
        today = session_date.resolve_datetime(args.date).date()
    stats, warnings = build_payload(today)

    if args.banner:
        print(render_banner(stats))
        return

    payload = json.dumps(stats, ensure_ascii=False, indent=2)

    if args.stdout:
        print(payload)
    elif args.validate:
        print(f"valid: {stats['totals']['reps']} reps · "
              f"{len(stats['problems'])} problems · {len(stats['badges'])} badges · "
              f"{stats['streak']['current']}-day streak", file=sys.stderr)
    else:
        DASHBOARD.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload + "\n", encoding="utf-8")
        # Compact (no indent), unlike progress.json: nobody reads progress-summary.json as a
        # human artifact, and it's fetched on every landing view — indentation alone was ~40%
        # of its bytes once techniques[]/studyDays[] joined the summary (Sep 2026).
        summary_payload = json.dumps(summary_of(stats), ensure_ascii=False, separators=(",", ":"))
        OUT_SUMMARY.write_text(summary_payload + "\n", encoding="utf-8")
        changed = update_readme_badge(badge_line(stats, args.repo))
        print(f"wrote {OUT.relative_to(REPO)} + {OUT_SUMMARY.relative_to(REPO)} "
              f"({stats['totals']['reps']} reps, "
              f"{stats['pipeline']['graduated']}🎓 {stats['pipeline']['retired']}🏆, "
              f"{stats['streak']['current']}-day streak)"
              + (" · README badge updated" if changed else ""))

    # Warnings go to stderr so --stdout / --validate keep a clean JSON stdout.
    for w in warnings:
        print(f"  !! {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
