# Auto-Fix Guide for VS Code

This guide explains the comprehensive auto-fix capabilities implemented in this project to automatically resolve code issues displayed in VS Code.

## Overview

The project includes multiple layers of auto-fixing:

1. **Real-Time Auto-Fix** - On save (via VS Code settings)
2. **Manual Auto-Fix Tasks** - One-click tasks in VS Code
3. **Pre-commit Auto-Fix** - Automatic fixes before committing
4. **Comprehensive Auto-Fix Script** - Complete auto-fix workflow

## 1. Real-Time Auto-Fix (On Save)

When you save a Python file in VS Code, the following fixes are applied automatically:

### What Gets Fixed

- **Linting issues** - Ruff fixes common code issues
- **Code formatting** - Ruff formats to consistent style
- **Import organization** - Imports are sorted and organized
- **Trailing whitespace** - Removed from all lines
- **Final newline** - Ensures file ends with newline
- **Line endings** - Normalized to LF (Unix-style)

### How It Works

The `.vscode/settings.json` file configures:

```json
{
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.fixAll": "explicit",
        "source.organizeImports": "explicit"
    },
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true
}
```

### Requirements

- Install recommended extensions (Ruff, Python)
- VS Code will prompt you when opening the workspace

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

**Or use the keyboard shortcut:**
- Press `Ctrl+Shift+B` (Default Build Task)

**Or via terminal:**
```bash
python scripts/autofix.py
```

### Other Useful Tasks

- **Run Tests** - Run all tests with coverage
- **Lint with Ruff** - Check and fix linting issues only
- **Format with Ruff** - Format code only
- **Type Check with mypy** - Run type checking
- **Run Pre-commit Hooks** - Run all pre-commit hooks

## 3. Pre-commit Auto-Fix

Before each commit, pre-commit hooks automatically fix issues:

### What Gets Fixed

- **Ruff fixes** - Auto-fix linting issues
- **Code formatting** - Ruff and Black formatting
- **Type checking** - mypy validation
- **Trailing whitespace** - Removed
- **End-of-file issues** - Fixed
- **Mixed line endings** - Normalized
- **Secret leaks** - Detected (via gitleaks)

### How to Use

Pre-commit hooks run automatically when you commit:

```bash
git commit -m "Your message"
```

If hooks modify files, you'll need to stage and commit again:

```bash
git add .
git commit -m "Your message"
```

### Manual Pre-commit Run

```bash
# Run on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run
```

## 4. Comprehensive Auto-Fix Script

The `scripts/autofix.py` script provides the most thorough auto-fix workflow.

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

| Issue Type | Auto-Fixed By | When |
|------------|---------------|------|
| Import order | Ruff | On save, pre-commit, script |
| Unused imports | Ruff | On save, pre-commit, script |
| Line length | Ruff, Black | On save, pre-commit, script |
| Indentation | Ruff, Black | On save, pre-commit, script |
| Quotes (single vs double) | Ruff, Black | On save, pre-commit, script |
| Trailing commas | Ruff, Black | On save, pre-commit, script |
| Whitespace | All | On save, pre-commit, script |
| Type hints (basic) | Manual | - |

### File Issues

| Issue Type | Auto-Fixed By | When |
|------------|---------------|------|
| Trailing whitespace | VS Code, pre-commit | On save, pre-commit |
| Missing final newline | VS Code, pre-commit | On save, pre-commit |
| Extra blank lines at EOF | VS Code, pre-commit | On save, pre-commit |
| Mixed line endings (CRLF/LF) | VS Code, pre-commit | On save, pre-commit |
| File encoding | VS Code | On save |

### Git & Security

| Issue Type | Detected By | When |
|------------|-------------|------|
| Private keys in code | gitleaks | Pre-commit |
| Secrets/tokens | gitleaks | Pre-commit |
| Large files | pre-commit | Pre-commit |
| Merge conflicts | Git | Commit time |

---

## Workflow Examples

### Example 1: Quick Fix Before Commit

```bash
# Run auto-fix
python scripts/autofix.py

# Review changes
git diff

# Commit
git add .
git commit -m "Fix code quality issues"
```

### Example 2: Fix Single File

```bash
# Open file in VS Code
code src/autonomous_dev/example.py

# Make changes and save (Ctrl+S)
# Auto-fix runs automatically on save

# Commit
git add src/autonomous_dev/example.py
git commit -m "Update example.py"
```

### Example 3: Fix All Before PR

```bash
# Run comprehensive auto-fix
python scripts/autofix.py

# Verify tests pass
pytest -v

# Check diff
git diff

# Commit all fixes
git add .
git commit -m "chore: auto-fix all code quality issues"

# Push (auto-syncs if using VS Code)
git push
```

---

## Keyboard Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| Auto-Fix All | `Ctrl+Shift+B` | Run comprehensive auto-fix |
| Save & Auto-Fix | `Ctrl+S` | Save file and trigger auto-fix |
| Format Document | `Shift+Alt+F` | Format current file |
| Organize Imports | - | Runs on save automatically |
| Run Task | `Ctrl+Shift+P` → Tasks | Access all tasks |
| Show Problems | `Ctrl+Shift+M` | View all problems |

---

## Configuration Files

The auto-fix system uses these configuration files:

- **`.vscode/settings.json`** - VS Code auto-fix on save
- **`.vscode/tasks.json`** - Quick tasks definition
- **`.pre-commit-config.yaml`** - Pre-commit hooks
- **`pyproject.toml`** - Ruff, Black, mypy configuration
- **`scripts/autofix.py`** - Comprehensive auto-fix script

---

## Troubleshooting

### Auto-fix Not Working on Save

1. **Check extension installation:**
   - Open Extensions panel (`Ctrl+Shift+X`)
   - Install "Ruff" extension
   - Install "Python" extension

2. **Check Python interpreter:**
   - Click on Python version in bottom status bar
   - Select your virtual environment

3. **Check settings:**
   - Open settings (`Ctrl+,`)
   - Search for "format on save"
   - Ensure it's enabled

### Pre-commit Hooks Failing

1. **Install pre-commit:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Update hooks:**
   ```bash
   pre-commit autoupdate
   pre-commit run --all-files
   ```

3. **Check hook versions:**
   - Review `.pre-commit-config.yaml`
   - Ensure all repos are accessible

### Auto-fix Script Errors

1. **Install dependencies:**
   ```bash
   pip install -e .[dev]
   ```

2. **Check Python version:**
   ```bash
   python --version  # Should be 3.11+
   ```

3. **Run steps individually:**
   ```bash
   ruff check . --fix
   ruff format .
   black .
   pytest -v
   ```

---

## Best Practices

### Do's ✅

- **Save frequently** - Auto-fix runs on every save
- **Review changes** - Always check `git diff` before committing
- **Run tests** - Ensure auto-fix didn't break anything
- **Use tasks** - Quick access to all auto-fix operations
- **Keep tools updated** - Update Ruff, Black, mypy regularly

### Don'ts ❌

- **Don't disable auto-fix** without good reason
- **Don't commit** without running auto-fix first
- **Don't ignore** type checking warnings
- **Don't skip** pre-commit hooks
- **Don't force-commit** when hooks fail

---

## Advanced Usage

### Custom Auto-fix Rules

Edit `pyproject.toml` to customize Ruff rules:

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "C4"]
ignore = ["E501"]  # Ignore line length
```

### Disable Auto-fix for Specific Files

Add to `.ruff.toml` or `pyproject.toml`:

```toml
[tool.ruff]
exclude = ["migrations/*.py", "generated/*.py"]
```

### Run Auto-fix on CI

Add to `.github/workflows/ci.yml`:

```yaml
- name: Auto-fix
  run: python scripts/autofix.py
```

---

## Integration with AI Agents

The auto-fix system is designed to work seamlessly with AI coding agents:

1. **Agent makes changes** - AI modifies code
2. **Auto-fix runs** - On save or via task
3. **Tests verify** - Ensure nothing broke
4. **Agent reviews** - AI checks diff
5. **Auto-commit** - If using Git automation

---

## Summary

The auto-fix system provides multiple layers of automation:

- **Real-time** - Fixes on save
- **On-demand** - One-click tasks
- **Pre-commit** - Automatic before commit
- **Comprehensive** - Full workflow script

This ensures code quality is maintained automatically with minimal manual intervention.

---

## References

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [VS Code Python](https://code.visualstudio.com/docs/python/python-tutorial)

---

## Support

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review `docs/VSCODE_SETTINGS_GUIDE.md`
3. Check tool documentation (Ruff, Black, etc.)
4. Open an issue in the repository
