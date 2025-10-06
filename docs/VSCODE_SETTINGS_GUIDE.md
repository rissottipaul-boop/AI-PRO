# VS Code Settings Guide

This document explains the VS Code configuration structure and how to use it for maximum automation.

## Directory Structure

The `.vscode/` directory contains workspace-specific settings that are shared across the team:

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

#### 2. `tasks.json` - Task Definitions
Predefined tasks for common development operations accessible via `Ctrl+Shift+B` or Command Palette.

**Available Tasks:**
- `Install Dependencies` - Install all dev dependencies
- `Run Tests` (default test task) - Run pytest
- `Run Tests with Coverage` - Full coverage report
- `Lint (Ruff)` - Run linter with auto-fix
- `Format (Ruff/Black)` - Format code
- `Type Check (mypy)` - Run type checker
- `Pre-commit Install` - Set up pre-commit hooks
- `Pre-commit Run All` - Validate all files
- `Security Audit` - Run pip-audit and bandit
- `Full CI Check` (default build task) - Complete validation

**Usage:**
- Press `Ctrl+Shift+B` to run default build task (Full CI Check)
- Press `Ctrl+Shift+T` to run default test task
- Open Command Palette (`Ctrl+Shift+P`) → "Tasks: Run Task"

#### 3. `extensions.json` - Recommended Extensions
Lists extensions that enhance the development experience.

**Core Extensions:**
- `ms-python.python` - Python language support
- `charliermarsh.ruff` - Fast Python linter/formatter
- `github.copilot` - AI pair programmer
- `eamodio.gitlens` - Enhanced Git integration
- `github.vscode-pull-request-github` - GitHub integration

**Installation:**
VS Code will prompt to install recommended extensions when opening the workspace.

#### 4. `launch.json` - Debug Configurations
Debug configurations for running and debugging Python code and tests.

**Available Configurations:**
- `Python: Current File` - Debug the currently open file
- `Python: Debug Tests` - Debug all tests
- `Python: Debug Specific Test` - Debug current test file
- `Python: Module` - Debug the main module

**Usage:**
- Press `F5` to start debugging with the default configuration
- Use Debug sidebar to select different configurations

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

## User Data Location

VS Code stores user-specific data in:

**Windows:**
```
%APPDATA%\Code
C:\Users\<username>\AppData\Roaming\Code
```

**macOS:**
```
~/Library/Application Support/Code
```

**Linux:**
```
~/.config/Code
```

### Key User Data Directories

#### `User/` Directory
Contains global user settings (not workspace-specific):

- `settings.json` - Global VS Code settings
- `keybindings.json` - Custom keyboard shortcuts
- `snippets/` - User-defined code snippets
- `globalStorage/` - Extension data (tokens, cache)
- `workspaceStorage/` - Per-workspace state
- `profiles/` - User profiles (if enabled)

#### `User/globalStorage/`
Extension-specific data:
- GitHub authentication tokens
- Extension settings and cache
- Language server data
- Telemetry state

#### `User/workspaceStorage/`
Workspace-specific state:
- Terminal history
- Editor layout
- Undo history
- Breakpoints
- Open files

#### Settings Sync Data

If Settings Sync is enabled (via GitHub/Microsoft account):

**Location:** `sync/` directory contains:
- `extensions/lastSyncextensions.json` - Extension list
- `settings/lastSyncsettings.json` - Settings snapshot
- `keybindings/lastSynckeybindings.json` - Keybindings
- `snippets/lastSyncsnippets.json` - Snippets
- `globalState/lastSyncglobalState.json` - Extension states

**Profile-specific sync:**
Each profile has its own subdirectory (e.g., `3d344ada/`) with the same structure.

### Cache Directories

- `CachedData/` - VS Code UI cache
- `Cache/`, `Code Cache/`, `GPUCache/` - Rendering cache
- `Logs/` - Diagnostic logs

## Recovering Deleted Settings

If you accidentally delete settings, you can recover from Settings Sync snapshots:

### Recovery Steps

1. **Close VS Code**

2. **Locate sync directory:**
   ```bash
   # Windows
   cd %APPDATA%\Code\User\sync

   # macOS/Linux
   cd ~/.config/Code/User/sync
   ```

3. **Extract settings:**
   ```bash
   # Settings
   cp settings/lastSyncsettings.json ../settings.json

   # Keybindings
   cp keybindings/lastSynckeybindings.json ../keybindings.json
   ```

4. **Restore extensions:**
   ```powershell
   # PowerShell
   $j = Get-Content sync\extensions\lastSyncextensions.json -Raw | ConvertFrom-Json
   $ids = $j.extensions | ForEach-Object { "$($_.identifier.publisher).$($_.identifier.extension)" }
   $ids | ForEach-Object { code --install-extension $_ }
   ```

5. **Restart VS Code**

### Cloud Sync Recovery

If you have Settings Sync enabled with GitHub/Microsoft account:

1. Open Command Palette (`Ctrl+Shift+P`)
2. Run "Settings Sync: Show Synced Data"
3. Review available backups
4. Download desired version

**Note:** Only the last synced version is stored locally. For history, enable cloud backup via Settings Sync.

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

## Troubleshooting

### Pre-commit Hook Issues

**Problem:** Files modified by hooks cause commit to fail

**Solution:**
```bash
# 1. Check which files were modified
git status

# 2. Add the modified files
git add <modified-files>

# 3. Commit again
git commit -m "your message"
```

**Common causes:**
- `end-of-file-fixer` adds missing newlines
- `trailing-whitespace` removes spaces
- Formatters modify code style

**Prevention:**
- Enable `files.insertFinalNewline` in VS Code
- Enable `files.trimTrailingWhitespace` in VS Code
- Run formatters before committing

### Auto-fetch Not Working

**Check:**
1. `git.autofetch` is `true` in settings
2. `git.autofetchPeriod` is set (default: 180 seconds)
3. Git credentials are configured correctly
4. No Git operations are currently running

### Tests Not Discovering

**Check:**
1. `python.testing.pytestEnabled` is `true`
2. `PYTHONPATH` includes `src` directory
3. Test files match `test_*.py` pattern
4. Virtual environment is activated

## Additional Resources

- [VS Code Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Git Integration](https://code.visualstudio.com/docs/sourcecontrol/overview)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

## Support

For issues or questions:
1. Check this guide
2. Review `.vscode/` configuration files
3. Check VS Code output panels
4. Review project documentation
5. Open an issue on GitHub
