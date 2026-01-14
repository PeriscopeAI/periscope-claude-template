# MCP Tools Reference

This document provides a quick reference for all MCP tools available in the Periscope platform.

## Overview

| MCP Server | Tools | Agent |
|------------|-------|-------|
| periscope-workflows-dev | 27 | workflow-operator |
| periscope-processes-dev | 25 | process-designer |
| periscope-tasks-dev | 10 | workflow-operator, task-handler |
| periscope-agents-dev | 27 | agent-manager |
| periscope-mcp-servers-dev | 15 | agent-manager |
| periscope-protocols-dev | 28 | integration-specialist |
| periscope-email-dev | 5 | integration-specialist |
| periscope-documents-dev | 15 | integration-specialist |
| periscope-users-dev | 5 | task-handler, system-admin |
| periscope-system-dev | 3 | system-admin |

**Total: ~160 tools**

---

## Workflow Tools (periscope-workflows-dev)

### Registry & Discovery
| Tool | Description |
|------|-------------|
| `get_workflow_registry` | List registered workflow types |
| `list_workflows` | List workflow executions |
| `validate_expression` | Validate gateway conditions |
| `get_workflow_stats` | Get execution statistics |

### Workflow CRUD
| Tool | Description |
|------|-------------|
| `create_workflow` | Start new workflow |
| `get_workflow_status` | Get workflow status |
| `cancel_workflow` | Cancel running workflow |
| `signal_workflow` | Send signal to workflow |
| `search_workflows` | Search executions |

### History & Batch
| Tool | Description |
|------|-------------|
| `get_workflow_history` | Get Temporal history |
| `execute_batch_workflows` | Run multiple workflows |
| `get_batch_status` | Check batch progress |

### Scheduling
| Tool | Description |
|------|-------------|
| `schedule_workflow` | Schedule future execution |
| `list_scheduled_workflows` | List scheduled |
| `cancel_scheduled_workflow` | Cancel scheduled |

### Triggers
| Tool | Description |
|------|-------------|
| `list_signal_triggers` | List signal triggers |
| `list_message_triggers` | List message triggers |
| `trigger_workflow_by_signal` | Start by signal |
| `trigger_workflow_by_message` | Start by message |
| `webhook_trigger` | External webhook |

---

## Process Tools (periscope-processes-dev)

### Process CRUD
| Tool | Description |
|------|-------------|
| `create_process` | Create process definition |
| `list_processes` | List processes |
| `get_process` | Get process by ID |
| `update_process` | Update process |
| `delete_process` | Delete process |
| `get_process_bpmn` | Get BPMN XML |

### Lifecycle
| Tool | Description |
|------|-------------|
| `archive_process` | Archive (soft delete) |
| `unarchive_process` | Restore archived |

### Versions
| Tool | Description |
|------|-------------|
| `get_process_versions` | Version history |
| `get_process_version_detail` | Version details |
| `get_process_stats` | Execution stats |

### BPMN Operations
| Tool | Description |
|------|-------------|
| `validate_bpmn` | Validate BPMN XML |
| `convert_bpmn_process` | Convert to Temporal |
| `get_async_conversion_status` | Check conversion |

### Deployment
| Tool | Description |
|------|-------------|
| `deploy_process` | Deploy to Temporal |
| `list_deployments` | List deployments |
| `get_deployment_info` | Deployment details |
| `undeploy_workflow` | Remove deployment |
| `redeploy_workflow` | Redeploy |

### Health
| Tool | Description |
|------|-------------|
| `get_deployment_health` | Deployment health |
| `get_worker_status` | Worker status |
| `get_dynamic_discovery_stats` | Discovery stats |
| `force_discovery_check` | Force discovery |

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

## Agent Tools (periscope-agents-dev)

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

## Protocol Tools (periscope-protocols-dev)

### A2A Coordination
| Tool | Description |
|------|-------------|
| `discover_a2a_agents` | Find agents |
| `delegate_task_between_agents` | Agent-to-agent |
| `get_coordination_statistics` | Stats |
| `list_coordination_tasks` | List tasks |
| `get_coordination_task` | Get task |
| `list_coordination_workflows` | List workflows |

### AG-UI
| Tool | Description |
|------|-------------|
| `stream_ag_ui_response` | SSE streaming |
| `get_session_info` | Session info |
| `pause_session` | Pause session |
| `resume_session` | Resume session |

### Routing
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

## Document Tools (periscope-documents-dev)

### Documents
| Tool | Description |
|------|-------------|
| `documents_health` | Health check |
| `upload_document` | Upload to S3 |

### Script Functions
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
