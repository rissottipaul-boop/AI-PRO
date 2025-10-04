"""Semantic version & commit classification check.

This script enforces that the version bump in pyproject.toml matches the
highest impact conventional commit found in the git log for the current HEAD
range (compared to origin/main).

Rules (simplified):
 - feat!: or BREAKING CHANGE -> major bump
 - feat -> minor bump
 - fix, perf, refactor, docs, chore, test -> patch bump
 - If no qualifying commits -> no bump required

Exit codes:
 0 - OK
 1 - Version bump mismatch
 2 - Could not determine base reference
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PYPROJECT = Path("pyproject.toml")

COMMIT_REGEX = re.compile(r"^(?P<type>\w+)(?P<breaking>!?)\(?.*?\)?:", re.IGNORECASE)


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()


def get_base_ref() -> str | None:
    # Try origin/main first
    try:
        run(["git", "fetch", "origin", "main", "--depth", "1"])
        return "origin/main"
    except Exception:
        return None


def read_version() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    m = re.search(r"^version\s*=\s*\"(.*?)\"", text, re.MULTILINE)
    if not m:
        raise SystemExit("Could not find version in pyproject.toml")
    return m.group(1)


def classify_commits(log: str) -> str | None:
    highest = None
    for line in log.splitlines():
        m = COMMIT_REGEX.match(line)
        if not m:
            continue
        ctype = m.group("type").lower()
        breaking = bool(m.group("breaking")) or "breaking change" in line.lower()
        if breaking:
            return "major"  # highest possible
        if ctype == "feat":
            highest = highest or "minor"
        elif ctype in {"fix", "perf", "refactor", "docs", "chore", "test"} and highest is None:
            highest = "patch"
    return highest


def expected_bump_from_versions(old: str, new: str) -> str | None:
    def split(v: str) -> tuple[int, int, int]:
        parts = v.split(".")
        return tuple(int(x) for x in parts[:3])  # type: ignore

    o_major, o_minor, o_patch = split(old)
    n_major, n_minor, n_patch = split(new)
    if n_major > o_major:
        return "major"
    if n_minor > o_minor:
        return "minor"
    if n_patch > o_patch:
        return "patch"
    return None


def main() -> int:
    base = get_base_ref()
    if not base:
        print("::warning::Could not fetch base main branch; skipping version check")
        return 2
    current_version = read_version()
    try:
        old_file = run(["git", "show", f"{base}:pyproject.toml"])  # full file text
        old_version = old_file.split("version = ")[1].split("\n")[0].strip().strip('"')
    except Exception:
        print("::warning::Could not read base version; skipping")
        return 2

    if current_version == old_version:
        # No bump; ensure no commits that would require bump
        log = run(["git", "log", f"{base}..HEAD", "--pretty=%s"])
        impact = classify_commits(log)
        if impact:
            print(f"::error::Commits require at least a {impact} bump but version not changed")
            return 1
        print("Version unchanged; no impactful commits – OK")
        return 0

    expected = expected_bump_from_versions(old_version, current_version)
    if not expected:
        print("::error::Version changed but bump type could not be determined")
        return 1
    log = run(["git", "log", f"{base}..HEAD", "--pretty=%s"])
    impact = classify_commits(log)
    if impact and impact != expected:
        print(f"::error::Version bump '{expected}' does not match commit impact '{impact}'")
        return 1
    if not impact:
        print("::warning::Version bumped without qualifying commits")
    print("Version bump matches commit impact – OK")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI wrapper
    sys.exit(main())
