# VSCode Setup Guide

This document describes the VSCode configuration for the autonomous-dev project.

## Overview

The project includes comprehensive VSCode configuration to provide an optimal development experience with AI-assisted coding through GitHub Copilot.

## Required Extensions

When you open this project in VSCode, you'll be prompted to install the following recommended extensions (defined in `.vscode/extensions.json`):

1. **GitHub Copilot** (`github.copilot`)
   - AI-powered code completion and generation
   - Automatically uses custom instructions from `.github/COPILOT_INSTRUCTIONS.md`

2. **GitHub Copilot Chat** (`github.copilot-chat`)
   - Interactive AI assistant for code discussions and explanations
   - Context-aware code generation

3. **Ruff** (`charliermarsh.ruff`)
   - Fast Python linter and formatter
   - Replaces flake8, isort, and other tools

4. **Python** (`ms-python.python`)
   - Core Python language support
   - Test discovery and execution

5. **Pylance** (`ms-python.vscode-pylance`)
   - Fast type checking and IntelliSense
   - Strict mode enabled for this project

## GitHub Copilot Custom Instructions

### What are Custom Instructions?

Custom instructions allow you to define project-specific rules and guidelines that GitHub Copilot follows when generating code. This ensures consistency with your project's coding standards, architecture decisions, and security requirements.

### Implementation

This project uses **instruction files** instead of workspace settings, following Microsoft's recommended approach (see [documentation](https://aka.ms/vscode-ghcp-custom-instructions)).

**Configuration in `.vscode/settings.json`:**

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "file": ".github/COPILOT_INSTRUCTIONS.md"
    }
  ]
}
```

### What's Included

The `.github/COPILOT_INSTRUCTIONS.md` file contains:

- **Core Principles**: Predictability, test-first development, minimal changes
- **Repository Context**: Python 3.11+, tooling, quality standards
- **Tooling Contract**: Pre-commit hooks, test coverage requirements
- **Allowed/Forbidden Changes**: Clear boundaries for AI agent
- **Commit Conventions**: Conventional Commits standard
- **Branch Naming**: Consistent naming scheme
- **Workflow**: Complete autonomous development cycle
- **PR Checklist**: Requirements for every pull request
- **Quality Standards**: Coverage, linting, type safety, security
- **Automation Policy**: Auto-merge rules and review requirements

### Benefits

- **Consistency**: All code generated follows the same standards
- **Safety**: Multiple validation layers prevent breaking changes
- **Efficiency**: AI understands project constraints without repeated prompts
- **Quality**: Automatic adherence to testing, security, and style requirements

## Python Configuration

### Type Checking

The project uses **strict type checking** with mypy:

```json
{
  "python.analysis.typeCheckingMode": "strict"
}
```

All public functions must have type hints.

### Testing

Pytest is configured as the default test framework:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"]
}
```

Run tests through:
- Test Explorer in VSCode
- Command Palette: `Python: Run All Tests`
- Tasks (see below)

### Formatting and Linting

Ruff is configured as the default formatter:

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  }
}
```

Code is automatically formatted on save, with import organization.

## Available Tasks

Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) and select `Tasks: Run Task` to access:

### Build Tasks

- **Run All Checks** (default): Runs pre-commit hooks + tests with coverage
- **Lint**: Runs ruff and mypy
- **Pre-commit**: Runs all pre-commit hooks

### Test Tasks

- **Run Tests** (default): Runs pytest
- **Run Tests with Coverage**: Runs pytest with coverage report

### Other Tasks

- **Install Dependencies**: Installs development dependencies
- **Format**: Formats code with ruff

### Keyboard Shortcuts

- Build (default task): `Ctrl+Shift+B` (or `Cmd+Shift+B`)
- Test (default task): Uses Test Explorer

## Debug Configuration

The project includes debug configurations in `.vscode/launch.json`:

1. **Python: Current File**
   - Debug the currently open Python file

2. **Python: Pytest Current File**
   - Debug tests in the current file

3. **Python: Pytest All**
   - Debug all tests in the project

Set breakpoints and press `F5` to start debugging.

## File Exclusions

The following are excluded from the file explorer to reduce clutter:

- `**/__pycache__`
- `**/*.pyc`
- `**/.pytest_cache`
- `**/.mypy_cache`
- `**/.ruff_cache`
- `**/*.egg-info`

## Virtual Environment

The default Python interpreter path is configured to use the local virtual environment:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

Create and activate the virtual environment:

**Linux/macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

VSCode will automatically detect and use this environment.

## Editor Configuration

### Line Length

The editor is configured with a ruler at 100 characters to match the project's line length limit:

```json
{
  "editor.rulers": [100]
}
```

### Format on Save

Code is automatically formatted when you save a file:

```json
{
  "editor.formatOnSave": true
}
```

## Troubleshooting

### Copilot Not Using Custom Instructions

1. Ensure you have the latest version of GitHub Copilot extension
2. Reload VSCode window (`Ctrl+Shift+P` → `Developer: Reload Window`)
3. Check that `.github/COPILOT_INSTRUCTIONS.md` exists and is accessible
4. Verify your GitHub Copilot subscription is active

### Python Extension Not Finding Interpreter

1. Open Command Palette (`Ctrl+Shift+P`)
2. Select `Python: Select Interpreter`
3. Choose the interpreter in `.venv` directory
4. If not listed, click "Enter interpreter path" and browse to `.venv/bin/python`

### Tests Not Discovered

1. Ensure pytest is installed: `pip install -e .[dev]`
2. Check that `python.testing.pytestEnabled` is `true` in settings
3. Reload window or restart VSCode
4. Check Output panel → Python Test Log for errors

### Ruff Not Working

1. Install the Ruff extension from the Extensions marketplace
2. Ensure `charliermarsh.ruff` is in extensions.json recommendations
3. Check that Ruff is installed: `pip install ruff`
4. Reload VSCode window

## Best Practices

### 1. Use Tasks for Common Operations

Instead of running commands in terminal, use VSCode tasks:
- Consistent execution environment
- Integrated problem matching
- Keyboard shortcuts

### 2. Leverage GitHub Copilot

The custom instructions ensure Copilot generates code that:
- Follows project conventions
- Includes appropriate tests
- Meets quality standards
- Adheres to security requirements

### 3. Watch the Problems Panel

The Problems panel (`Ctrl+Shift+M`) shows:
- Linting errors (Ruff)
- Type errors (Pylance/mypy)
- Test failures

Fix issues as they appear to maintain code quality.

### 4. Use Test Explorer

The Test Explorer (beaker icon in sidebar) provides:
- Visual test discovery
- One-click test execution
- Integrated test results
- Debug test capabilities

### 5. Format and Lint Before Commit

While pre-commit hooks will catch issues, it's faster to:
1. Enable format on save (already configured)
2. Run the "Lint" task before committing
3. Use the "Run All Checks" task before pushing

## References

- [VSCode Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [GitHub Copilot Custom Instructions](https://aka.ms/vscode-ghcp-custom-instructions)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)

---

**Status:** ✅ Complete and operational  
**Last Updated:** 2025-10-04
