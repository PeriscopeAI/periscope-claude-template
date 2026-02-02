# Periscope Platform Learnings

This document captures learnings from working with the Periscope platform.

---

## Session: 2026-02-01 - Kitchen Inventory Management Workflow

### Context Management

**Learning 1: Always Set Context First**
- Before using any MCP tools, get and set the organization/project context
- Use `mcp__periscope-context__get_current_context` to check current context
- Use `mcp__periscope-context__set_context` to set org and project IDs
- Context is stored in Redis with 30-day TTL

**Learning 2: Context Propagation Issues**
- Issue discovered: Setting context via `set_context` may not propagate to all MCP servers
- The `script-functions` server returned `project_id: null` despite context being set
- **Status**: ~~Bug~~ **RESOLVED** (2026-02-02) - All APIs now accept explicit org_id/project_id

**Learning 2b: API Parameter Availability**
| MCP Server | create has org_id/project_id? | Status |
|------------|-------------------------------|--------|
| `periscope-agents-core` | YES | Use explicit params |
| `periscope-processes` | YES | Use explicit params |
| `periscope-script-functions` | YES | Fixed! Use explicit params |

**Recommendation**: Always pass explicit `organization_id` and `project_id` when available.

### Agent Configuration

**Learning 7: Valid Agent Types**
- `document_analyzer` - For document processing agents
- `business_decision` - For decision-making/analysis agents
- `custom` - For general-purpose agents

**Learning 8: Model Provider Requirements**
- All model providers require API keys to be configured
- API keys can be set via environment variables or Conjur
- Required environment variables:
  - `ANTHROPIC_API_KEY` - For Anthropic/Claude models
  - `OPENAI_API_KEY` - For OpenAI models
  - `OPENROUTER_API_KEY` - For OpenRouter models
  - `GOOGLE_API_KEY` - For Google/Gemini models
- **Issue discovered**: Agent creation fails if API key not configured (validated at creation time)

**Learning 9: Agent Capabilities (valid values)**
```
document_processing, data_analysis, web_search, code_generation,
file_operations, business_decision, risk_assessment, communication,
workflow_coordination, approval_processing
```

### Script Functions

**Learning 3: Function Signature Requirements**
- Script functions MUST use the signature: `def execute(input_data: dict) -> dict:`
- Do NOT use custom function names like `def main(...)` or `def check_stock(...)`
- All input parameters come from `input_data` dict
- Return value must be a dict

**Example - Correct:**
```python
def execute(input_data: dict) -> dict:
    items = input_data.get("items", [])
    threshold = input_data.get("threshold", 10)
    # ... processing ...
    return {"result": processed_items, "count": len(processed_items)}
```

**Example - Incorrect:**
```python
def main(items: list, threshold: int = 10) -> dict:  # WRONG!
    # This will fail validation
    pass
```

**Learning 4: Function Lifecycle**
- Functions start in 'draft' status
- Must be published using `publish_version` to be usable in workflows
- Each publish creates an immutable version snapshot

### BPMN Configuration (CRITICAL)

**Learning 10: Use Periscope Namespace, NOT Camunda**
- Use `xmlns:periscope="http://periscope.dev/schema/bpmn"` namespace
- Do NOT use `camunda` namespace - it is not supported
- Do NOT use `camunda:type`, `camunda:inputOutput`, `camunda:formData`, etc.

**Learning 11: Local Validation Before Upload**
- Always validate BPMN locally before uploading to save API round-trips
- Use: `python3 .claude/skills/process/scripts/validate-bpmn.py <file.bpmn> --verbose`
- Script validates: XML, structure, connectivity, and Periscope-specific rules

**Learning 12: Periscope Extension Elements**

| Task Type | Extension Element | Key Attributes |
|-----------|-------------------|----------------|
| Service Task (AI) | `periscope:AIAgentConfiguration` | `agentId`, `agentType`, `modelProvider`, `modelName`, `prompt` |
| Script Task | `periscope:ScriptTaskConfiguration` | `functionName`, `functionId` |
| User Task | `periscope:TaskDefinition` | `assignee`, `candidateGroups`, `priority` |
| Send Task | `periscope:SendTaskConfiguration` | Email configuration |
| Process | `periscope:processVariables` | Define input/output variables |

**Learning 13: AI Agent Configuration in BPMN**
```xml
<bpmn:serviceTask id="my_agent_task" name="Analyze Data">
  <bpmn:extensionElements>
    <periscope:AIAgentConfiguration agentId="my-agent" agentType="business_decision"
        modelProvider="openai" modelName="gpt-4o-mini"
        prompt="Analyze the data and provide recommendations.">
      <periscope:inputMapping source="input_data" target="data" />
      <periscope:outputMapping variable="result" errorVariable="error" />
      <periscope:advancedSettings temperature="0.3" maxTokens="2000" timeoutSeconds="60" />
      <periscope:structuredOutput enabled="true" strictMode="true">
        <periscope:outputField name="recommendation" fieldType="string" required="true" />
      </periscope:structuredOutput>
    </periscope:AIAgentConfiguration>
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

**Learning 14: Script Task Configuration in BPMN**
```xml
<bpmn:scriptTask id="my_script_task" name="Process Data">
  <bpmn:extensionElements>
    <periscope:ScriptTaskConfiguration functionName="my_function" description="Process data">
      <periscope:scriptTaskInputMapping source="input_var" target="param" mappingType="variable" />
      <periscope:outputVariable>result_var</periscope:outputVariable>
    </periscope:ScriptTaskConfiguration>
  </bpmn:extensionElements>
</bpmn:scriptTask>
```

**Learning 15: User Task Configuration in BPMN**
```xml
<bpmn:userTask id="my_user_task" name="Approve Request">
  <bpmn:extensionElements>
    <periscope:TaskDefinition assignee="${approver}" candidateGroups="managers" priority="1" outputVariable="approval_result">
      <periscope:formData>
        <periscope:field name="approved" type="boolean" required="true" label="Approve?" />
        <periscope:field name="notes" type="text" required="false" label="Notes" />
      </periscope:formData>
    </periscope:TaskDefinition>
  </bpmn:extensionElements>
</bpmn:userTask>
```

**Learning 16: BPMN Diagram Must Include Edges**
- Always include `bpmndi:BPMNEdge` elements for each sequence flow
- Without edges, the visual diagram won't show connections between nodes
- Each edge needs waypoints (`di:waypoint`) to define the path

**Learning 17: Gateway Requirements**
- Exclusive gateways with conditions should have a `default` flow
- Add `default="flow_id"` attribute to the gateway element
- Prevents deadlock when no condition matches

### Available Projects

For reference, the available projects in the admin org:
- **Test Processes** (`b1bff085-ad38-4c1a-9612-3df2a8aecf38`) - For experimentation
- **Default Project** (`68e5521d-a94f-41d8-97b4-70ad68fff924`) - For production

### MCP Tool Patterns

**Learning 5: Tool Discovery**
- Use `ToolSearch` with `+server-name` prefix to find tools from specific servers
- Example: `+periscope-context get` finds context-related tools
- Use `select:tool_name` for direct tool selection when you know the exact name

**Learning 6: Parallel Tool Calls**
- Independent tool calls can be made in parallel for efficiency
- Dependent calls must be sequential (e.g., set context before creating resources)

---

## Quick Reference

### Context Setup Pattern
```
1. mcp__periscope-context__get_current_context  - Check what's set
2. mcp__periscope-context__list_my_projects     - Find available projects
3. mcp__periscope-context__set_context          - Set org + project
```

### Workflow Creation Pattern
```
1. Set context (org + project)
2. Create script functions (draft)
3. Publish script functions
4. Create AI agents
5. Design BPMN process
6. Deploy to Temporal
7. Test execution
```

---

---

## Session: 2026-02-01 - Template Improvements

Based on learnings from the Kitchen Inventory session, the following template improvements were implemented:

### Files Updated

| File | Changes |
|------|---------|
| `.claude/agents/process-designer.md` | Context setup, BPMN namespace warning, extension cheat sheet, edge requirement, pre-deployment checklist |
| `.claude/agents/agent-manager.md` | Context setup, API key requirements, valid types/capabilities |
| `.claude/agents/integration-specialist.md` | Context setup, function signature requirement, known issues |
| `.claude/agents/process-generator.md` | Context setup, BPMN requirements, validation step, function signature |
| `.claude/skills/function/SKILL.md` | Fixed all examples to use `execute(input_data: dict)` signature |
| `.claude/skills/generate/SKILL.md` | Added behind-the-scenes steps, validation info |
| `docs/known-issues.md` | Created - documents platform bugs and workarounds |

### Key Improvements

1. **Context Management**: All agents now document the context setup pattern
2. **BPMN Namespace**: Critical warnings about using `periscope` not `camunda`
3. **Local Validation**: Instructions to use validation script before upload
4. **Function Signature**: Emphasized correct `def execute(input_data: dict) -> dict:` signature
5. **BPMN Edges**: Documented requirement for `bpmndi:BPMNEdge` elements
6. **Pre-deployment Checklist**: Added to process-designer agent
7. **Known Issues Doc**: Created central reference for platform bugs

---

*Last updated: 2026-02-02 (Context propagation issue marked resolved)*
