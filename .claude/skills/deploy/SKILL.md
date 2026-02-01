---
name: deploy
description: Deploy processes to Temporal and manage deployments
delegates-to: process-designer
---

# /deploy - Deploy Processes

Use this skill to deploy BPMN processes to Temporal and manage workflow deployments.

## What You Can Do

1. **Deploy processes** - Deploy a process to Temporal
2. **List deployments** - View all active deployments
3. **Undeploy workflows** - Remove deployed workflows
4. **Redeploy workflows** - Update existing deployments
5. **Check health** - Verify deployment system status

## How to Use

Describe what you want to deploy:

- "Deploy the approval process"
- "List all deployed workflows"
- "Undeploy workflow xyz"
- "Redeploy the invoice processing workflow"
- "Check deployment health"

## Deployment Process

### 1. Validate First
Before deployment, validate your BPMN:
```
Validate BPMN: workspace/processes/my-process.bpmn
```

### 2. Deploy to Temporal
```
Deploy process: process-uuid
Workflow type: MyProcessWorkflow
Task queue: periscope-queue
```

### 3. Verify Deployment
```
Get deployment info: MyProcessWorkflow
```

### 4. Activate Workers (if new)
After deploying new workflows, workers need to be restarted:
```
1. Reload workflows (discovery)
2. Restart workers (activation)
```

## Deployment Configuration

| Option | Description | Default |
|--------|-------------|---------|
| task_queue | Temporal task queue | periscope-queue |
| workflow_type | Temporal workflow class | Auto-generated |
| auto_restart_workers | Restart workers after deploy | true |

## Task Queues

| Queue | Purpose |
|-------|---------|
| periscope-queue | Standard business workflows |
| periscope-ai-queue | AI agent workflows |
| periscope-priority-queue | High-priority workflows |

## Deployment Status

| Status | Description |
|--------|-------------|
| deployed | Active and running |
| pending | Waiting for worker restart |
| failed | Deployment failed |
| undeployed | Removed |

## Post-Deployment

After successful deployment:

1. **Start a workflow** - Use `/workflow` skill
2. **Monitor execution** - Check Temporal UI
3. **Handle tasks** - Use `/task` skill

## Delegated Agent

This skill delegates to the **process-designer** agent which has access to:
- `periscope-processes-dev` MCP server (29 tools)
- `periscope-context-dev` MCP server (5 tools)

The agent can also check worker status via coordination with system-admin.

## Deployment Statistics

Use `get_deployment_stats` to view:
- Total deployments
- Static vs generated workflows
- Deployment status counts
- Recent deployments
