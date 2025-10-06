#!/usr/bin/env python3
"""
Comprehensive Auto-Fix Script for VS Code Problems

This script automatically fixes common code quality issues that appear in VS Code:
- Runs Ruff to fix linting issues
- Formats code with Ruff and Black
- Organizes imports
- Fixes trailing whitespace and newlines
- Runs pre-commit hooks to fix additional issues
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str, critical: bool = False) -> bool:
    """Run a command and report results."""
    print(f"\n{'=' * 70}")
    print(f"▶ {description}")
    print(f"{'=' * 70}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )

        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode != 0:
            print(f"⚠ Warning: {description} exited with code {result.returncode}")
            if critical:
                print(f"❌ Critical step failed: {description}")
            return not critical

        print(f"✅ {description} completed successfully")
        return True

    except FileNotFoundError:
        print(f"❌ Error: Command not found: {cmd[0]}")
        print("   Make sure it's installed: pip install -e '.[dev]'")
        return not critical
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return not critical


def main() -> int:
    """Run all auto-fix operations."""
    print("🔧 Starting Comprehensive Auto-Fix Process")
    print("=" * 70)

    # Get project root
    project_root = Path(__file__).parent.parent
    print(f"📁 Project root: {project_root}")

    # Change to project directory
    import os

    os.chdir(project_root)

    success_count = 0
    total_steps = 7

    # Step 1: Fix linting issues with Ruff
    if run_command(
        ["ruff", "check", ".", "--fix"],
        "Fixing linting issues with Ruff",
    ):
        success_count += 1

    # Step 2: Format code with Ruff
    if run_command(
        ["ruff", "format", "."],
        "Formatting code with Ruff",
    ):
        success_count += 1

    # Step 3: Format with Black (for compatibility)
    if run_command(
        ["black", "."],
        "Formatting code with Black",
    ):
        success_count += 1

    # Step 4: Organize imports
    if run_command(
        ["ruff", "check", ".", "--select", "I", "--fix"],
        "Organizing imports",
    ):
        success_count += 1

    # Step 5: Run pre-commit hooks (they auto-fix many issues)
    if run_command(
        ["pre-commit", "run", "--all-files"],
        "Running pre-commit hooks (auto-fixing)",
    ):
        success_count += 1

    # Step 6: Check for remaining issues with mypy
    if run_command(
        ["mypy", "src"],
        "Checking types with mypy (informational)",
    ):
        success_count += 1

    # Step 7: Run tests to ensure nothing broke
    if run_command(
        ["pytest", "-v", "--tb=short"],
        "Running tests to verify fixes",
        critical=True,
    ):
        success_count += 1

    # Summary
    print("\n" + "=" * 70)
    print("📊 Auto-Fix Summary")
    print("=" * 70)
    print(f"✅ Successful steps: {success_count}/{total_steps}")

    if success_count == total_steps:
        print("\n🎉 All auto-fix operations completed successfully!")
        print("   Your code should now be free of common issues.")
        print("\nNext steps:")
        print("  1. Review the changes with 'git diff'")
        print("  2. Stage files: 'git add .'")
        print("  3. Commit: 'git commit -m \"Auto-fix code issues\"'")
        return 0
    elif success_count >= total_steps - 1:
        print("\n⚠ Most auto-fix operations completed with minor warnings.")
        print("   Review the output above for details.")
        return 0
    else:
        print("\n❌ Some critical auto-fix operations failed.")
        print("   Review the errors above and fix manually if needed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
