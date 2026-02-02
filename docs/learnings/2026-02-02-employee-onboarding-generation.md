# Learning: Employee Onboarding Workflow Generation

**Date**: 2026-02-02
**Category**: Best Practice | Issue
**Impact**: High

## Summary

Key learnings from generating an employee onboarding workflow using `/generate`.

---

## 1. BPMN Extension Element Names are PascalCase

**Problem**: Local validator reported missing AI agent and script task configurations even though they were present in the BPMN.

**Cause**: Used camelCase element names instead of PascalCase.

| Wrong (camelCase) | Correct (PascalCase) |
|-------------------|----------------------|
| `periscope:aIAgentConfiguration` | `periscope:AIAgentConfiguration` |
| `periscope:scriptTaskConfiguration` | `periscope:ScriptTaskConfiguration` |
| `periscope:taskDefinition` | `periscope:TaskDefinition` |

**Solution**: Always use PascalCase for Periscope extension element names.

**How to Apply**:
```xml
<!-- Correct -->
<periscope:AIAgentConfiguration agentId="my-agent" />
<periscope:ScriptTaskConfiguration functionId="uuid" />
<periscope:TaskDefinition assignee="user@example.com" />

<!-- Wrong -->
<periscope:aIAgentConfiguration agentId="my-agent" />
```

---

## 2. BPMN Task Names - Avoid Special Characters

**Problem**: Task name "Extract & Validate Documents" caused API validation error.

**Cause**: Even when properly XML-escaped (`&amp;`), the ampersand caused issues during activity name generation.

**Solution**: Use plain English in task names - "Extract and Validate Documents".

**How to Apply**:
- Avoid `&`, `<`, `>`, `"`, `'` in task names
- Use "and" instead of "&"
- Keep names alphanumeric with spaces

---

## 3. File Upload URLs Expire Quickly

**Problem**: The `file_id` from `request_bpmn_upload` expired between validation and process creation calls.

**Solution**: Perform upload and process creation in quick succession. Don't add validation step between upload and create.

**How to Apply**:
```
1. request_bpmn_upload → get file_id
2. curl PUT the file
3. create_process_from_file_ref immediately (don't validate first)
```

Or validate locally before upload using `validate-bpmn.py`.

---

## 4. Workers Need Restart for New Workflows

**Problem**: Workflow task failed immediately after deployment with `WORKFLOW_TASK_FAILED` because workers hadn't loaded the new workflow definition.

**Cause**: Even with `auto_restart_workers=true` in deploy API, workers may not fully reload.

**Solution**: Manually restart workers after deployment using `mcp__periscope-system__restart_workers`.

**How to Apply**:
```
1. deploy_process(process_id, ...)
2. restart_workers()  # Explicit restart
3. Wait 5-10 seconds for workers to come back
4. create_workflow(...)
```

---

## 5. Agent API Requires Explicit Context IDs

**Problem**: `create_agent_enhanced` failed with "Organization context required" even after calling `set_context`.

**Cause**: Agent creation API doesn't read from context cache - requires explicit parameters.

**Solution**: Always pass `organization_id` and `project_id` explicitly to agent APIs.

**How to Apply**:
```python
# Wrong - relies on context
create_agent_enhanced(name="my-agent", ...)

# Correct - explicit IDs
create_agent_enhanced(
    name="my-agent",
    organization_id="uuid",
    project_id="uuid",
    ...
)
```

---

## 6. Workflow Status Shows Progress After Worker Restart

**Problem**: Workflow status showed 0 activities and "running" status but was actually stuck.

**Cause**: Workers hadn't loaded the workflow definition yet.

**Indicator**: Check `get_workflow_history` - if you see `WORKFLOW_TASK_FAILED` early, workers need restart.

**Solution**: After worker restart, workflow auto-retries and progress shows correctly.

---

## 7. Human Tasks Assigned to Roles Don't Appear in Personal Task List

**Problem**: After workflow created a human task assigned to `hr_team`, it didn't appear in `get_my_tasks`.

**Cause**: Task was assigned to a role, not the current user directly.

**Solution**: Use `claim_task` with the task ID (visible in workflow status activities) to claim it for yourself.

---

## Related

- [BPMN Format Requirements](../bpmn-format-requirements.md)
- [BPMN Extensions Reference](../bpmn-extensions-reference.md)
- [Known Issues](../known-issues.md)
- Local validator: `.claude/skills/process/scripts/validate-bpmn.py`
