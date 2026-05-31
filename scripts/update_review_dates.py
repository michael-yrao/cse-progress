from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path

MARKDOWN_PATH = Path("docs/review_progresion.md")
TABLE_HEADER = "| Difficulty | Problem | Mastered | Next Review Date | Latest Attempt Date | Attempt Dates |"
ROW_SEPARATOR = "|---|---|---|---|---|---|"

ROW_RE = re.compile(
    r"^\| (?P<difficulty>[^|]+) \| \[(?P<problem>[^\]]+)\]\((?P<url>[^)]+)\) \| (?P<mastered>[YN]) \| (?P<next>[^|]*) \| (?P<latest>[^|]*) \| (?P<attempts>.*) \|$"
)


def parse_date(value: str) -> datetime | None:
    value = value.strip()
    if not value or value == "Not Attempted":
        return None
    return datetime.strptime(value, "%Y-%m-%d")


def format_date(date: datetime | None) -> str:
    return date.strftime("%Y-%m-%d") if date else ""


def compute_next_review_date(mastered: str, latest_attempt_date: datetime | None) -> datetime | None:
    if not latest_attempt_date:
        return None
    delta = timedelta(days=30 if mastered == "Y" else 2)
    return latest_attempt_date + delta


def build_row(entry: dict) -> str:
    return (
        f"| {entry['difficulty']} | [{entry['problem']}]({entry['url']})"
        f" | {entry['mastered']} | {entry['next_review']} | {entry['latest_attempt_date']} | {entry['attempts']} |"
    )


def main() -> None:
    text = MARKDOWN_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    prefix_lines: list[str] = []
    table_rows: list[dict] = []
    suffix_lines: list[str] = []
    in_table = False
    table_header_seen = False
    table_separator_seen = False

    for line in lines:
        if not in_table:
            prefix_lines.append(line)
            if line.strip() == TABLE_HEADER:
                in_table = True
                table_header_seen = True
            continue

        if in_table and not table_separator_seen:
            if line.strip() == ROW_SEPARATOR:
                prefix_lines.append(line)
                table_separator_seen = True
                continue
            # malformed file, keep going and preserve
            prefix_lines.append(line)
            continue

        # parse row lines after header and separator
        if line.startswith("|") and ROW_RE.match(line):
            match = ROW_RE.match(line)
            assert match is not None
            difficulty = match.group("difficulty").strip()
            problem = match.group("problem").strip()
            url = match.group("url").strip()
            mastered = match.group("mastered").strip()
            latest = parse_date(match.group("latest"))
            attempts = match.group("attempts").strip()
            next_review = format_date(compute_next_review_date(mastered, latest))
            table_rows.append({
                "difficulty": difficulty,
                "problem": problem,
                "url": url,
                "mastered": mastered,
                "latest": latest,
                "latest_attempt_date": format_date(latest),
                "attempts": attempts,
                "next_review": next_review,
            })
            continue

        suffix_lines.append(line)

    if not table_header_seen or not table_separator_seen:
        raise RuntimeError("Could not find review table header and separator in markdown file.")

    sorted_rows = sorted(
        table_rows,
        key=lambda entry: (entry["latest"] is not None, entry["latest"]),
        reverse=True,
    )

    sorted_lines = [build_row(entry) for entry in sorted_rows]
    new_lines = prefix_lines + sorted_lines + suffix_lines
    if new_lines != lines:
        MARKDOWN_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print(f"Reordered {len(sorted_rows)} rows by latest attempt date in {MARKDOWN_PATH}")
    else:
        print(f"No reorder needed in {MARKDOWN_PATH}")


if __name__ == "__main__":
    main()
