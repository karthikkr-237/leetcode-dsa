#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"

AUTO_START = "<!-- AUTO_STATS_START -->"
AUTO_END = "<!-- AUTO_STATS_END -->"

DIFFICULTIES = ("Easy", "Medium", "Hard")
DIFFICULTY_SET = {d.lower() for d in DIFFICULTIES}

EXTENSION_TO_LANGUAGE = {
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".kt": "Kotlin",
    ".swift": "Swift",
}

SOLUTION_FILE_RE = re.compile(r"^(?P<id>\d+)-(?P<name>.+)$")
AUTO_BLOCK_RE = re.compile(
    rf"{re.escape(AUTO_START)}.*?{re.escape(AUTO_END)}",
    re.DOTALL,
)


@dataclass(frozen=True)
class SolutionFile:
    rel_path: Path
    topic: str
    difficulty: str
    problem_id: str
    problem_name: str
    language: str


def normalize_problem_name(raw_name: str) -> str:
    cleaned = raw_name.replace("_", " ").replace("-", " ").strip()
    return " ".join(part.capitalize() for part in cleaned.split())


def iter_solution_files(root: Path) -> Iterable[SolutionFile]:
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        rel = file_path.relative_to(root)
        parts = rel.parts

        if len(parts) < 3:
            continue

        topic, difficulty = parts[0], parts[1]
        if topic.startswith("."):
            continue
        if difficulty.lower() not in DIFFICULTY_SET:
            continue

        ext = file_path.suffix.lower()
        language = EXTENSION_TO_LANGUAGE.get(ext)
        if not language:
            continue

        stem_match = SOLUTION_FILE_RE.match(file_path.stem)
        if not stem_match:
            continue

        problem_id = stem_match.group("id")
        problem_name = normalize_problem_name(stem_match.group("name"))

        yield SolutionFile(
            rel_path=rel,
            topic=topic,
            difficulty=difficulty.capitalize(),
            problem_id=problem_id,
            problem_name=problem_name,
            language=language,
        )


def sorted_rows_from_sets(data: dict[str, set[str]], empty_label: str) -> list[str]:
    if not data:
        return [f"| {empty_label} | 0 |"]

    items = sorted(data.items(), key=lambda item: (-len(item[1]), item[0].lower()))
    return [f"| {name} | {len(problem_ids)} |" for name, problem_ids in items]


def get_recent_problem_lines(
    solutions: list[SolutionFile],
    files_by_path: dict[Path, SolutionFile],
    per_problem_display: dict[str, str],
    limit: int = 8,
) -> list[str]:
    if not solutions:
        return ["- None"]

    problem_ids_seen: set[str] = set()
    ordered_ids: list[str] = []

    try:
        proc = subprocess.run(
            ["git", "log", "--name-only", "--pretty=format:", "--diff-filter=AM", "--", "."],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        for line in proc.stdout.splitlines():
            candidate = line.strip()
            if not candidate:
                continue
            rel = Path(candidate)
            solution = files_by_path.get(rel)
            if not solution:
                continue
            if solution.problem_id in problem_ids_seen:
                continue
            problem_ids_seen.add(solution.problem_id)
            ordered_ids.append(solution.problem_id)
            if len(ordered_ids) >= limit:
                break
    except (subprocess.CalledProcessError, OSError):
        ordered_ids = []

    if len(ordered_ids) < limit:
        remaining = sorted(
            solutions,
            key=lambda s: (
                -(ROOT / s.rel_path).stat().st_mtime,
                s.rel_path.as_posix(),
            ),
        )
        for solution in remaining:
            if solution.problem_id in problem_ids_seen:
                continue
            problem_ids_seen.add(solution.problem_id)
            ordered_ids.append(solution.problem_id)
            if len(ordered_ids) >= limit:
                break

    return [f"- {per_problem_display[problem_id]}" for problem_id in ordered_ids] or ["- None"]


def build_auto_section(solutions: list[SolutionFile]) -> str:
    unique_problem_ids: set[str] = set()
    difficulty_to_ids: dict[str, set[str]] = defaultdict(set)
    topic_to_ids: dict[str, set[str]] = defaultdict(set)
    language_to_ids: dict[str, set[str]] = defaultdict(set)

    files_by_path: dict[Path, SolutionFile] = {}
    id_to_topics: dict[str, set[str]] = defaultdict(set)
    id_to_difficulties: dict[str, set[str]] = defaultdict(set)
    id_to_names: dict[str, set[str]] = defaultdict(set)

    for solution in solutions:
        files_by_path[solution.rel_path] = solution
        unique_problem_ids.add(solution.problem_id)
        difficulty_to_ids[solution.difficulty].add(solution.problem_id)
        topic_to_ids[solution.topic].add(solution.problem_id)
        language_to_ids[solution.language].add(solution.problem_id)

        id_to_topics[solution.problem_id].add(solution.topic)
        id_to_difficulties[solution.problem_id].add(solution.difficulty)
        id_to_names[solution.problem_id].add(solution.problem_name)

    display_by_problem_id: dict[str, str] = {}
    for problem_id, names in id_to_names.items():
        preferred = sorted(names)[0]
        display_by_problem_id[problem_id] = f"{problem_id.zfill(4)} {preferred}"

    total = len(unique_problem_ids)
    easy = len(difficulty_to_ids.get("Easy", set()))
    medium = len(difficulty_to_ids.get("Medium", set()))
    hard = len(difficulty_to_ids.get("Hard", set()))

    topic_rows = "\n".join(sorted_rows_from_sets(topic_to_ids, "None"))
    language_rows = "\n".join(sorted_rows_from_sets(language_to_ids, "None"))

    recent_rows = "\n".join(
        get_recent_problem_lines(solutions, files_by_path, display_by_problem_id)
    )

    duplicate_lines: list[str] = []
    for problem_id in sorted(unique_problem_ids, key=lambda pid: int(pid)):
        topics = sorted(id_to_topics[problem_id])
        difficulties = sorted(id_to_difficulties[problem_id])
        if len(topics) > 1 or len(difficulties) > 1:
            duplicate_lines.append(
                f"- {display_by_problem_id[problem_id]} — topics: {', '.join(topics)}; "
                f"difficulties: {', '.join(difficulties)}"
            )

    if duplicate_lines:
        duplicate_section = "\n".join([
            "### Duplicate ID Report",
            "",
            "Conflicting metadata detected. Counts remain deduplicated by problem ID:",
            *duplicate_lines,
        ])
    else:
        duplicate_section = "\n".join([
            "### Duplicate ID Report",
            "",
            "No duplicate topic/difficulty metadata conflicts detected.",
        ])

    return "\n".join([
        AUTO_START,
        "## Repository Statistics",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Total Problems | {total} |",
        f"| Easy | {easy} |",
        f"| Medium | {medium} |",
        f"| Hard | {hard} |",
        "",
        "### Topic Statistics",
        "",
        "| Topic | Unique Problems |",
        "|---|---:|",
        topic_rows,
        "",
        "### Language Statistics",
        "",
        "| Language | Unique Problems |",
        "|---|---:|",
        language_rows,
        "",
        "### Recently Added",
        "",
        recent_rows,
        "",
        duplicate_section,
        AUTO_END,
    ])


def update_readme(readme_path: Path, auto_block: str) -> bool:
    if readme_path.exists():
        original = readme_path.read_text(encoding="utf-8")
    else:
        original = "# leetcode-dsa\n\nA structured collection of LeetCode solutions and DSA practice.\n"

    if AUTO_BLOCK_RE.search(original):
        updated = AUTO_BLOCK_RE.sub(auto_block, original, count=1)
    else:
        marker_present = AUTO_START in original or AUTO_END in original
        cleaned = original.replace(AUTO_START, "").replace(AUTO_END, "") if marker_present else original
        cleaned = cleaned.rstrip()
        updated = f"{cleaned}\n\n{auto_block}\n"

    if updated == original:
        return False

    readme_path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    solutions = sorted(
        iter_solution_files(ROOT),
        key=lambda s: (int(s.problem_id), s.topic.lower(), s.difficulty, s.rel_path.as_posix()),
    )
    auto_block = build_auto_section(solutions)
    changed = update_readme(README_PATH, auto_block)
    print("README updated" if changed else "README already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
