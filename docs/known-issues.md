# Periscope Platform - Known Issues

This document tracks known issues and workarounds for the Periscope platform.

---

## Context Management

### Issue: Script Functions Context Not Propagating

**Status**: ~~Open Bug~~ **RESOLVED**
**Severity**: High
**Affected**: `periscope-script-functions` MCP server

**Description**: Setting context via `mcp__periscope-context__set_context` does not propagate to the script-functions server. The `create_function` API returns:
```
null value in column 'project_id' of relation 'script_functions' violates not-null constraint
```

**Root Cause**: The script-functions MCP server doesn't receive the project context from Redis/session.

**Resolution**: The `create_function` API now accepts explicit `organization_id` and `project_id` parameters. Pass these explicitly when creating functions:
```python
create_function(
    name="my_function",
    code="...",
    organization_id="<org-uuid>",
    project_id="<project-uuid>",
    ...
)
```

---

## Agent Management

### Issue: API Keys Required at Creation Time

**Status**: By Design
**Severity**: Medium
**Affected**: `periscope-agents-core` MCP server

**Description**: Agent creation validates API keys at creation time. If the required API key for the specified `model_provider` is not configured, agent creation fails with an error like:
```
OpenAI API key not found. Set OPENAI_API_KEY environment variable or configure it in Conjur.
```

**Workaround**: Ensure API keys are configured before creating agents:

| Provider | Environment Variable |
|----------|---------------------|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Google | `GOOGLE_API_KEY` |

---

## BPMN Processing

### Issue: Camunda Namespace Not Supported

**Status**: By Design
**Severity**: Critical
**Affected**: BPMN validation and deployment

**Description**: The Periscope platform does NOT support the Camunda BPMN namespace. Using `xmlns:camunda` or Camunda-specific elements will cause validation failures.

**Workaround**: Use the Periscope namespace:
```xml
xmlns:periscope="http://periscope.dev/schema/bpmn"
```

Replace all Camunda elements:
| Camunda (Wrong) | Periscope (Correct) |
|-----------------|---------------------|
| `camunda:inputOutput` | `periscope:inputMapping` / `periscope:outputMapping` |
| `camunda:formData` | `periscope:formData` |
| `camunda:field` | `periscope:field` |

---

### Issue: BPMN Diagram Edges Missing

**Status**: User Error (Common)
**Severity**: Medium
**Affected**: BPMN visual rendering

**Description**: If BPMN files don't include `bpmndi:BPMNEdge` elements for sequence flows, the visual diagram in the designer won't show connections between nodes.

**Workaround**: Always include edge elements:
```xml
<bpmndi:BPMNEdge id="flow1_edge" bpmnElement="flow_id">
  <di:waypoint x="136" y="218" />
  <di:waypoint x="200" y="218" />
</bpmndi:BPMNEdge>
```

---

## API Parameter Consistency

### Issue: Inconsistent org_id/project_id Parameter Support

**Status**: ~~Inconsistency~~ **RESOLVED**
**Severity**: Medium
**Affected**: Various MCP servers

**Description**: Previously, not all MCP server `create_*` operations supported explicit `organization_id`/`project_id` parameters. This has been fixed.

| MCP Server | Supports Explicit IDs? | Workaround |
|------------|------------------------|------------|
| `periscope-agents-core` | YES | Pass explicit params |
| `periscope-processes` | YES | Pass explicit params |
| `periscope-script-functions` | YES | Pass explicit params (fixed!) |

**Recommendation**: Always pass explicit `organization_id` and `project_id` when the API supports it, as context auto-propagation is unreliable.

---

## Script Functions

### Issue: Function Signature Validation Strict

**Status**: By Design
**Severity**: High
**Affected**: Script function creation and updates

**Description**: Script functions MUST use the exact signature:
```python
def execute(input_data: dict) -> dict:
```

Common mistakes that cause validation failures:
- Using custom function names (`def main()`, `def process()`)
- Using direct parameters (`def execute(items, threshold)`)
- Missing return type annotation

**Workaround**: Always use the correct signature:
```python
def execute(input_data: dict) -> dict:
    items = input_data.get("items", [])
    threshold = input_data.get("threshold", 10)
    # ... processing ...
    return {"result": processed_data}
```

---

*Last updated: 2026-02-01*
