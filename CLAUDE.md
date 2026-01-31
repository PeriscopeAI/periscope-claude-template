# Periscope Workspace

This workspace is configured for interacting with the **Periscope** Agentic Business Workflow Orchestration platform.

## Quick Start

Use these slash commands to interact with Periscope:

| Command | Description |
|---------|-------------|
| `/process` | Design a new BPMN business process |
| `/workflow` | Start, monitor, or manage workflow executions |
| `/agent` | Create and configure AI agents |
| `/function` | Create RestrictedPython script functions |
| `/task` | View and complete human tasks assigned to you |
| `/deploy` | Deploy a process to Temporal |
| `/analyze` | Diagnose failures and get optimization recommendations |
| `/status` | Check platform health and system status |

## Platform Overview

Periscope combines:
- **Temporal** - Durable workflow execution
- **BPMN-JS** - Visual process modeling
- **PydanticAI** - Type-safe AI agents
- **Multi-Protocol** - MCP, A2A, AG-UI communication

## Available Agents

This workspace uses specialized agents with focused tool access:

| Agent | Use For |
|-------|---------|
| `workflow-operator` | Start workflows, monitor execution, handle signals |
| `process-designer` | Create BPMN processes, validate, deploy |
| `process-generator` | **Meta-agent**: Create complete processes from natural language |
| `agent-manager` | Register AI agents, configure MCP servers |
| `task-handler` | Claim, complete, delegate human tasks |
| `integration-specialist` | Email, documents, protocol coordination |
| `system-admin` | Worker management, user administration |

**Tip**: Use `process-generator` when you want to create an entire workflow from a description. It will create all necessary agents, functions, BPMN, and deploy automatically.

## Workspace Structure

```
workspace/
├── processes/    # Your BPMN process definitions
├── agents/       # Your AI agent configurations
└── workflows/    # Your workflow templates
```

## MCP Server Endpoints

All services are available at `https://api.superagent.studio/mcp/`:

| Service | Endpoint | Tools |
|---------|----------|-------|
| Workflows | `/mcp/workflows` | 27 |
| Processes | `/mcp/processes` | 25 |
| Tasks | `/mcp/tasks` | 10 |
| Agents | `/mcp/agents-core` | 27 |
| MCP Servers | `/mcp/mcp-servers` | 15 |
| Protocols | `/mcp/protocols` | 28 |
| Email | `/mcp/email` | 5 |
| Documents | `/mcp/documents` | 15 |
| Users | `/mcp/users` | 5 |
| System | `/mcp/system` | 3 |

## Getting Help

- See `docs/getting-started.md` for setup instructions
- See `docs/mcp-tools-reference.md` for available tools
- See `examples/` for sample configurations
