# Troubleshooting Guide

Common issues and solutions when using the Periscope Claude workspace.

## Connection Issues

### MCP Server Connection Failed

**Symptom**: Tools fail with "connection refused" or "All connection attempts failed"

**Solutions**:

1. **Check services are running**:
   ```bash
   docker compose -f docker/docker-compose.yml ps
   ```

2. **Verify URLs in `.mcp.json`**:
   ```json
   {
     "mcpServers": {
       "periscope-workflows-dev": {
         "url": "http://localhost:8001/mcp/workflows"
       }
     }
   }
   ```

3. **Check your token**:
   ```bash
   echo $PERISCOPE_TOKEN
   ```

4. **Test connection manually**:
   ```bash
   curl -H "Authorization: Bearer $PERISCOPE_TOKEN" \
     http://localhost:8001/api/v1/health
   ```

### Authentication Failed (401/403)

**Symptom**: "Unauthorized" or "Forbidden" errors

**Solutions**:

1. **Verify token is set**:
   ```bash
   export PERISCOPE_TOKEN="your-token"
   ```

2. **Check token hasn't expired**:
   - Tokens typically expire after 1 hour
   - Regenerate from Keycloak

3. **Verify user has required roles**:
   - `workflow_operator`
   - `process_designer`
   - `system_administrator` (for admin ops)

---

## Workflow Issues

### Workflow Not Found

**Symptom**: 404 error when getting workflow status

**Solutions**:

1. **Use correct workflow_id**:
   - Use the full `workflow_id` from `create_workflow` response
   - Not the database `id`

2. **Check workflow hasn't been cleaned up**:
   - Temporal cleans up old workflows
   - Check Temporal UI for history

### Workflow Stuck

**Symptom**: Workflow stays in "running" state

**Solutions**:

1. **Check for pending human tasks**:
   ```
   /task
   Show tasks for workflow xyz
   ```

2. **Check for failed activities**:
   ```
   Use get_workflow_history to see events
   ```

3. **Check worker status**:
   ```
   /status
   ```

### New Workflow Not Available

**Symptom**: Deployed workflow returns "workflow not registered"

**Solutions**:

1. **Reload workflows**:
   ```
   /status
   Reload workflows
   ```

2. **Restart workers** (required for new workflows):
   ```
   /status
   Restart workers
   ```

---

## Process Issues

### BPMN Validation Failed

**Symptom**: `validate_bpmn` returns errors

**Common Causes**:

1. **Missing start event**:
   ```xml
   <bpmn:startEvent id="start">
     <bpmn:outgoing>flow1</bpmn:outgoing>
   </bpmn:startEvent>
   ```

2. **Missing end event**:
   ```xml
   <bpmn:endEvent id="end">
     <bpmn:incoming>flowN</bpmn:incoming>
   </bpmn:endEvent>
   ```

3. **Disconnected elements**:
   - All elements must have incoming/outgoing flows
   - Gateways must have proper branches

4. **Invalid XML syntax**:
   - Check for unclosed tags
   - Verify namespace declarations

### Deployment Failed

**Symptom**: `deploy_process` returns error

**Solutions**:

1. **Validate first**:
   ```
   Validate BPMN before deployment
   ```

2. **Check for unique process ID**:
   - Process IDs must be unique
   - Update or archive existing process

3. **Verify task queue exists**:
   - Default: `periscope-queue`
   - Workers must be listening

---

## Task Issues

### Task Not Visible

**Symptom**: `get_my_tasks` returns empty but tasks exist

**Solutions**:

1. **Check assignment**:
   - Tasks must be assigned to your user
   - Or you must be a candidate user

2. **Check filters**:
   ```
   get_my_tasks without status filter
   ```

3. **Check task status**:
   - Completed tasks won't show by default

### Cannot Complete Task

**Symptom**: `complete_task` returns 400 error

**Causes**:

1. **Task already completed**:
   - Check task status first

2. **Not assigned to you**:
   - Claim or get reassigned

3. **Invalid action**:
   - Use: approve, reject, submit, complete

---

## Agent Issues

### Agent Execution Failed

**Symptom**: `execute_agent` returns error

**Solutions**:

1. **Check API key configuration**:
   ```bash
   ./scripts/manage-secrets.sh --status ai
   ```

2. **Verify model provider**:
   - OpenAI: Requires OPENAI_API_KEY
   - Anthropic: Requires ANTHROPIC_API_KEY
   - Google: Requires GOOGLE_API_KEY

3. **Check agent exists**:
   ```
   List agents and verify ID
   ```

### MCP Server Not Connected

**Symptom**: Agent can't use MCP tools

**Solutions**:

1. **Check server assignment**:
   ```
   Get agent MCP servers
   ```

2. **Test server connection**:
   ```
   Test MCP server: server-id
   ```

3. **Reload servers**:
   ```
   Reload MCP servers
   ```

---

## System Issues

### Workers Not Responding

**Symptom**: `get_workers_status` shows workers unreachable

**Solutions**:

1. **Check Docker containers**:
   ```bash
   docker compose -f docker/docker-compose.yml ps | grep worker
   ```

2. **Check worker logs**:
   ```bash
   docker compose -f docker/docker-compose.yml logs orchestration-worker
   ```

3. **Restart workers**:
   ```bash
   docker compose -f docker/docker-compose.yml restart orchestration-worker
   ```

### Permission Denied (System Tools)

**Symptom**: 403 on system admin tools

**Solution**:
- Add `system_administrator` role in Keycloak
- Regenerate token after role change

---

## Common Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Bad Request | Check input parameters |
| 401 | Unauthorized | Check/refresh token |
| 403 | Forbidden | Check user roles |
| 404 | Not Found | Verify resource exists |
| 422 | Validation Error | Check request format |
| 500 | Server Error | Check service logs |
| 503 | Service Unavailable | Service is down |

---

## Getting Help

1. **Check logs**:
   ```bash
   docker compose -f docker/docker-compose.yml logs -f
   ```

2. **Use `/status`** to diagnose:
   ```
   /status
   ```

3. **Check Temporal UI**:
   - http://temporal-ui.periscope.local:8088

4. **Check Keycloak**:
   - http://keycloak.periscope.local:8080/admin
