# Quick Reference: Auto-Fix All Problems

This is a quick reference guide for automatically fixing code issues in VS Code.

## 🚀 Quick Start

### Method 1: Automatic (No Action Needed)
Just save your file (`Ctrl+S`) - issues are fixed automatically!

### Method 2: One-Click Fix All
1. Press `Ctrl+Shift+P` (Command Palette)
2. Type "Tasks: Run Task"
3. Select **"Auto-Fix All Problems"**

### Method 3: Command Line
```bash
python scripts/autofix.py
```

---

## ✅ What Gets Fixed Automatically

When you **save a file** (`Ctrl+S`), these are fixed instantly:

- ✅ Code formatting (PEP 8)
- ✅ Import organization
- ✅ Unused imports removed
- ✅ Trailing whitespace removed
- ✅ Final newline added
- ✅ All linting issues (when auto-fixable)

---

## 📋 Available Tasks

| Task | What It Does | When to Use |
|------|--------------|-------------|
| **Auto-Fix All Problems** | Complete fix of all issues | Before committing, after major changes |
| **Fix All Issues** | Quick fix with pre-commit | Fast fix-all without full validation |
| **Lint (Ruff)** | Fix linting issues only | When you see linting errors |
| **Format (Ruff)** | Format code only | Quick formatting |
| **Full CI Check** | Fix + validate everything | Before pushing to Git |

### How to Run Tasks

**Option 1:** Command Palette
- Press `Ctrl+Shift+P`
- Type "Tasks: Run Task"
- Select the task

**Option 2:** Keyboard Shortcuts
- `Ctrl+Shift+B` - Full CI Check (default)
- `Ctrl+Shift+T` - Run Tests

---

## 🔧 Auto-Fix Script Usage

The comprehensive auto-fix script is at `scripts/autofix.py`.

### Run It
```bash
cd /path/to/AI-PRO
python scripts/autofix.py
```

### What It Does
1. ✅ Fixes all linting issues (Ruff)
2. ✅ Formats code (Ruff + Black)
3. ✅ Organizes imports
4. ✅ Runs pre-commit hooks
5. ✅ Checks types (mypy)
6. ✅ Runs tests to verify

### Output
```
🔧 Starting Comprehensive Auto-Fix Process
======================================================================
✅ Fixing linting issues with Ruff completed successfully
✅ Formatting code with Ruff completed successfully
...
📊 Auto-Fix Summary
✅ Successful steps: 7/7
🎉 All auto-fix operations completed successfully!
```

---

## 🐛 Common Issues & Solutions

### Pre-commit Hook Failed
**Problem:** `end-of-file-fixer` or `trailing-whitespace` modified files

**Solution:** Auto-fix settings prevent this. But if it happens:
```bash
git add .
git commit -m "your message"
```

### Some Issues Not Fixed
**Problem:** Type errors or complex issues remain

**Solution:** These require manual fixes. Click the lightbulb 💡 in VS Code for suggestions.

### Auto-fix Not Working
**Problem:** Save doesn't fix issues

**Solution:**
1. Reload VS Code: `Ctrl+Shift+P` → "Reload Window"
2. Check Ruff extension is installed
3. Run: `python scripts/autofix.py`

---

## 📚 Documentation

For complete details, see:

- **[AUTO_FIX_GUIDE.md](./AUTO_FIX_GUIDE.md)** - Complete auto-fix documentation (11KB)
- **[VSCODE_SETTINGS_GUIDE.md](./VSCODE_SETTINGS_GUIDE.md)** - VS Code settings guide
- **[GIT_VSCODE_AUTOMATION_SUMMARY.md](./GIT_VSCODE_AUTOMATION_SUMMARY.md)** - Implementation summary

---

## 🎯 Best Practices

### ✅ Do This
- Save files regularly (auto-fix runs on save)
- Run "Auto-Fix All Problems" before committing
- Review changes after auto-fix
- Trust the auto-fixes (they follow best practices)

### ❌ Avoid This
- Don't disable format-on-save
- Don't skip pre-commit hooks
- Don't ignore type errors (they won't auto-fix)
- Don't commit without testing

---

## 🎹 Keyboard Shortcuts

| Action | Shortcut | What It Does |
|--------|----------|--------------|
| Save & Auto-fix | `Ctrl+S` | Save and apply all auto-fixes |
| Format Document | `Shift+Alt+F` | Format current file |
| Organize Imports | `Shift+Alt+O` | Organize imports |
| Run Tasks | `Ctrl+Shift+P` | Open task menu |
| Full CI Check | `Ctrl+Shift+B` | Complete validation |

---

## 💡 Pro Tips

1. **Save Often** - Auto-fix runs on every save
2. **Use Tasks** - Quick access to comprehensive fixes
3. **Pre-commit** - Catches issues before commit
4. **Script** - Run `autofix.py` for thorough cleanup
5. **Review** - Always check what was fixed with `git diff`

---

**Last Updated:** December 2024  
**Status:** ✅ Fully Implemented and Tested
