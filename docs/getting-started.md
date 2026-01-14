# Getting Started with Periscope Claude Workspace

This guide will help you set up and start using the Periscope Claude workspace.

## Prerequisites

1. **Claude Code** installed and configured
2. **Periscope platform** running (see Platform Setup below)
3. **Authentication token** for MCP server access

## Platform Setup

### Option 1: Local Development

Start the Periscope platform locally:

```bash
# Clone the Periscope repository
git clone https://github.com/your-org/periscope.git
cd periscope

# Start services
./scripts/dev-services.sh -d

# Initialize database
./scripts/db/init.sh

# Initialize secrets
./scripts/init-secrets.sh
```

### Option 2: Connect to Existing Instance

Update `.mcp.json` with your Periscope instance URLs:

```json
{
  "mcpServers": {
    "periscope-workflows-dev": {
      "url": "https://your-periscope-instance.com/mcp/workflows"
    }
  }
}
```

## Authentication

### Get Your Token

1. Log into Keycloak at `http://keycloak.periscope.local:8080`
2. Navigate to your account settings
3. Generate an API token
4. Set the environment variable:

```bash
export PERISCOPE_TOKEN="your-token-here"
```

### Token in .env file

Create a `.env` file in this workspace:

```
PERISCOPE_TOKEN=your-token-here
```

## Verify Connection

Use the `/status` skill to verify your connection:

```
/status
```

This will check:
- Worker status
- Keycloak connection
- Service health

## Quick Start

### 1. Design a Process

Use the `/process` skill to design a business process:

```
/process

Create a simple approval workflow for expense reports
```

### 2. Deploy the Process

Use the `/deploy` skill to deploy:

```
/deploy

Deploy the expense approval process
```

### 3. Start a Workflow

Use the `/workflow` skill to execute:

```
/workflow

Start the expense approval workflow with amount 500
```

### 4. Complete Tasks

Use the `/task` skill to view and complete tasks:

```
/task

Show me my pending tasks
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

## Workspace Structure

```
workspace/
├── processes/    # Save your BPMN designs here
├── agents/       # Save agent configurations here
└── workflows/    # Save workflow templates here
```

## Examples

Check the `examples/` directory for:
- Sample BPMN processes
- Agent configurations
- Workflow templates

## Troubleshooting

### MCP Connection Failed

1. Verify Periscope services are running:
   ```bash
   docker compose -f docker/docker-compose.yml ps
   ```

2. Check your token is valid:
   ```bash
   curl -H "Authorization: Bearer $PERISCOPE_TOKEN" \
     http://localhost:8001/api/v1/health
   ```

3. Verify MCP server URLs in `.mcp.json`

### Permission Denied

Ensure your Keycloak user has the required roles:
- `workflow_operator` - For workflow operations
- `process_designer` - For process design
- `system_administrator` - For admin operations

### Workers Not Responding

Use `/status` to check worker health, then:
```
/status

Restart the workers if needed
```

## Next Steps

1. Explore the example processes in `examples/processes/`
2. Create your first AI agent with `/agent`
3. Design a custom workflow with `/process`
4. Read the MCP tools reference in `docs/mcp-tools-reference.md`
