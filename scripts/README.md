# Scripts Directory

Utility scripts for the AI-PRO project.

## Available Scripts

### autofix.py
**Purpose:** Comprehensive auto-fix for all code issues

**Usage:**
```bash
python scripts/autofix.py
```

**What it does:**
1. Fixes all linting issues with Ruff
2. Formats code with Ruff and Black
3. Organizes imports
4. Runs pre-commit hooks
5. Checks types with mypy
6. Runs tests to verify nothing broke

**When to use:**
- Before committing major changes
- After pulling updates
- When VS Code shows many problems
- As part of your daily workflow

**Output:**
- Detailed progress for each step
- Success/warning indicators
- Summary of operations
- Next steps guidance

---

### check_version.py
**Purpose:** Check and validate project version

**Usage:**
```bash
python scripts/check_version.py
```

---

### dev.ps1
**Purpose:** PowerShell development utilities (Windows)

**Usage:**
```powershell
.\scripts\dev.ps1
```

---

## Auto-Fix Integration

The `autofix.py` script is integrated with VS Code:

1. **Via Task:**
   - Press `Ctrl+Shift+P`
   - Select "Tasks: Run Task"
   - Select "Auto-Fix All Problems"

2. **Via Command Line:**
   ```bash
   python scripts/autofix.py
   ```

3. **Automatic:** Many fixes happen on save (see .vscode/settings.json)

For complete documentation, see [AUTO_FIX_GUIDE.md](../docs/AUTO_FIX_GUIDE.md).

---

## Development

To add new scripts:

1. Create Python script in this directory
2. Make it executable: `chmod +x scripts/your_script.py`
3. Add shebang: `#!/usr/bin/env python3`
4. Update this README
5. Consider adding a VS Code task in `.vscode/tasks.json`

---

**Last Updated:** December 2024
