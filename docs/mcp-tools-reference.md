# MCP Tools Reference

This document provides a quick reference for all MCP tools available in the Periscope platform.

## Overview

| MCP Server | MCP Tools | REST-Only | Agent |
|------------|-----------|-----------|-------|
| periscope-workflows-dev | 18 | 9 | workflow-operator |
| periscope-processes-dev | 18 | 7 | process-designer |
| periscope-tasks-dev | ~11 | - | workflow-operator, task-handler |
| periscope-agents-core-dev | 15 | - | agent-manager |
| periscope-mcp-servers-dev | ~13 | - | agent-manager |
| periscope-script-functions-dev | 13 | - | integration-specialist |
| periscope-email-dev | ~5 | - | integration-specialist |
| periscope-users-dev | ~6 | - | task-handler, system-admin |
| periscope-system-dev | ~3 | - | system-admin |
| periscope-context-dev | 5 | - | all agents |

**Total: ~69 MCP tools** (REST-only tools remain accessible via HTTP API)

> **Note:** `periscope-protocols-dev` is currently disabled to reduce tool bloat. Protocol operations remain available via REST API.

---

## Workflow Tools (periscope-workflows-dev)

### MCP Tools (18)

#### Workflow Operations
| Tool | Description |
|------|-------------|
| `list_workflows` | List workflow executions |
| `create_workflow` | Start new workflow |
| `get_workflow_status` | Get workflow status |
| `signal_workflow` | Send signal to workflow |
| `get_workflow_history` | Get Temporal history |
| `validate_expression` | Validate gateway conditions |
| `search_workflows` | Search executions |

#### Scheduling
| Tool | Description |
|------|-------------|
| `schedule_workflow` | Schedule future execution |

#### Triggers
| Tool | Description |
|------|-------------|
| `list_signal_triggers` | List signal triggers |
| `list_message_triggers` | List message triggers |
| `trigger_workflow_by_signal` | Start by signal |
| `trigger_workflow_by_message` | Start by message |
| `webhook_trigger` | External webhook |

#### State Management
| Tool | Description |
|------|-------------|
| `get_workflow_state` | Get workflow state snapshot |
| `create_checkpoint` | Create state checkpoint |
| `get_state_history` | Get state transition history |
| `get_state_analytics` | Get state analytics |

### REST-Only Tools (9)

| Tool | Description | Reason |
|------|-------------|--------|
| `get_workflow_registry` | List registered workflow types | Admin/discovery |
| `delete_workflow` | Delete workflow execution | Destructive operation |
| `get_workflow_stats` | Get execution statistics | Admin analytics |
| `execute_batch_workflows` | Run multiple workflows | Complex operation |
| `get_batch_status` | Check batch progress | Accompanies batch |
| `cancel_scheduled_workflow` | Cancel scheduled | Destructive operation |
| `stream_workflow_status` | SSE streaming | Streaming endpoint |
| `restore_checkpoint` | Restore from checkpoint | State-modifying |
| `state_management_health` | Health check | Admin health check |

---

## Process Tools (periscope-processes-dev)

### MCP Tools (18)

#### File Upload (Token-Efficient - Recommended)
| Tool | Description |
|------|-------------|
| `request_bpmn_upload` | Get pre-signed URL for BPMN upload |
| `create_process_from_file_ref` | Create process from uploaded file |
| `update_process_from_file_ref` | Update process from uploaded file |

> **Token Efficiency**: Use file upload flow (~70 tokens) instead of inline BPMN (~250+ tokens) for large files.
> 1. Call `request_bpmn_upload` to get upload URL
> 2. Upload file directly to MinIO via pre-signed URL
> 3. Call `create_process_from_file_ref` with file_id

#### Process Operations
| Tool | Description |
|------|-------------|
| `list_processes` | List processes |
| `get_process` | Get process by ID |
| `get_process_bpmn` | Get BPMN XML |
| `archive_process` | Archive (soft delete) |
| `unarchive_process` | Restore archived |

#### Versions
| Tool | Description |
|------|-------------|
| `get_process_versions` | Version history |
| `get_process_version_detail` | Version details |

#### BPMN Operations
| Tool | Description |
|------|-------------|
| `validate_bpmn_from_file_ref` | Validate BPMN from uploaded file |
| `convert_bpmn_from_file_ref` | Convert from uploaded file |
| `get_async_conversion_status` | Check conversion |

#### Deployment
| Tool | Description |
|------|-------------|
| `deploy_process` | Deploy to Temporal |
| `get_process_deployments` | Get deployment history |
| `list_deployments` | List all deployments |
| `get_deployment_info` | Deployment details |
| `force_discovery_check` | Force discovery |
| `get_worker_status` | Worker status |
| `get_deployment_health` | Deployment health |

### REST-Only Tools (7)

| Tool | Description | Reason |
|------|-------------|--------|
| `create_process` | Create process (inline BPMN) | Token-inefficient |
| `update_process` | Update process (inline BPMN) | Token-inefficient |
| `validate_bpmn` | Validate inline BPMN XML | Token-inefficient |
| `convert_bpmn_process` | Convert inline BPMN | Token-inefficient |
| `get_process_stats` | Execution statistics | Admin analytics |
| `get_discovery_stats` | Discovery statistics | Admin analytics |
| `get_deployment_stats` | Deployment statistics | Admin analytics |
| `undeploy_workflow` | Remove deployment | Destructive operation |
| `redeploy_workflow` | Redeploy | Admin operation |

---

## Task Tools (periscope-tasks-dev)

### Discovery
| Tool | Description |
|------|-------------|
| `get_my_tasks` | Get assigned tasks |
| `get_task` | Get task by ID |
| `get_task_statistics` | Task counts |

### Operations
| Tool | Description |
|------|-------------|
| `claim_task` | Claim unassigned |
| `complete_task` | Complete task |
| `delegate_task` | Transfer task |
| `cancel_task` | Cancel task |

### Comments
| Tool | Description |
|------|-------------|
| `add_comment` | Add comment |
| `get_comments` | Get comments |

### Admin
| Tool | Description |
|------|-------------|
| `reassign_task` | Force reassign |

---

## Agent Tools (periscope-agents-core-dev)

### Lifecycle
| Tool | Description |
|------|-------------|
| `agents_health_check` | Service health |
| `list_agents` | List agents |
| `list_agents_enhanced` | List with filters |
| `register_agent` | Create basic agent |
| `create_agent_enhanced` | Create with config |
| `get_agent` | Get agent |
| `get_agent_enhanced` | Get with metrics |
| `update_agent_config` | Update config |
| `unregister_agent` | Delete agent |

### Execution
| Tool | Description |
|------|-------------|
| `execute_agent` | Execute agent |
| `execute_agent_enhanced` | Execute with tools |
| `stream_agent_response` | SSE streaming |
| `get_agent_statistics` | Execution stats |

### Prompts
| Tool | Description |
|------|-------------|
| `prompt_assist` | AI prompt help |
| `get_effective_prompt` | Get composed prompt |
| `get_prompt_templates` | List templates |

### Advanced
| Tool | Description |
|------|-------------|
| `select_optimal_model` | Dynamic selection |
| `discover_agents_by_capability` | Find agents |
| `coordinate_agents` | Multi-agent |
| `evaluate_agent_performance` | Performance eval |

---

## MCP Server Tools (periscope-mcp-servers-dev)

### Discovery
| Tool | Description |
|------|-------------|
| `list_mcp_servers` | List all servers |
| `list_available_mcp_servers` | List active |
| `health_check_all_servers` | Health check |
| `get_mcp_server_tools` | Get server tools |

### CRUD
| Tool | Description |
|------|-------------|
| `create_mcp_server` | Create server |
| `get_mcp_server` | Get server |
| `update_mcp_server` | Update server |
| `delete_mcp_server` | Delete server |
| `test_mcp_server` | Test connection |
| `reload_mcp_servers` | Hot reload |

### Assignments
| Tool | Description |
|------|-------------|
| `get_agent_mcp_servers` | Get agent servers |
| `update_agent_mcp_servers` | Assign servers |
| `populate_default_mcp_assignments` | Default assignments |

---

## Protocol Tools (periscope-protocols-dev) - DISABLED

> **Note:** This MCP server is currently disabled to reduce tool bloat for AI assistants. Protocol operations remain available via REST API at `http://localhost:8002/api/v1/protocols/`.

### A2A Coordination (REST-only)
| Tool | Description |
|------|-------------|
| `discover_a2a_agents` | Find agents |
| `delegate_task_between_agents` | Agent-to-agent |
| `get_coordination_statistics` | Stats |
| `list_coordination_tasks` | List tasks |
| `get_coordination_task` | Get task |
| `list_coordination_workflows` | List workflows |

### AG-UI (REST-only)
| Tool | Description |
|------|-------------|
| `stream_ag_ui_response` | SSE streaming |
| `get_session_info` | Session info |
| `pause_session` | Pause session |
| `resume_session` | Resume session |

### Routing (REST-only)
| Tool | Description |
|------|-------------|
| `route_protocol_message` | Route message |
| `get_protocol_capabilities` | Capabilities |
| `protocols_health_check` | Health check |

---

## Email Tools (periscope-email-dev)

| Tool | Description |
|------|-------------|
| `send_email` | Send custom email |
| `send_template_email` | Send templated |
| `list_templates` | List templates |
| `preview_template` | Preview |
| `email_health` | Health check |

---

## Script Functions Tools (periscope-script-functions-dev)

| Tool | Description |
|------|-------------|
| `create_function` | Create function |
| `list_functions` | List functions |
| `get_function` | Get function |
| `update_function` | Update function |
| `delete_function` | Delete function |
| `publish_version` | Publish version |
| `list_versions` | List versions |
| `get_version` | Get version |
| `test_function` | Test function |
| `test_code` | Test code |
| `validate_code` | Validate code |
| `get_function_stats` | Stats |
| `deprecate_function` | Deprecate |

---

## User Tools (periscope-users-dev)

| Tool | Description |
|------|-------------|
| `health_check` | Keycloak health |
| `search_users` | Search users |
| `get_user` | Get user |
| `get_user_display_name` | Display name |
| `refresh_user` | Refresh cache |

---

## System Tools (periscope-system-dev)

| Tool | Description |
|------|-------------|
| `get_workers_status` | Worker status |
| `reload_workflows` | Reload discovery |
| `restart_workers` | Restart workers |

**Note**: Requires `system_administrator` role.

---

## Context Tools (periscope-context-dev)

| Tool | Description |
|------|-------------|
| `list_my_organizations` | List user's organizations |
| `list_my_projects` | List accessible projects |
| `get_current_context` | Get active org/project context |
| `set_context` | Set default org/project context |
| `clear_context` | Clear stored context |

**Note**: Context is stored in Redis with 30-day TTL. Used by MCP clients to maintain tenant context across requests.
