# Auto-Fix Guide for VS Code

This guide explains the comprehensive auto-fix capabilities implemented in this project to automatically resolve code issues displayed in VS Code.

## Overview

The project now includes multiple layers of automatic problem resolution:

1. **Real-time Auto-Fix (On Save)** - Fixes issues as you type and save
2. **Manual Auto-Fix Tasks** - One-click fixes for all problems
3. **Pre-commit Auto-Fix** - Fixes issues before committing
4. **Comprehensive Auto-Fix Script** - Complete automated problem resolution

---

## 1. Real-Time Auto-Fix (On Save)

These settings automatically fix issues every time you save a file:

### Enabled Auto-Fixes

✅ **Code Formatting**
- Formats Python code with Ruff (PEP 8 compliant)
- Consistent code style across the project

✅ **Import Organization**
- Automatically sorts and organizes imports
- Removes unused imports
- Groups imports by type (standard, third-party, local)

✅ **Trailing Whitespace**
- Removes all trailing spaces at end of lines
- Prevents unnecessary diffs

✅ **Final Newline**
- Ensures every file ends with a newline
- Fixes EOF issues that cause pre-commit hooks to fail

✅ **Line Endings**
- Normalizes line endings to LF (\n)
- Consistent across platforms

✅ **All Linting Fixes**
- Fixes all auto-fixable linting issues
- Includes unused variables, imports, and more

### Configuration

These are configured in `.vscode/settings.json`:

```json
{
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit",
        "source.fixAll": "explicit"
    },
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "files.trimFinalNewlines": true,
    "ruff.fixAll": true
}
```

### Usage

Just save your file (`Ctrl+S` or `Cmd+S`) and watch the issues disappear!

---

## 2. Manual Auto-Fix Tasks

Quick-access tasks for fixing all problems at once:

### "Auto-Fix All Problems" Task

Runs the comprehensive auto-fix script that:
1. Fixes all linting issues with Ruff
2. Formats code with Ruff and Black
3. Organizes all imports
4. Runs pre-commit hooks
5. Verifies with type checking
6. Runs tests to ensure nothing broke

**How to run:**
- Press `Ctrl+Shift+P` (Command Palette)
- Type "Tasks: Run Task"
- Select "Auto-Fix All Problems"

**Or via terminal:**
```bash
python scripts/autofix.py
```

### "Fix All Issues (Comprehensive)" Task

A faster alternative that runs:
- Ruff linting with auto-fix
- Ruff formatting
- Black formatting
- All pre-commit hooks

**How to run:**
- Press `Ctrl+Shift+P` (Command Palette)
- Type "Tasks: Run Task"
- Select "Fix All Issues (Comprehensive)"

**Or via terminal:**
```bash
ruff check . --fix && ruff format . && black . && pre-commit run --all-files
```

---

## 3. Pre-commit Auto-Fix

Pre-commit hooks automatically fix many issues before you commit:

### Auto-Fixing Hooks

✅ **trailing-whitespace** - Removes trailing spaces
✅ **end-of-file-fixer** - Adds missing final newlines
✅ **ruff** - Fixes linting issues
✅ **ruff format** - Formats code
✅ **black** - Additional formatting

### Workflow

1. Make changes to files
2. Stage files: `git add .`
3. Commit: `git commit -m "message"`
4. Hooks run automatically and fix issues
5. If hooks modified files:
   - Review changes: `git diff`
   - Re-stage: `git add .`
   - Commit again: `git commit -m "message"`

### Installation

Pre-commit hooks are installed automatically in CI, but you can install them locally:

```bash
pre-commit install
```

Or use the VS Code task:
- Press `Ctrl+Shift+P`
- Type "Tasks: Run Task"
- Select "Pre-commit Install"

---

## 4. Comprehensive Auto-Fix Script

The `scripts/autofix.py` script performs a complete auto-fix sequence:

### What It Does

1. **Fix Linting Issues** - Runs `ruff check . --fix`
2. **Format Code** - Runs `ruff format .` and `black .`
3. **Organize Imports** - Runs `ruff check . --select I --fix`
4. **Run Pre-commit Hooks** - Applies all hook fixes
5. **Type Check** - Verifies with mypy (informational)
6. **Run Tests** - Ensures nothing broke

### Output

The script provides detailed feedback:
- ✅ Success messages for each step
- ⚠️ Warnings for non-critical issues
- ❌ Errors for critical failures
- 📊 Summary of successful steps

### Example Output

```
🔧 Starting Comprehensive Auto-Fix Process
======================================================================

✅ Fixing linting issues with Ruff completed successfully
✅ Formatting code with Ruff completed successfully
✅ Formatting code with Black completed successfully
✅ Organizing imports completed successfully
✅ Running pre-commit hooks completed successfully
✅ Checking types with mypy completed successfully
✅ Running tests to verify fixes completed successfully

======================================================================
📊 Auto-Fix Summary
======================================================================
✅ Successful steps: 7/7

🎉 All auto-fix operations completed successfully!
```

---

## Problem Types That Get Auto-Fixed

### Python Code Issues

✅ Import order and organization
✅ Unused imports
✅ Unused variables (with warnings)
✅ Code formatting (indentation, spacing)
✅ Line length violations (when possible)
✅ Trailing commas in multi-line structures
✅ Quote style consistency
✅ Docstring formatting

### File Issues

✅ Trailing whitespace
✅ Missing final newline
✅ Multiple blank lines at EOF
✅ CRLF → LF line ending conversion
✅ Inconsistent indentation

### Common Errors

✅ F401: Unused import
✅ F841: Unused variable assignment
✅ E501: Line too long (when auto-fixable)
✅ W291: Trailing whitespace
✅ W293: Blank line with whitespace
✅ E302/E303: Expected blank lines

---

## Workflow Examples

### Scenario 1: Working on a Feature

1. Write code
2. Save file → Auto-fixes apply automatically
3. Continue working
4. Commit → Pre-commit hooks fix any remaining issues

**No manual intervention needed!**

### Scenario 2: Fixing Multiple Files

1. Make changes across multiple files
2. Run "Auto-Fix All Problems" task
3. Review changes with `git diff`
4. Commit all fixes at once

### Scenario 3: Pre-commit Hook Failed

If pre-commit hooks modify files and fail the commit:

1. Check what was fixed: `git diff`
2. Stage the fixes: `git add .`
3. Commit again: `git commit -m "your message"`

**Or** just run the auto-fix script:
```bash
python scripts/autofix.py
```

---

## Keyboard Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| Save & Auto-fix | `Ctrl+S` / `Cmd+S` | Saves and applies all on-save fixes |
| Format Document | `Shift+Alt+F` | Manually format current file |
| Organize Imports | `Shift+Alt+O` | Manually organize imports |
| Run Task | `Ctrl+Shift+P` → "Tasks" | Access all auto-fix tasks |
| Run Tests | `Ctrl+Shift+T` | Test after fixes |
| Run Build | `Ctrl+Shift+B` | Full CI check with fixes |

---

## Configuration Files

### .vscode/settings.json
Contains all auto-fix settings for VS Code:
- Format on save
- Code actions on save
- File auto-fixes
- Ruff configuration

### .vscode/tasks.json
Defines auto-fix tasks:
- Auto-Fix All Problems
- Fix All Issues (Comprehensive)
- Individual fix tasks (Lint, Format, etc.)

### .pre-commit-config.yaml
Configures pre-commit hooks:
- File fixing hooks
- Linting hooks
- Formatting hooks
- Security hooks

### scripts/autofix.py
The comprehensive auto-fix script that orchestrates all fixes.

---

## Troubleshooting

### Auto-fix Not Working

**Check:**
1. VS Code settings are loaded (reload window)
2. Ruff extension is installed
3. Python extension is installed
4. File is saved (auto-fix runs on save)

**Solution:**
- Reload VS Code: `Ctrl+Shift+P` → "Reload Window"
- Install extensions: `Ctrl+Shift+P` → "Extensions: Install Extensions"

### Pre-commit Hooks Keep Failing

**Problem:** Hooks modify files, causing commit to fail repeatedly

**Solution 1 (Recommended):**
Enable all auto-fix settings in VS Code so files are already correct before committing.

**Solution 2:**
Run the auto-fix script before committing:
```bash
python scripts/autofix.py
git add .
git commit -m "message"
```

**Solution 3:**
Skip hooks temporarily (not recommended):
```bash
git commit --no-verify -m "message"
```

### Some Issues Not Auto-Fixable

Some issues require manual fixes:
- Type errors (incorrect type annotations)
- Logic errors
- Missing docstrings
- Complex refactoring needs

**For these:**
1. Review the error message in VS Code
2. Click the lightbulb icon for suggestions
3. Apply suggested fixes or fix manually

---

## Best Practices

### Do's ✅

- **Enable auto-format on save** (already configured)
- **Review auto-fixes before committing**
- **Run auto-fix script regularly** (e.g., before PRs)
- **Keep extensions updated**
- **Trust the auto-fixes** - they follow best practices

### Don'ts ❌

- **Don't disable auto-fix** without good reason
- **Don't skip pre-commit hooks** regularly
- **Don't ignore type errors** - they won't auto-fix
- **Don't commit without testing** - auto-fix runs tests for a reason

---

## Advanced Usage

### Custom Auto-Fix

Add custom auto-fixes to `.vscode/settings.json`:

```json
{
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit",
        "source.fixAll": "explicit",
        "source.fixAll.ruff": "explicit",
        // Add more here
    }
}
```

### Selective Auto-Fix

To fix only specific file types:

```json
{
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit"
        }
    },
    "[markdown]": {
        "editor.formatOnSave": false
    }
}
```

### Auto-Fix on Focus Change

Fix issues when switching between files:

```json
{
    "files.autoSave": "onFocusChange",
    "editor.formatOnSave": true
}
```

---

## Integration with AI Agents

These auto-fix capabilities are optimized for AI agents:

1. **Consistent Code Style** - AI doesn't have to worry about formatting
2. **Auto-fixing Errors** - AI's code is automatically corrected
3. **Pre-commit Validation** - Ensures AI changes meet quality standards
4. **Comprehensive Script** - AI can run one command to fix everything

---

## Summary

This project includes **4 layers of auto-fix**:

1. **On-save fixes** (instant, automatic)
2. **Manual tasks** (one-click, comprehensive)
3. **Pre-commit hooks** (automatic, before commit)
4. **Auto-fix script** (comprehensive, on-demand)

**Result:** Most code issues are fixed automatically, with minimal manual intervention needed.

---

## References

- [VS Code Settings Guide](./VSCODE_SETTINGS_GUIDE.md)
- [Git & VS Code Automation Summary](./GIT_VSCODE_AUTOMATION_SUMMARY.md)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pre-commit Documentation](https://pre-commit.com/)

## Support

For issues or questions:
1. Review this guide
2. Check [VSCODE_SETTINGS_GUIDE.md](./VSCODE_SETTINGS_GUIDE.md)
3. Run the auto-fix script: `python scripts/autofix.py`
4. Check VS Code Output panels
5. Open an issue on GitHub

---

**Last Updated:** December 2024  
**Status:** ✅ Fully Implemented and Tested
