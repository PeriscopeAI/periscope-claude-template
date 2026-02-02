# Periscope Claude Workspace

**From idea to running business process in minutes.**

A Claude Code workspace template for the **Periscope** Agentic Business Workflow Orchestration platform.

## What You Can Do

Describe a business process in plain English, and Periscope will:

1. **Understand** your requirements
2. **Design** the process flow
3. **Create** AI agents for intelligent tasks
4. **Deploy** to production
5. **Run** a test to verify it works

No coding. No configuration. Just describe what you need.

## Quick Start

1. **Open with Claude Code**:
   ```bash
   cd periscope-claude-workspace
   claude
   ```

2. **Create your first process**:
   ```
   /generate When a customer submits a refund request, check their
   order history, approve automatically if under $50 and good standing,
   otherwise route to customer service for review.
   ```

3. **Watch it deploy** - You'll see each step as the AI creates your workflow.

4. **Start using it**:
   ```
   /workflow start refund-request {"order_id": "12345", "reason": "defective"}
   ```

## Commands

### Primary (Start Here)

| Command | Purpose |
|---------|---------|
| `/generate` | Create a complete process from natural language |
| `/workflow` | Start and monitor workflow executions |
| `/task` | Handle tasks that need your attention |

### Operations

| Command | Purpose |
|---------|---------|
| `/analyze` | Diagnose problems and understand failures |
| `/optimize` | Improve speed and reduce costs |
| `/status` | Check platform health |

### Advanced (Optional)

| Command | Purpose |
|---------|---------|
| `/process` | Manually design BPMN processes |
| `/agent` | Configure AI agents directly |
| `/function` | Create Python script functions |
| `/deploy` | Manual deployment control |

## Example Processes

### Finance
```
/generate Invoice approval where amounts under $1000 auto-approve,
$1000-10000 needs manager, over $10000 needs CFO. Match against POs
and flag discrepancies.
```

### HR
```
/generate Employee onboarding that collects documents, runs background
check, provisions IT accounts, assigns buddy, and schedules orientation.
Track progress and notify HR if stuck.
```

### Operations
```
/generate Order fulfillment that validates inventory, processes payment,
assigns to warehouse, tracks shipping, and handles delivery confirmation.
Alert if any step takes too long.
```

### Customer Service
```
/generate Support ticket routing that classifies by type and urgency,
routes to specialists, escalates if no response in 2 hours, and surveys
customer after resolution.
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                        YOUR DESCRIPTION                              │
│  "When an invoice arrives, extract data, validate against PO..."    │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PERISCOPE AI AGENTS                            │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │ Understand  │→ │   Design    │→ │   Create    │                 │
│  │ Requirements│  │   Process   │  │ Components  │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│                                            │                         │
│                          ┌─────────────────┼─────────────────┐      │
│                          ▼                 ▼                 ▼      │
│                   ┌──────────┐      ┌──────────┐      ┌──────────┐ │
│                   │AI Agents │      │Functions │      │   BPMN   │ │
│                   └──────────┘      └──────────┘      └──────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      RUNNING WORKFLOW                                │
│                                                                      │
│  [Start] → [Extract] → [Validate] → [Decision] → [Approve/Review]  │
│                                                                      │
│  Deployed on Temporal • Self-healing • Observable • Optimizable     │
└─────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
periscope-claude-workspace/
├── CLAUDE.md                    # Quick reference
├── .mcp.json                    # Platform connection
├── .claude/
│   └── skills/                  # Available commands
│       ├── generate/            # /generate - create processes
│       ├── workflow/            # /workflow - execute
│       ├── task/                # /task - human tasks
│       ├── analyze/             # /analyze - diagnose
│       ├── optimize/            # /optimize - improve
│       └── ...
├── workspace/                   # Your work area
│   ├── processes/               # Generated BPMN (auto-managed)
│   ├── agents/                  # AI configurations (auto-managed)
│   └── workflows/               # Templates and history
├── examples/                    # Sample configurations
└── docs/                        # Help documentation
```

## Requirements

- Claude Code CLI
- Periscope platform access
- Authentication token (see docs/getting-started.md)

## What Periscope Creates For You

When you `/generate` a process, the platform automatically:

| Component | Purpose | You See |
|-----------|---------|---------|
| BPMN Process | Visual workflow definition | Diagram in dashboard |
| AI Agents | Handle intelligent tasks | "Extracting invoice data..." |
| Functions | Calculations, validations | Instant results |
| User Tasks | Human decision points | Items in your task list |
| Notifications | Slack, email updates | Messages when things happen |

## Documentation

- [Getting Started](docs/getting-started.md) - Setup and authentication
- [MCP Tools Reference](docs/mcp-tools-reference.md) - All available tools
- [Troubleshooting](docs/troubleshooting.md) - Common issues

## License

Apache 2.0
