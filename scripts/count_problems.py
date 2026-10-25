#!/usr/bin/env python3
"""Refresh or check the manuscript's numbered-problem statistics.

Uses only Python's standard library. The parser follows this manuscript's
explicit section/subsection/problem environments; it does not expand TeX macros.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "papers/src/scv-problem-list.tex"
START_MARKER = "<!-- problem-counts:start -->"
END_MARKER = "<!-- problem-counts:end -->"
CATEGORIES = {
    "Closed problems with complete solutions": "closed",
    "Open problems with partial results": "partial_results",
    "Wide-open problems": "wide_open",
}
CATEGORY_LABELS = {
    "closed": "Closed",
    "partial_results": "Partial results",
    "wide_open": "Wide-open",
}


def strip_comments(text: str) -> str:
    """Remove TeX comments while preserving escaped percent signs and lines."""
    lines = []
    for line in text.splitlines():
        for position, char in enumerate(line):
            if char != "%":
                continue
            previous = position - 1
            while previous >= 0 and line[previous] == "\\":
                previous -= 1
            if (position - previous - 1) % 2 == 0:
                line = line[:position]
                break
        lines.append(line)
    return "\n".join(lines)


def braced_argument(text: str, position: int) -> tuple[str, int]:
    """Read one balanced brace argument, including nested formatting braces."""
    while position < len(text) and text[position].isspace():
        position += 1
    if position >= len(text) or text[position] != "{":
        raise ValueError("Expected a braced section title")
    start = position + 1
    depth = 1
    position += 1
    while position < len(text):
        char = text[position]
        if char == "\\" and position + 1 < len(text):
            if text[position + 1] in "{}%":
                position += 2
                continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:position], position + 1
        position += 1
    raise ValueError("Unbalanced braces in a section title")


def plain_title(title: str) -> str:
    if title.startswith(r"\texorpdfstring"):
        title, _ = braced_argument(title, len(r"\texorpdfstring"))
    return title.replace("$L^2$", "L²").replace(r"\&", "&")


def collect_counts() -> dict:
    text = strip_comments(SOURCE.read_text(encoding="utf-8"))
    document = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", text, re.S)
    if document is None:
        raise ValueError("The source must contain a complete document environment")
    text = document.group(1)
    if re.search(r"\\(?:setcounter|addtocounter)\s*\{problem\}", text):
        raise ValueError("Manual problem-counter changes require a parser review")
    if re.search(r"\\(?:input|include)\s*\{", text):
        raise ValueError("External TeX inputs require a parser review")

    token = re.compile(
        r"\\(?P<heading>section|subsection)(?P<star>\*)?\s*(?=\{)"
        r"|\\(?P<environment>begin|end)\s*\{problem\}"
    )
    sections = []
    section = None
    category = None
    inside_problem = False
    for match in token.finditer(text):
        if match.group("heading"):
            title, _ = braced_argument(text, match.end())
            if inside_problem:
                raise ValueError("A section heading occurs inside a problem")
            if match.group("star"):
                category = None
                continue
            if match.group("heading") == "section":
                section = {
                    "section": len(sections) + 1,
                    "title": plain_title(title),
                    "total": 0,
                    "counts": {key: 0 for key in CATEGORY_LABELS},
                    "problem_numbers": {key: [] for key in CATEGORY_LABELS},
                }
                sections.append(section)
                category = None
            else:
                if title not in CATEGORIES:
                    raise ValueError(f"Unknown problem category: {title}")
                category = CATEGORIES[title]
            continue

        if match.group("environment") == "begin":
            if inside_problem:
                raise ValueError("Nested problem environments are not supported")
            if section is None or category is None:
                raise ValueError("A problem has no numbered section or known category")
            inside_problem = True
            section["total"] += 1
            section["counts"][category] += 1
            section["problem_numbers"][category].append(
                f"{section['section']}.{section['total']}"
            )
        else:
            if not inside_problem:
                raise ValueError("An end{problem} has no matching begin{problem}")
            inside_problem = False
    if inside_problem:
        raise ValueError("A problem environment is not closed")
    if not sections:
        raise ValueError("No numbered sections were found")

    totals = {
        key: sum(section["counts"][key] for section in sections)
        for key in CATEGORY_LABELS
    }
    return {
        "schema_version": 1,
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "counting_unit": "One explicitly numbered problem environment",
        "category_headings": {value: key for key, value in CATEGORIES.items()},
        "total": sum(totals.values()),
        "subject_count": len(sections),
        "totals_by_status": totals,
        "sections": sections,
    }


def summary_table(data: dict) -> str:
    totals = data["totals_by_status"]
    lines = [
        "| Section | Subject | Closed | Partial results | Wide-open | Total |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for section in data["sections"]:
        counts = section["counts"]
        lines.append(
            f"| {section['section']} | {section['title']} | {counts['closed']} | "
            f"{counts['partial_results']} | {counts['wide_open']} | {section['total']} |"
        )
    lines.append(
        f"| **Total** | | **{totals['closed']}** | **{totals['partial_results']}** | "
        f"**{totals['wide_open']}** | **{data['total']}** |"
    )
    return "\n".join(lines)


def readme_summary(data: dict) -> str:
    totals = data["totals_by_status"]
    return (
        f"**{data['total']} numbered problems across {data['subject_count']} subject areas:** "
        f"{totals['closed']} closed, {totals['partial_results']} with partial results, "
        f"and {totals['wide_open']} wide-open.\n\n"
        + summary_table(data)
    )


def statistics_document(data: dict) -> str:
    total = data["total"]
    totals = data["totals_by_status"]
    lines = [
        "# Problem statistics",
        "",
        "Generated from [the LaTeX source](papers/src/scv-problem-list.tex) by "
        "[`scripts/count_problems.py`](scripts/count_problems.py).",
        "",
        "## Counting convention",
        "",
        "Each independently numbered `problem` environment counts as one problem. "
        "Subquestions within one environment are not split. Multiple source labels "
        "attached to one problem do not increase the count. References in remarks "
        "and TeX comments are excluded.",
        "",
        "Status categories follow the manuscript: closed problems have been resolved "
        "affirmatively or negatively; partial-results problems have substantial known "
        "cases or weaker results; wide-open problems have a central question that "
        "remains largely unresolved. The statistics describe the manuscript's "
        "classification and do not independently reassess the literature.",
        "",
        "## By resolution status",
        "",
        "| Status | Count | Share |",
        "| --- | ---: | ---: |",
    ]
    for key, label in CATEGORY_LABELS.items():
        lines.append(f"| {label} | {totals[key]} | {100 * totals[key] / total:.2f}% |")
    lines.extend([
        f"| **Total** | **{total}** | **100%** |",
        "",
        f"The two unresolved categories together contain **{totals['partial_results'] + totals['wide_open']}** problems.",
        "",
        "## By subject and status",
        "",
        summary_table(data),
        "",
        "## Problem-number ranges",
        "",
        "| Section | Closed | Partial results | Wide-open |",
        "| --- | --- | --- | --- |",
    ])
    for section in data["sections"]:
        ranges = []
        for key in CATEGORY_LABELS:
            numbers = section["problem_numbers"][key]
            ranges.append(
                "None" if not numbers else numbers[0] if len(numbers) == 1
                else f"{numbers[0]}–{numbers[-1]}"
            )
        lines.append(f"| {section['section']} | " + " | ".join(ranges) + " |")
    lines.extend([
        "",
        "## Refresh or verify",
        "",
        "From the repository root:",
        "",
        "```sh",
        "python scripts/count_problems.py",
        "python scripts/count_problems.py --check",
        "```",
        "",
        "The first command refreshes this file, `data/problem-counts.json`, and "
        "the marked statistics block in `README.md`. The second checks them "
        "without writing. No TeX installation is required for either command.",
        "",
    ])
    return "\n".join(lines)


def expected_outputs(data: dict) -> dict[Path, str]:
    readme = ROOT / "README.md"
    if not readme.exists():
        raise ValueError("README.md must exist and contain the problem-counts markers")
    contents = readme.read_text(encoding="utf-8")
    if contents.count(START_MARKER) != 1 or contents.count(END_MARKER) != 1:
        raise ValueError("README.md must contain exactly one pair of problem-counts markers")
    start = contents.index(START_MARKER) + len(START_MARKER)
    end = contents.index(END_MARKER)
    if end < start:
        raise ValueError("The README statistics markers are reversed")
    updated = contents[:start] + "\n\n" + readme_summary(data) + "\n\n" + contents[end:]
    return {
        ROOT / "data/problem-counts.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        ROOT / "statistics.md": statistics_document(data),
        readme: updated,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check generated statistics without writing")
    args = parser.parse_args()
    try:
        data = collect_counts()
        outputs = expected_outputs(data)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    stale = []
    for path, expected in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8", newline="\n")
    if stale:
        print("Stale or missing statistics: " + ", ".join(stale), file=sys.stderr)
        print("Run: python scripts/count_problems.py", file=sys.stderr)
        return 1
    totals = data["totals_by_status"]
    action = "Verified" if args.check else "Refreshed"
    print(
        f"{action}: {data['total']} problems in {data['subject_count']} sections "
        f"({totals['closed']} closed, {totals['partial_results']} partial, "
        f"{totals['wide_open']} wide-open)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
