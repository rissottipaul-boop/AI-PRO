# Agent-Specific Instructions

This directory contains specialized instructions for different AI agents that may work on this repository. Each agent should have its own subdirectory with an `instructions.md` file.

## Structure

```text
.github/agents/
├── README.md                    # This file
├── coding/
│   └── instructions.md          # Instructions for coding agents
├── review/
│   └── instructions.md          # Instructions for code review agents
└── documentation/
    └── instructions.md          # Instructions for documentation agents
```

## Usage

Agent-specific instructions in this directory extend and complement the general instructions in `.github/copilot-instructions.md`. When working on specific tasks:

1. **General instructions**: All agents should read `.github/copilot-instructions.md` first
2. **Specialized instructions**: Then read the relevant agent-specific instructions from this directory

## Creating New Agent Instructions

To add instructions for a new agent type:

1. Create a new subdirectory with the agent type name (e.g., `security/`, `testing/`)
2. Add an `instructions.md` file with specific guidance for that agent type
3. Ensure the instructions are consistent with the general instructions
4. Update this README to document the new agent type

## References

- [VS Code GitHub Copilot Custom Instructions](https://aka.ms/vscode-ghcp-custom-instructions)
- [General Repository Instructions](../copilot-instructions.md)
- [Automation Guide](../../AUTOMATION_GUIDE.md)
