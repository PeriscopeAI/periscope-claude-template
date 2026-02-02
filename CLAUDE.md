# Periscope Workspace

Transform your business processes into running workflows using natural language.

## The Fastest Way to Start

**Just describe what you want:**

```
/generate When a customer submits a support ticket, classify its urgency,
route to the right team, and escalate if not responded within 4 hours.
```

That's it. Periscope will create, deploy, and test your workflow automatically.

## All Commands

| Command | What It Does |
|---------|--------------|
| `/generate` | **Create a complete process from description** (start here!) |
| `/workflow` | Start, monitor, or manage running workflows |
| `/task` | View and complete tasks assigned to you |
| `/analyze` | Diagnose issues when something goes wrong |
| `/optimize` | Improve performance and reduce costs |
| `/status` | Check if everything is running |

### For Advanced Users

| Command | What It Does |
|---------|--------------|
| `/process` | Design BPMN processes manually |
| `/agent` | Create and configure AI agents |
| `/function` | Create Python script functions |
| `/deploy` | Deploy processes to Temporal |

## How It Works

```
Your Description → AI Understanding → Process Design → Auto-Deploy → Running Workflow
     ↑                                                                      │
     └──────────────── Analyze & Optimize ←─────────────────────────────────┘
```

**You focus on**: What your business needs
**AI handles**: BPMN, agents, functions, deployment, testing

## Example Workflows

### Expense Approval
```
/generate Expense approval where employees submit with receipts.
Under $100 auto-approve, $100-500 needs manager, over $500 needs finance.
Notify via Slack at each stage.
```

### Document Processing
```
/generate When invoices arrive by email, extract vendor and amount,
match against purchase orders, flag variances over 5% for review.
```

### Customer Onboarding
```
/generate Customer onboarding that collects documents, verifies identity,
sets up account, and schedules welcome call. Send progress emails.
```

### IT Ticket Triage
```
/generate IT support tickets classified by type and urgency, routed to
appropriate team, with escalation if no response in 2 hours.
```

## Your Workspace

```
workspace/
├── processes/    # Your process definitions (auto-generated)
├── agents/       # AI agent configurations (auto-generated)
└── workflows/    # Workflow templates and history

docs/
├── learnings/    # Session learnings and discoveries
├── known-issues.md  # Platform bugs and workarounds
└── *.md          # Reference documentation
```

## Capturing Learnings

**Important**: Document learnings to improve future interactions.

### When to Capture Learnings

- After completing a `/generate` workflow (successes and failures)
- When discovering a platform bug or workaround
- When finding a better pattern or approach
- When resolving a tricky issue

### How to Document

Create a timestamped file in `docs/learnings/`:
```
docs/learnings/YYYY-MM-DD-short-description.md
```

Use the template at `docs/learnings/_TEMPLATE.md`. Include:
- **Problem**: What was the challenge?
- **Solution**: How was it resolved?
- **How to Apply**: Steps for future use

### Update Known Issues

If a bug is found or resolved, update `docs/known-issues.md`:
- New bugs → Add with status "Open Bug"
- Resolved bugs → Mark as "RESOLVED" with solution

## What Periscope Uses

Behind the scenes:
- **Temporal** - Makes your workflows reliable and resumable
- **AI Agents** - Understand documents, make decisions, communicate
- **Script Functions** - Handle calculations and validations
- **BPMN** - Industry-standard process notation

You don't need to know any of this to use Periscope.

## Getting Help

- **Something not working?** → `/analyze [workflow-id]`
- **Want it faster/cheaper?** → `/optimize [process-name]`
- **Check system health** → `/status`
- **See examples** → Look in `examples/` folder

## Platform Connection

Your workspace connects to: `https://api.superagent.studio`

~69 MCP tools are available across 9 servers. Just describe what you need.
