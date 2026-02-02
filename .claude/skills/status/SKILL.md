---
name: status
description: Check Periscope platform health and system status
delegates-to: system-admin
---

# /status - Check Platform Status

Use this skill to check the health and status of the Periscope platform.

## What You Can Do

1. **System health** - Check overall platform status
2. **Worker status** - View Temporal worker health
3. **Service health** - Check individual services
4. **User status** - Verify Keycloak connection

## How to Use

Ask about platform status:

- "Check platform status"
- "Are the workers running?"
- "Is Keycloak connected?"
- "Show me the system health"

## Health Checks

### Worker Status
Shows all Temporal workers:
- Worker pools
- Running instances
- Task queues served
- Reachability

### Service Status
Individual service health:
- Agent Management (port 8002)
- Orchestration (port 8001)
- Keycloak (port 8080)
- Temporal (port 7233)

### Database Status
Database connectivity:
- periscope-db (PostgreSQL)
- temporal-db
- keycloak-db

## Status Indicators

| Status | Meaning |
|--------|---------|
| healthy | All systems operational |
| degraded | Some issues detected |
| unhealthy | Critical issues |
| unknown | Cannot determine status |

## Worker Information

```
Workers:
- orchestration-worker (port 9190)
  - Task queue: periscope-queue
  - Status: running
  - Instances: 3

- orchestration-worker-priority (port 9191)
  - Task queue: periscope-priority-queue
  - Status: running
  - Instances: 2
```

## Quick Diagnostics

### If Workers Are Down
```bash
docker compose -f docker/docker-compose.yml ps | grep worker
docker compose -f docker/docker-compose.yml logs orchestration-worker
```

### If Keycloak Is Down
```bash
docker compose -f docker/docker-compose.yml ps keycloak
docker compose -f docker/docker-compose.yml logs keycloak
```

### If Database Is Down
```bash
docker compose -f docker/docker-compose.yml ps periscope-db
docker compose -f docker/docker-compose.yml logs periscope-db
```

## Reference Documentation

- [Troubleshooting Guide](../../../docs/troubleshooting.md) - Common issues and fixes
- [Queues and Workers](../../../docs/queues-and-workers.md) - Task queue configuration

## Delegated Agent

This skill delegates to the **system-admin** agent which has access to:
- `periscope-system-dev` MCP server (3 tools)
- `periscope-users-dev` MCP server (5 tools)

**Note**: Some operations require `system_administrator` role.
