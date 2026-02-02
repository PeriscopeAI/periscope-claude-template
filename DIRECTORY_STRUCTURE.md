# Periscope Claude Template - Directory Structure

A Claude Code workspace for transforming natural language into running business workflows.

```
periscope-claude-template/
├── CLAUDE.md                          # Quick reference for users
├── .mcp.json                          # Platform connection (160+ tools)
├── .claude/
│   ├── settings.json                  # Claude Code settings
│   │
│   ├── agents/                        # AI agents with focused capabilities
│   │   ├── process-generator.md       # Meta-agent: end-to-end process creation
│   │   ├── workflow-operator.md       # Execute and monitor workflows
│   │   ├── process-designer.md        # Manual BPMN design
│   │   ├── agent-manager.md           # AI agent configuration
│   │   ├── task-handler.md            # Human task management
│   │   ├── integration-specialist.md  # Protocols, email, documents
│   │   └── system-admin.md            # System administration
│   │
│   └── skills/                        # User commands (slash commands)
│       │
│       │  # PRIMARY - Start here
│       ├── generate/
│       │   └── SKILL.md               # /generate - Natural language to process
│       ├── workflow/
│       │   └── SKILL.md               # /workflow - Execute workflows
│       ├── task/
│       │   └── SKILL.md               # /task - Handle human tasks
│       │
│       │  # OPERATIONS - Manage running processes
│       ├── analyze/
│       │   └── SKILL.md               # /analyze - Diagnose issues
│       ├── optimize/
│       │   └── SKILL.md               # /optimize - Improve performance
│       ├── status/
│       │   └── SKILL.md               # /status - System health
│       │
│       │  # ADVANCED - For power users
│       ├── process/
│       │   └── SKILL.md               # /process - Manual BPMN design
│       ├── agent/
│       │   └── SKILL.md               # /agent - Configure AI agents
│       ├── function/
│       │   └── SKILL.md               # /function - Script functions
│       └── deploy/
│           └── SKILL.md               # /deploy - Manual deployment
│
├── workspace/                         # User's work area
│   ├── processes/                     # BPMN definitions (auto-generated)
│   │   └── .gitkeep
│   ├── agents/                        # Agent configs (auto-generated)
│   │   └── .gitkeep
│   └── workflows/                     # Templates and history
│       └── .gitkeep
│
├── examples/                          # Sample configurations
│   ├── processes/
│   │   ├── approval-workflow.bpmn
│   │   └── document-processing.bpmn
│   ├── agents/
│   │   └── document-analyzer.json
│   ├── functions/
│   │   └── expense-validator.py
│   └── workflows/
│       └── batch-processing.json
│
└── docs/                              # Help documentation
    ├── getting-started.md
    ├── mcp-tools-reference.md
    └── troubleshooting.md
```

## Skill Categories

### Primary Skills (Start Here)

| Skill | Purpose | Delegates To |
|-------|---------|--------------|
| `/generate` | Create complete process from description | process-generator |
| `/workflow` | Start and manage executions | workflow-operator |
| `/task` | Handle assigned tasks | task-handler |

### Operations Skills

| Skill | Purpose | Delegates To |
|-------|---------|--------------|
| `/analyze` | Diagnose failures | workflow-operator |
| `/optimize` | Improve performance | workflow-operator |
| `/status` | Check system health | system-admin |

### Advanced Skills

| Skill | Purpose | Delegates To |
|-------|---------|--------------|
| `/process` | Manual BPMN design | process-designer |
| `/agent` | Configure AI agents | agent-manager |
| `/function` | Create script functions | process-designer |
| `/deploy` | Manual deployment | process-designer |

## Agent Capabilities

| Agent | MCP Servers | What It Does |
|-------|-------------|--------------|
| process-generator | processes, agents, documents | Creates entire processes from natural language |
| workflow-operator | workflows, tasks | Runs workflows, monitors execution |
| process-designer | processes | Designs BPMN, validates, deploys |
| agent-manager | agents, mcp-servers | Manages AI agent lifecycle |
| task-handler | tasks, users | Handles human task interactions |
| integration-specialist | protocols, email, documents | Manages integrations |
| system-admin | system, users | Platform administration |

## User Journey

```
1. /generate "Create an expense approval workflow..."
   └── process-generator agent takes over
       ├── Understands requirements
       ├── Creates AI agents (if needed)
       ├── Creates functions (if needed)
       ├── Generates BPMN
       ├── Deploys to Temporal
       └── Runs test execution

2. /workflow start expense-approval {"amount": 500}
   └── workflow-operator agent takes over
       ├── Starts workflow
       ├── Returns workflow ID
       └── Workflow runs on Temporal

3. /task
   └── task-handler agent takes over
       ├── Shows pending tasks
       ├── User completes task
       └── Workflow continues

4. /analyze expense-approval
   └── workflow-operator agent takes over
       ├── Analyzes recent executions
       ├── Identifies issues
       └── Suggests improvements

5. /optimize expense-approval
   └── workflow-operator agent takes over
       ├── Analyzes performance
       ├── Suggests optimizations
       └── Applies improvements
```
