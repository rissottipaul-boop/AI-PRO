# VSCode Configuration

This directory contains Visual Studio Code workspace settings for the autonomous-dev project.

## Files

### `settings.json`

Workspace settings that configure:
- Python interpreter path (uses local `.venv`)
- Testing configuration (pytest with coverage)
- Linting (Ruff enabled)
- Formatting (Black as default formatter)
- Format on save enabled
- GitHub Copilot integration
- File exclusions for cleaner workspace

### `tasks.json`

Predefined tasks for common development operations:
- **Install Dependencies** - Install project dependencies with dev extras
- **Run Tests** (default test task) - Execute pytest with coverage
- **Run Lint** - Check code with Ruff and mypy
- **Format Code** - Auto-format with Ruff and Black
- **Pre-commit** - Run all pre-commit hooks
- **Run All Checks** (default build task) - Complete validation pipeline

Run tasks via: `Terminal > Run Task...` or `Ctrl+Shift+B` (default build task)

### `extensions.json`

Recommended VSCode extensions for this project:
- Python language support (Pylance, Python)
- Formatters (Black, Ruff)
- Type checking (mypy)
- GitHub Copilot and Copilot Chat
- Markdown support
- EditorConfig support

VSCode will prompt to install these extensions when opening the workspace.

## GitHub Copilot Instructions

This project uses GitHub Copilot custom instructions defined in `.github/copilot-instructions.md`.

These instructions are automatically picked up by GitHub Copilot in VSCode and provide context about:
- Project structure and conventions
- Code quality standards
- Testing requirements
- Security policies
- Commit message conventions
- Workflow guidelines

For more information, see:
- [GitHub Copilot Custom Instructions](https://aka.ms/vscode-ghcp-custom-instructions)
- [Project Instructions](.github/copilot-instructions.md)

## Usage

1. Open the project in VSCode
2. Install recommended extensions when prompted
3. The settings will be automatically applied
4. Use `Ctrl+Shift+P` to access tasks
5. GitHub Copilot will use custom instructions automatically

## Customization

These settings are project-wide defaults. You can override them with user settings or workspace-specific settings in `.vscode/settings.local.json` (add to `.gitignore` if needed).
