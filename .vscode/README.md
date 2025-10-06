# VS Code Workspace Configuration

This directory contains VS Code workspace settings for the autonomous-dev project.

## Files

- **settings.json** - Workspace settings including Git automation, Python configuration, and auto-fix on save
- **tasks.json** - Quick tasks for common operations (auto-fix, test, lint, format)
- **extensions.json** - Recommended extensions for the best development experience
- **launch.json** - Debug configurations for Python files and tests

## Quick Start

### 1. Install Recommended Extensions

When you open this workspace, VS Code will prompt you to install recommended extensions. Click "Install All" to get the best experience.

### 2. Auto-Fix on Save

The workspace is configured to automatically:
- Fix linting issues on save
- Format code on save
- Organize imports on save
- Trim trailing whitespace
- Ensure final newline

### 3. Quick Tasks

Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and type "Tasks: Run Task" to access:

- **Auto-Fix All Problems** - Run comprehensive auto-fix script (Default Build Task: `Ctrl+Shift+B`)
- **Run Tests** - Run all tests with coverage (Default Test Task)
- **Lint with Ruff** - Check and fix linting issues
- **Format with Ruff** - Format all Python files
- **Type Check with mypy** - Run type checking
- **Run Pre-commit Hooks** - Run all pre-commit hooks

### 4. Git Automation

Git is configured for maximum automation:
- **Auto-fetch** every 3 minutes
- **Smart commit** - commits all changes if none are staged
- **Auto-sync** - automatically pushes after commit
- **No confirmation prompts** for sync operations

### 5. Debug Configurations

Press `F5` to start debugging with pre-configured setups:
- Debug current Python file
- Debug current test file
- Debug all tests

## Git Workflow

```bash
# 1. Make changes and save files (auto-formatted)
# 2. Stage files or let smart commit handle it
git add .

# 3. Commit (will auto-push)
git commit -m "Your message"

# 4. Changes are automatically pushed to remote
# 5. Background auto-fetch keeps you updated
```

## Keyboard Shortcuts

- `Ctrl+Shift+B` - Run Auto-Fix All Problems
- `F5` - Start Debugging
- `Ctrl+Shift+P` - Command Palette (access all tasks)
- `Ctrl+\`` - Toggle Terminal

## Troubleshooting

### Tests Not Running

Ensure dependencies are installed:
```bash
pip install -e .[dev]
```

### Auto-fix Not Working

1. Check that Ruff extension is installed
2. Verify Python interpreter is selected
3. Check Output panel for errors (View > Output > Ruff)

### Git Sync Issues

If auto-push fails:
1. Check your Git credentials
2. Ensure you have push access to the repository
3. Temporarily disable auto-sync in Source Control menu

## More Information

See detailed documentation in:
- `docs/VSCODE_SETTINGS_GUIDE.md` - Complete settings guide
- `docs/AUTO_FIX_GUIDE.md` - Auto-fix documentation
- `docs/GIT_VSCODE_AUTOMATION_SUMMARY.md` - Implementation details
