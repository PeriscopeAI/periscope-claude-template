# Periscope Claude Workspace

A Claude Code workspace template for interacting with the **Periscope** Agentic Business Workflow Orchestration platform.

## Features

- **6 Specialized Agents** with focused MCP tool access
- **6 Skills (Slash Commands)** for common operations
- **160+ MCP Tools** organized by domain
- **Examples** for processes, agents, and workflows
- **Documentation** for quick reference

## Quick Start

1. **Clone/Copy this template**:
   ```bash
   cp -r periscope-claude-template ~/my-periscope-workspace
   cd ~/my-periscope-workspace
   ```

2. **Configure authentication**:
   ```bash
   export PERISCOPE_TOKEN="your-keycloak-token"
   ```

3. **Open with Claude Code**:
   ```bash
   claude
   ```

4. **Check platform status**:
   ```
   /status
   ```

## Available Skills

| Skill | Description |
|-------|-------------|
| `/process` | Design BPMN business processes |
| `/workflow` | Execute and monitor workflows |
| `/agent` | Create AI agents |
| `/task` | Manage human tasks |
| `/deploy` | Deploy processes to Temporal |
| `/status` | Check platform health |

## Agent Architecture

Each agent has access to specific MCP servers to minimize context usage:

| Agent | MCP Servers | Tools |
|-------|-------------|-------|
| workflow-operator | workflows, tasks | ~37 |
| process-designer | processes | ~25 |
| agent-manager | agents, mcp-servers | ~42 |
| task-handler | tasks, users | ~15 |
| integration-specialist | protocols, email, documents | ~48 |
| system-admin | system, users | ~8 |

## Directory Structure

```
periscope-claude-template/
├── CLAUDE.md                    # Main instructions
├── .mcp.json                    # MCP server configs
├── .claude/
│   ├── settings.json            # Claude Code settings
│   ├── agents/                  # 6 specialized agents
│   └── skills/                  # 6 slash commands
├── workspace/                   # Your work area
│   ├── processes/               # BPMN files
│   ├── agents/                  # Agent configs
│   └── workflows/               # Workflow templates
├── examples/                    # Sample configurations
└── docs/                        # Documentation
```

## Requirements

- Claude Code CLI
- Periscope platform running
- Keycloak authentication token

## Documentation

- [Getting Started](docs/getting-started.md)
- [MCP Tools Reference](docs/mcp-tools-reference.md)
- [Troubleshooting](docs/troubleshooting.md)

## License

Apache 2.0
