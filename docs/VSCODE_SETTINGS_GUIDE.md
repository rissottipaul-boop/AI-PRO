# VS Code Settings Guide

This guide explains the VS Code workspace settings and how they enable automatic problem-solving and Git synchronization.

## Overview

The `.vscode/` directory contains configuration files that automate common development tasks, fix code issues, and manage Git operations without manual intervention.

## Directory Structure

```
.vscode/
├── settings.json        # Workspace settings (main configuration)
├── tasks.json          # Quick tasks for common operations
├── extensions.json     # Recommended extensions
├── launch.json         # Debug configurations
└── README.md           # Quick reference
```

### Core Files

#### 1. `settings.json` - Workspace Settings
Contains all workspace-specific settings including Git automation, Python configuration, and editor preferences.

**Key Git Automation Settings:**
```json
{
    "git.autofetch": true,              // Auto-fetch every 3 minutes
    "git.autofetchPeriod": 180,         // Fetch interval in seconds
    "git.enableSmartCommit": true,      // Commit all changes if none staged
    "git.confirmSync": false,           // No confirmation for sync
    "git.pruneOnFetch": true,           // Clean up deleted remote branches
    "git.pullTags": true,               // Pull tags automatically
    "git.postCommitCommand": "sync",    // Auto push after commit
    "git.fetchOnPull": true             // Fetch before pull
}
```

**Python & Formatting:**
- Auto-format on save with Ruff
- Organize imports automatically
- Type checking enabled
- Test discovery configured for pytest

**File Management:**
- Trim trailing whitespace on save
- Insert final newline on save
- Normalize line endings to LF (Unix)

#### 2. `tasks.json` - Task Definitions

Quick-access tasks via Command Palette (`Ctrl+Shift+P`):

| Task | Shortcut | Description |
|------|----------|-------------|
| Auto-Fix All Problems | `Ctrl+Shift+B` | Comprehensive auto-fix |
| Run Tests | Test Task | Run pytest with coverage |
| Lint with Ruff | - | Fix linting issues |
| Format with Ruff | - | Format all code |
| Type Check with mypy | - | Check types |
| Run Pre-commit Hooks | - | Run all hooks |
| Install Dev Dependencies | - | Install requirements |
| Clean Cache Files | - | Remove __pycache__, etc. |

#### 3. `extensions.json` - Recommended Extensions

Essential extensions for the best experience:

**Python Development:**
- ms-python.python
- ms-python.vscode-pylance
- charliermarsh.ruff
- ms-python.mypy-type-checker

**Git:**
- eamodio.gitlens
- mhutchie.git-graph

**Code Quality:**
- streetsidesoftware.code-spell-checker
- EditorConfig.EditorConfig

**Other:**
- GitHub.copilot
- GitHub.vscode-pull-request-github

#### 4. `launch.json` - Debug Configurations

Pre-configured debug setups:
- Debug current Python file
- Debug Python module
- Debug current test file
- Debug all tests with coverage

Press `F5` to start debugging with the appropriate configuration.

---

## Git Automation Workflow

### How It Works

1. **Auto-fetch** - VS Code fetches changes from remote every 3 minutes
2. **Smart Commit** - If no files are staged, commit all changes
3. **Post-commit Sync** - Automatically push after commit
4. **No Confirmations** - Sync happens without prompts

### Workflow Example

```bash
# 1. Make changes to files
# 2. Save files (auto-formatted on save)
# 3. Commit via Source Control panel or Ctrl+Enter
# 4. VS Code automatically pushes the commit
# 5. Every 3 minutes, VS Code fetches latest changes
```

### Manual Controls

Despite automation, you can still:
- Stage specific files manually
- Review changes before commit
- Use Git commands in terminal
- Pause sync temporarily via Source Control menu

### Safety Features

- **No force push** - Force push is disabled for safety
- **Push notifications** - Success notifications enabled
- **Rebase disabled** - Uses merge instead of rebase by default
- **Review before commit** - You still control when to commit

---

## Auto-Fix Capabilities

### On Save (Automatic)

When you save a Python file:

1. **Ruff linting** - Fixes common issues
2. **Code formatting** - Applies consistent style
3. **Import organization** - Sorts and cleans imports
4. **Whitespace trimming** - Removes trailing spaces
5. **EOF newline** - Ensures final newline

### Manual Trigger

**Keyboard Shortcut:**
- Press `Ctrl+Shift+B` - Runs comprehensive auto-fix

**Command Palette:**
- `Ctrl+Shift+P` → "Tasks: Run Task" → "Auto-Fix All Problems"

**Terminal:**
```bash
python scripts/autofix.py
```

### What Gets Fixed

- Linting errors (Ruff)
- Code formatting (Ruff, Black)
- Import organization
- Trailing whitespace
- Missing newlines
- Mixed line endings
- Pre-commit hook issues

---

## Python Development Settings

### Code Quality

**Linting:**
- Primary linter: Ruff (fast, comprehensive)
- Runs on save automatically
- Auto-fix enabled for most issues

**Formatting:**
- Primary formatter: Ruff
- Backup formatter: Black
- Line length: 100 characters
- Target Python: 3.11+

**Type Checking:**
- Tool: mypy
- Mode: Basic (configurable)
- Configuration: `pyproject.toml`

### Testing

**Framework:** pytest
**Coverage:** Enabled with 85% minimum
**Auto-discovery:** Tests in `tests/` directory
**Run via:**
- Test Explorer panel
- Tasks: "Run Tests"
- Terminal: `pytest -v`

### Environment

**Python Path:**
- Auto-configured for `src/` directory
- Virtual environment auto-activation
- PYTHONPATH includes `src/`

---

## Editor Preferences

### Code Editing

```json
{
    "editor.formatOnSave": true,        // Format on save
    "editor.rulers": [100],             // Line length guide
    "editor.tabSize": 4,                // Tab = 4 spaces
    "editor.insertSpaces": true,        // Use spaces, not tabs
    "editor.trimAutoWhitespace": true   // Trim whitespace
}
```

### File Handling

```json
{
    "files.trimTrailingWhitespace": true,  // Remove trailing spaces
    "files.insertFinalNewline": true,      // Add final newline
    "files.eol": "\n",                     // Unix line endings (LF)
    "files.encoding": "utf8"               // UTF-8 encoding
}
```

### Search & Visibility

Hidden from search and explorer:
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `.coverage`
- `htmlcov/`

---

## Customization

### Project-Specific Settings

Edit `.vscode/settings.json` to customize for your needs:

**Disable auto-sync:**
```json
{
    "git.confirmSync": true,  // Enable confirmation
    "git.postCommitCommand": "none"  // Disable auto-push
}
```

**Change line length:**
```json
{
    "editor.rulers": [88],  // Black's default
    "[python]": {
        "editor.rulers": [88]
    }
}
```

**Adjust auto-fetch interval:**
```json
{
    "git.autofetchPeriod": 300  // 5 minutes instead of 3
}
```

### User-Specific Settings

For personal preferences that shouldn't be committed:
- Use User Settings (`Ctrl+,`)
- Settings: `File > Preferences > Settings`
- User tab (not Workspace)

---

## Best Practices

### Git Automation

✅ **Do:**
- Review changes before committing (even with auto-sync)
- Use meaningful commit messages
- Keep commits small and focused
- Enable auto-stash if using rebase workflows

❌ **Don't:**
- Commit sensitive data (use .gitignore)
- Disable confirmations without understanding implications
- Auto-push to production branches without review

### Settings Management

✅ **Do:**
- Commit `.vscode/` to repository for team consistency
- Document workspace-specific settings
- Use workspace settings for project preferences
- Keep user settings for personal preferences

❌ **Don't:**
- Store credentials in settings.json
- Override critical safety settings
- Commit user-specific paths or tokens

### Extension Management

✅ **Do:**
- Install recommended extensions
- Keep extensions updated
- Disable unused extensions
- Review extension permissions

❌ **Don't:**
- Install unverified extensions
- Grant excessive permissions
- Ignore security warnings

---

## Troubleshooting

### Git Issues

**Problem: Auto-push fails**
- Check Git credentials are configured
- Ensure you have push access to remote
- Verify network connectivity
- Check Output panel: "Git" for errors

**Problem: Auto-fetch not working**
- Verify `git.autofetch` is `true`
- Check `git.autofetchPeriod` value
- Look for errors in Output: "Git"

### Auto-Fix Issues

**Problem: Format on save not working**
- Install Ruff extension
- Select Python interpreter
- Check settings.json syntax
- Restart VS Code

**Problem: Import organization fails**
- Ensure Ruff extension is active
- Check for syntax errors in file
- Verify `ruff.organizeImports` is `true`

### Extension Issues

**Problem: Recommended extensions not showing**
- Open Extensions panel (`Ctrl+Shift+X`)
- Look for "Recommended" section
- Click "Show Recommendations"

**Problem: Extension conflicts**
- Disable conflicting extensions (e.g., multiple formatters)
- Keep only one Python linter active
- Restart VS Code after changes

---

## Advanced Configuration

### Multiple Python Versions

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.pythonPath": "${workspaceFolder}/.venv/bin/python"
}
```

### Custom Tasks

Add to `.vscode/tasks.json`:

```json
{
    "label": "My Custom Task",
    "type": "shell",
    "command": "python",
    "args": ["my_script.py"],
    "group": "build"
}
```

### Workspace vs User Settings

**Workspace Settings** (`.vscode/settings.json`):
- Project-specific
- Shared with team
- Committed to repository

**User Settings**:
- Personal preferences
- Not committed
- Apply to all projects

  - **Linux:** `~/.config/Code/User/settings.json`
  - **Windows:** `%APPDATA%\Code\User\settings.json`
  - **macOS:** `~/Library/Application Support/Code/User/settings.json`
---

## Keyboard Shortcuts Reference

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+B` | Run Auto-Fix All Problems |
| `Ctrl+S` | Save & auto-fix current file |
| `Ctrl+Shift+P` | Command Palette (all tasks) |
| `F5` | Start Debugging |
| `Ctrl+\`` | Toggle Terminal |
| `Ctrl+Shift+M` | View Problems panel |
| `Ctrl+Shift+X` | Extensions panel |
| `Ctrl+,` | Open Settings |
| `Shift+Alt+F` | Format Document |

---

## Recovering Deleted Settings

If you accidentally delete settings, you can recover from Settings Sync snapshots:

### Recovery Steps

1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "Settings Sync: Show Synced Data"
3. Browse available snapshots
4. Restore desired version

### Cloud Sync Recovery

If Settings Sync is enabled:
1. Go to Settings Sync: Turn On
2. Select "Merge" or "Replace Local"
3. Choose snapshot to restore

### Manual Recovery

From the local sync folder:
- Windows: `%APPDATA%\Code\User\syncLocalSettings\`
- Linux: `~/.config/Code/User/syncLocalSettings/`
- macOS: `~/Library/Application Support/Code/User/syncLocalSettings/`

Look for `lastSyncsettings.json` and other backup files.

---

## Integration with CI/CD

The workspace settings complement CI/CD workflows:

**Local (VS Code):**
- Auto-fix on save
- Quick tasks for testing
- Git automation

**Remote (GitHub Actions):**
- Same linting rules (Ruff)
- Same formatting (Black)
- Same type checking (mypy)
- Same test configuration (pytest)

This ensures consistency between local development and CI.

---

## Security Considerations

### Credentials

Never store in settings.json:
- API keys
- Passwords
- Tokens
- Private keys

Use environment variables or `.env` files (excluded from Git).

### Extension Security

- Only install verified extensions
- Review extension permissions
- Keep extensions updated
- Disable unused extensions

### Git Security

- Don't disable gitleaks pre-commit hook
- Review commits before auto-push
- Use SSH keys instead of passwords
- Enable 2FA on GitHub

---

## Additional Resources

- [Auto-Fix Guide](./AUTO_FIX_GUIDE.md) - Detailed auto-fix documentation
- [Git & VS Code Automation Summary](./GIT_VSCODE_AUTOMATION_SUMMARY.md) - Implementation details
- [VS Code Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

---

## Feedback

If you have suggestions for improving these settings:
1. Test your changes locally
2. Document the benefits
3. Submit a pull request
4. Update this guide accordingly
