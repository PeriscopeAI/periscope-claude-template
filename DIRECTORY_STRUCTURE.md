# Periscope Claude Template - Directory Structure

This template provides a Claude Code workspace for interacting with the Periscope platform.

```
periscope-claude-template/
├── CLAUDE.md                          # Main instructions for Claude
├── .mcp.json                          # MCP server configurations
├── .claude/
│   ├── settings.json                  # Claude Code settings
│   │
│   ├── agents/                        # Specialized agents with focused tools
│   │   ├── workflow-operator.md       # Start, monitor, manage workflows
│   │   ├── process-designer.md        # Design BPMN processes
│   │   ├── agent-manager.md           # Create and execute AI agents
│   │   ├── task-handler.md            # Manage human tasks
│   │   ├── integration-specialist.md  # Protocols, email, documents
│   │   └── system-admin.md            # System administration
│   │
│   └── skills/                        # User-invocable skills (slash commands)
│       ├── process/
│       │   └── SKILL.md               # /process - Design new processes
│       ├── workflow/
│       │   └── SKILL.md               # /workflow - Execute workflows
│       ├── agent/
│       │   └── SKILL.md               # /agent - Create AI agents
│       ├── task/
│       │   └── SKILL.md               # /task - Manage human tasks
│       ├── deploy/
│       │   └── SKILL.md               # /deploy - Deploy processes
│       └── status/
│           └── SKILL.md               # /status - Check system status
│
├── workspace/                         # User workspace for designs
│   ├── processes/                     # BPMN process definitions
│   │   └── .gitkeep
│   ├── agents/                        # Agent configurations
│   │   └── .gitkeep
│   └── workflows/                     # Workflow templates
│       └── .gitkeep
│
├── examples/                          # Example configurations
│   ├── processes/
│   │   ├── approval-workflow.bpmn
│   │   └── document-processing.bpmn
│   ├── agents/
│   │   └── document-analyzer.json
│   └── workflows/
│       └── batch-processing.json
│
└── docs/                              # Quick reference documentation
    ├── getting-started.md
    ├── mcp-tools-reference.md
    └── troubleshooting.md
```

## Agent Responsibilities

| Agent | MCP Servers | Purpose |
|-------|-------------|---------|
| workflow-operator | workflows, tasks | Runtime workflow operations |
| process-designer | processes | BPMN design and deployment |
| agent-manager | agents, mcp-servers | AI agent lifecycle |
| task-handler | tasks, users | Human task management |
| integration-specialist | protocols, email, documents | Integration operations |
| system-admin | system, users | Administration |

## Skills (Slash Commands)

| Skill | Delegates To | Purpose |
|-------|--------------|---------|
| /process | process-designer | Design a new BPMN process |
| /workflow | workflow-operator | Start and manage workflows |
| /agent | agent-manager | Create and configure AI agents |
| /task | task-handler | View and complete human tasks |
| /deploy | process-designer | Deploy process to Temporal |
| /status | system-admin | Check platform health |
