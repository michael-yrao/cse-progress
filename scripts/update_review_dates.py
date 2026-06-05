from __future__ import annotations

import argparse
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

MARKDOWN_PATH = Path("docs/review_progresion.md")
SOURCE_ROOT = Path("data_structure_algorithms/2026_leetcode")
TABLE_HEADER = "| Difficulty | Problem | Mastered | Next Review Date | Latest Attempt Date | Attempt Dates |"
ROW_SEPARATOR = "|---|---|---|---|---|---|"

ROW_RE = re.compile(
    r"^\| (?P<difficulty>[^|]+) \| \[(?P<problem>[^\]]+)\]\((?P<url>[^)]+)\) \| (?P<mastered>[YN]) \| (?P<next>[^|]*) \| (?P<latest>[^|]*) \| (?P<attempts>.*) \|$"
)
SOURCE_FILE_RE = re.compile(r"^(?P<number>\d+)_(?P<name>.+)\.py$")
ROMAN_NUMERALS = {
    "i",
    "ii",
    "iii",
    "iv",
    "v",
    "vi",
    "vii",
    "viii",
    "ix",
    "x",
    "xi",
    "xii",
    "xiii",
    "xiv",
    "xv",
    "xvi",
    "xvii",
    "xviii",
    "xix",
    "xx",
}


def parse_date(value: str) -> datetime | None:
    value = value.strip()
    if not value or value == "Not Attempted":
        return None
    return datetime.strptime(value, "%Y-%m-%d")


def format_date(date: datetime | None) -> str:
    return date.strftime("%Y-%m-%d") if date else ""


def parse_latest_attempt_date_from_attempts(attempts: str) -> datetime | None:
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", attempts)
    parsed_dates = []
    for date_text in dates:
        try:
            parsed_dates.append(datetime.strptime(date_text, "%Y-%m-%d"))
        except ValueError:
            continue
    return max(parsed_dates) if parsed_dates else None


def extract_problem_number(problem_title: str) -> int | None:
    match = re.match(r"^(?P<number>\d+)\.", problem_title)
    if not match:
        return None
    return int(match.group("number"))


def compute_next_review_date(mastered: str, latest_attempt_date: datetime | None) -> datetime | None:
    if not latest_attempt_date:
        return None
    delta = timedelta(days=30 if mastered == "Y" else 2)
    return latest_attempt_date + delta


def count_attempt_dates(attempts: str) -> int:
    return len([part for part in attempts.split(",") if part.strip()])


def build_summary_lines(table_rows: list[dict]) -> list[str]:
    problems_done = sum(1 for row in table_rows if row["latest"] is not None)
    total_attempts = sum(count_attempt_dates(row["attempts"]) for row in table_rows)
    return [
        f"**Problems Done:** {problems_done}",
        f"**Total Successful Attempts:** {total_attempts}",
        "",
    ]


def humanize_raw_name(raw_name: str) -> str:
    tokens = raw_name.split("_")
    normalized_tokens: list[str] = []
    for token in tokens:
        lower = token.lower()
        if lower in ROMAN_NUMERALS:
            normalized_tokens.append(lower.upper())
        else:
            normalized_tokens.append(token.capitalize())
    return " ".join(normalized_tokens)


def build_row(entry: dict) -> str:
    return (
        f"| {entry['difficulty']} | [{entry['problem']}]({entry['url']})"
        f" | {entry['mastered']} | {entry['next_review']} | {entry['latest_attempt_date']} | {entry['attempts']} |"
    )


def extract_difficulty_from_source(path: Path) -> str | None:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return None

    # First attempt: parse top-level triple-quoted docstring/header
    top_doc = re.match(r"^\s*(['\"]{3})(.*?)(\1)", content, re.DOTALL)
    if top_doc:
        body = top_doc.group(2).strip().splitlines()
        for line in body:
            candidate = line.strip()
            if not candidate:
                continue
            normalized = candidate.lower()
            if normalized in {"easy", "medium", "hard"}:
                return candidate.capitalize()
            if any(word in normalized for word in ["easy", "medium", "hard"]):
                for token in normalized.split():
                    if token in {"easy", "medium", "hard"}:
                        return token.capitalize()
            break

    # Fallback: search first several lines for an explicit difficulty comment
    for line in content.splitlines()[:20]:
        candidate = line.strip().lower()
        if candidate.startswith("#"):
            candidate = candidate[1:].strip()
        if candidate in {"easy", "medium", "hard"}:
            return candidate.capitalize()
        if "difficulty" in candidate:
            for token in candidate.split():
                if token in {"easy", "medium", "hard"}:
                    return token.capitalize()
    return None


def get_staged_paths() -> tuple[list[Path], bool]:
    try:
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            text=True,
            cwd=Path.cwd(),
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [], False

    staged_paths: list[Path] = []
    markdown_staged = False
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        normalized = line.replace("\\", "/")
        if normalized.startswith("./"):
            normalized = normalized[2:]
        if normalized == MARKDOWN_PATH.as_posix():
            markdown_staged = True
            continue
        if not normalized.endswith(".py"):
            continue
        path = Path(normalized)
        try:
            path.relative_to(SOURCE_ROOT)
        except ValueError:
            continue
        staged_paths.append(path)
    return staged_paths, markdown_staged


def get_staged_markdown_row_titles() -> set[str]:
    try:
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--unified=0", "--", str(MARKDOWN_PATH)],
            text=True,
            cwd=Path.cwd(),
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return set()

    titles: set[str] = set()
    for line in output.splitlines():
        if not line.startswith("+| "):
            continue
        added_line = line[1:]
        match = ROW_RE.match(added_line)
        if not match:
            continue
        titles.add(match.group("problem").strip().lower())
    return titles


def get_staged_problem_numbers(staged_files: list[Path]) -> set[int]:
    numbers: set[int] = set()
    for path in staged_files:
        match = SOURCE_FILE_RE.match(path.name)
        if match:
            numbers.add(int(match.group("number")))
    return numbers


def fill_current_date_for_staged_rows(
    table_rows: list[dict],
    staged_files: list[Path] | None = None,
    staged_markdown_titles: set[str] | None = None,
) -> int:
    if not staged_files and not staged_markdown_titles:
        return 0

    staged_numbers = get_staged_problem_numbers(staged_files) if staged_files else set()
    now = datetime.now()
    updated_count = 0

    for row in table_rows:
        if row["latest"] is not None:
            continue

        problem_title_low = row["problem"].strip().lower()
        if staged_markdown_titles:
            if problem_title_low not in staged_markdown_titles:
                continue
        elif staged_numbers:
            match = re.match(r"^(?P<number>\d+)\.", row["problem"])
            if not match:
                continue
            number = int(match.group("number"))
            if number not in staged_numbers:
                continue
        else:
            continue

        row["latest"] = now
        row["latest_attempt_date"] = format_date(now)
        attempts = [part.strip() for part in row["attempts"].split(",") if part.strip()]
        today_text = format_date(now)
        if today_text not in attempts:
            attempts.append(today_text)
        row["attempts"] = ", ".join(attempts)
        row["next_review"] = format_date(compute_next_review_date(row["mastered"], now))
        updated_count += 1

    return updated_count


def update_existing_row_difficulties(table_rows: list[dict], staged_files: list[Path] | None = None) -> int:
    row_number_to_indices: dict[int, list[int]] = {}
    for index, row in enumerate(table_rows):
        match = re.match(r"^(?P<number>\d+)\.", row["problem"])
        if match:
            number = int(match.group("number"))
            row_number_to_indices.setdefault(number, []).append(index)

    if not row_number_to_indices:
        return 0

    paths = list(SOURCE_ROOT.rglob("*.py")) if staged_files is None else staged_files
    updated_count = 0
    for path in paths:
        match = SOURCE_FILE_RE.match(path.name)
        if not match:
            continue
        number = int(match.group("number"))
        row_indices = row_number_to_indices.get(number)
        if not row_indices:
            continue

        difficulty = extract_difficulty_from_source(path)
        if not difficulty:
            continue

        for row_index in row_indices:
            if table_rows[row_index]["difficulty"] == "Unknown":
                table_rows[row_index]["difficulty"] = difficulty
                updated_count += 1

    return updated_count


def discover_source_problems(existing_titles: set[str], staged_files: list[Path] | None = None) -> list[dict]:
    missing_rows: list[dict] = []
    if staged_files is None:
        paths = list(SOURCE_ROOT.rglob("*.py"))
    else:
        paths = staged_files

    use_today = staged_files is not None
    now = datetime.now() if use_today else None

    existing_numbers = {
        extract_problem_number(title)
        for title in existing_titles
        if extract_problem_number(title) is not None
    }

    for path in paths:
        match = SOURCE_FILE_RE.match(path.name)
        if not match:
            continue
        number = int(match.group("number"))
        raw_name = match.group("name")
        title = humanize_raw_name(raw_name)
        problem_title = f"{number}. {title}"
        if problem_title.lower() in existing_titles:
            continue
        if number in existing_numbers:
            continue
        difficulty = extract_difficulty_from_source(path) or "Unknown"
        missing_rows.append({
            "difficulty": difficulty,
            "problem": problem_title,
            "url": f"https://leetcode.com/problemset/all/?search={number}",
            "mastered": "N",
            "latest": now,
            "latest_attempt_date": format_date(now) if now else "",
            "attempts": format_date(now) if now else "",
            "next_review": format_date(compute_next_review_date("N", now)) if now else "",
        })
        existing_titles.add(problem_title.lower())
        existing_numbers.add(number)
    return missing_rows


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
            attempts_latest = parse_latest_attempt_date_from_attempts(attempts)
            if latest is None or (attempts_latest is not None and attempts_latest > latest):
                latest = attempts_latest
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

    parser = argparse.ArgumentParser(description="Update review progression markdown from source problem files.")
    parser.add_argument(
        "--staged-only",
        action="store_true",
        help="Only discover new problems from staged source files and fill missing dates for staged review rows.",
    )
    parser.add_argument(
        "--all-source",
        action="store_true",
        help="Scan all source files for new problems.",
    )
    args = parser.parse_args()

    staged_files = None
    markdown_staged = False
    if args.staged_only and args.all_source:
        parser.error("--staged-only and --all-source cannot be used together.")
    staged_markdown_titles: set[str] = set()
    if args.staged_only:
        staged_files, markdown_staged = get_staged_paths()
        staged_markdown_titles = get_staged_markdown_row_titles() if markdown_staged else set()
        print(f"Scanning {len(staged_files)} staged source file(s) for new problems.")
        if markdown_staged:
            print(
                f"Detected staged markdown table changes; only {len(staged_markdown_titles)} changed/added row(s) will be considered for current-date filling."
            )

    existing_titles = {
        row["problem"].strip().lower()
        for row in table_rows
    }

    updated_count = update_existing_row_difficulties(table_rows, staged_files=staged_files)
    if updated_count:
        print(f"Updated difficulty for {updated_count} existing review row(s) from source comments.")

    staged_date_count = fill_current_date_for_staged_rows(
        table_rows,
        staged_files=staged_files,
        staged_markdown_titles=staged_markdown_titles,
    )
    if staged_date_count:
        print(f"Filled current date for {staged_date_count} staged review row(s) with missing latest attempt dates.")

    discovered = discover_source_problems(existing_titles, staged_files=staged_files)
    if discovered:
        table_rows.extend(discovered)
        print(f"Discovered and added {len(discovered)} problem(s) from source files.")

    sorted_rows = sorted(
        table_rows,
        key=lambda entry: (entry["latest"] is not None, entry["latest"]),
        reverse=True,
    )

    sorted_lines = [build_row(entry) for entry in sorted_rows]

    try:
        header_index = prefix_lines.index(TABLE_HEADER)
    except ValueError:
        header_index = len(prefix_lines)
    
    # Remove old summary lines from prefix
    filtered_prefix = []
    for line in prefix_lines[:header_index]:
        if not (line.startswith("**Problems Done:**") or line.startswith("**Total Successful Attempts:**") or line.strip() == ""):
            filtered_prefix.append(line)
        elif line.strip() == "" and (not filtered_prefix or filtered_prefix[-1].strip() != ""):
            # Keep empty lines that aren't consecutive
            filtered_prefix.append(line)
    
    # Remove trailing empty lines before inserting summary
    while filtered_prefix and filtered_prefix[-1].strip() == "":
        filtered_prefix.pop()
    
    summary_lines = build_summary_lines(sorted_rows)
    new_prefix = filtered_prefix + summary_lines + prefix_lines[header_index:]

    new_lines = new_prefix + sorted_lines + suffix_lines
    if new_lines != lines:
        MARKDOWN_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print(f"Reordered {len(sorted_rows)} rows by latest attempt date in {MARKDOWN_PATH}")
    else:
        print(f"No reorder needed in {MARKDOWN_PATH}")


if __name__ == "__main__":
    main()
