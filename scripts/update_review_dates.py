from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path

MARKDOWN_PATH = Path("docs/review_progresion.md")
TABLE_HEADER = "| Difficulty | Problem | Mastered | Next Review Date | Latest Attempt Date | Attempt Dates |"

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


def main() -> None:
    text = MARKDOWN_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    new_lines: list[str] = []
    updated_rows = 0
    found_table = False

    for line in lines:
        if not found_table and line.strip() == TABLE_HEADER:
            found_table = True
            new_lines.append(line)
            continue

        if found_table and line.startswith("|"):
            match = ROW_RE.match(line)
            if match:
                mastered = match.group("mastered").strip()
                latest = parse_date(match.group("latest"))
                computed = compute_next_review_date(mastered, latest)
                next_review = format_date(computed)
                current_next = match.group("next").strip()
                if current_next != next_review:
                    updated_rows += 1
                    row = (
                        f"| {match.group('difficulty').strip()} | [{match.group('problem')}]({match.group('url')})"
                        f" | {mastered} | {next_review} | {match.group('latest').strip()} | {match.group('attempts').strip()} |"
                    )
                    new_lines.append(row)
                    continue
        new_lines.append(line)

    if updated_rows > 0:
        MARKDOWN_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print(f"Updated {updated_rows} row(s) in {MARKDOWN_PATH}")
    else:
        print(f"No updates needed in {MARKDOWN_PATH}")


if __name__ == "__main__":
    main()
