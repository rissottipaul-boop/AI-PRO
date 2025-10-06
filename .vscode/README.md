# VS Code Workspace Configuration

This directory contains shared VS Code settings for the autonomous-dev project.

## Files

- **settings.json** - Git automation, Python, formatting, and editor settings
- **tasks.json** - Common development tasks (build, test, lint, format)
- **extensions.json** - Recommended extensions for this project
- **launch.json** - Debug configurations for Python code and tests

## Quick Start

1. **Open this workspace in VS Code**
   - VS Code will prompt to install recommended extensions
   - Click "Install All" to get the full development experience

2. **Key Features Enabled:**
   - ✅ Auto-fetch from Git every 3 minutes
   - ✅ Auto-format on save (Ruff)
   - ✅ Smart commit (commit all if none staged)
   - ✅ Auto-sync after commit
   - ✅ Organize imports on save
   - ✅ Pytest integration
   - ✅ Type checking with mypy

3. **Useful Shortcuts:**
   - `Ctrl+Shift+B` - Run Full CI Check (default build)
   - `Ctrl+Shift+T` - Run Tests (default test)
   - `F5` - Start debugging
   - `Ctrl+Shift+P` → "Tasks: Run Task" - See all available tasks

## Git Automation

The workspace is configured for maximum Git automation:

```json
{
    "git.autofetch": true,           // Fetch every 3 minutes
    "git.enableSmartCommit": true,   // Commit all if none staged
    "git.confirmSync": false,        // No sync confirmation
    "git.postCommitCommand": "sync"  // Auto-push after commit
}
```

**Workflow:**
1. Edit files → Auto-format on save
2. Commit via Source Control panel
3. Automatically pushed to remote
4. Auto-fetch keeps you updated

## Tasks

Run common tasks via Command Palette or keyboard shortcuts:

| Task | Description | Shortcut |
|------|-------------|----------|
| Full CI Check | Lint + format + type check + test | `Ctrl+Shift+B` |
| Run Tests | Execute pytest with coverage | `Ctrl+Shift+T` |
| Pre-commit Run All | Validate all files | - |
| Lint (Ruff) | Check and fix code issues | - |
| Format | Format code with Ruff/Black | - |
| Type Check | Run mypy type checker | - |

## Documentation

For detailed documentation, see:
- [VS Code Settings Guide](../docs/VSCODE_SETTINGS_GUIDE.md) - Complete guide to settings and recovery

## Troubleshooting

### Pre-commit hooks fail

If pre-commit hooks modify files:
```bash
git add .
git commit -m "your message"
```

### Tests not running

Check that:
1. Virtual environment is activated
2. Dependencies are installed: `pip install -e '.[dev]'`
3. `PYTHONPATH` includes `src` directory

### Extensions not loading

1. Reload window: `Ctrl+Shift+P` → "Reload Window"
2. Check extension compatibility
3. Review Output panel for errors
