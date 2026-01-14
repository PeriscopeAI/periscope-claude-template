# Loop Workflow Implementation Guide

This document captures learnings from implementing a loop workflow in Periscope, including common pitfalls and solutions.

## Overview

Loop workflows in Periscope use BPMN's exclusive gateway pattern with backward sequence flows to repeat tasks until a condition is met. The workflow logic is implemented using **script functions** that execute in a sandboxed environment.

## Architecture

```
┌─────────┐    ┌────────────┐    ┌──────────────┐    ┌───────────────┐
│  Start  │───▸│ Init Loop  │───▸│ Process Item │◂───│ Continue?     │
└─────────┘    └────────────┘    └──────┬───────┘    └───────┬───────┘
                                        │                     │
                                        ▼                     ▼
                                   ┌─────────┐          ┌─────────┐
                                   │   End   │◂─────────│   No    │
                                   └─────────┘          └─────────┘
```

## Key Components

### 1. Script Functions

Script functions are versioned Python functions that execute workflow logic. They run in a **RestrictedPython sandbox** with limited imports.

#### Creating a Script Function

```python
def execute(input_data: dict) -> dict:
    """Process one iteration and check loop condition.

    Accepts either:
    - Direct fields: {"counter": 0, "max_iterations": 3}
    - Nested from BPMN mapping: {"input_data": {"counter": 0, "max_iterations": 3}}
    """
    # Handle nested input_data from BPMN mapping
    data = input_data.get("input_data", input_data)

    counter = data.get("counter", 0) + 1
    max_iterations = data.get("max_iterations", 3)
    continue_loop = counter < max_iterations

    return {
        "counter": counter,
        "max_iterations": max_iterations,
        "result": f"Processed item {counter}",
        "continue_loop": continue_loop
    }
```

**Important**: Always handle nested input structures because BPMN input mappings may wrap data.

### 2. BPMN Script Task Configuration

Use `bpmn:scriptTask` (not `bpmn:serviceTask`) with the Periscope extension:

```xml
<bpmn:scriptTask id="process_item" name="Process Item">
  <bpmn:extensionElements>
    <periscope:scriptTaskConfiguration
      functionId="9bed6d65-4b77-4aa7-92ca-8fc6ebf07240"
      functionName="loop_process"
      version="2"
      outputVariable="loop_state">
      <periscope:scriptTaskInputMapping source="loop_state" target="input_data"/>
    </periscope:scriptTaskConfiguration>
  </bpmn:extensionElements>
  <bpmn:incoming>flow_init_to_process</bpmn:incoming>
  <bpmn:incoming>flow_loop_back</bpmn:incoming>
  <bpmn:outgoing>flow_process_to_gateway</bpmn:outgoing>
</bpmn:scriptTask>
```

**Attributes:**
- `functionId`: UUID of the script function
- `functionName`: Human-readable name
- `version`: Version number to use (increment when updating)
- `outputVariable`: Workflow context variable to store the result

### 3. Gateway Condition Expressions

Gateway conditions must be **valid Python expressions** that evaluate to boolean.

```xml
<!-- Loop back when continue_loop is True -->
<bpmn:sequenceFlow id="flow_loop_back" name="Yes"
                   sourceRef="check_continue" targetRef="process_item">
  <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
    loop_state and loop_state["continue_loop"] == True
  </bpmn:conditionExpression>
</bpmn:sequenceFlow>

<!-- Exit when continue_loop is False -->
<bpmn:sequenceFlow id="flow_to_end" name="No"
                   sourceRef="check_continue" targetRef="end">
  <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
    loop_state and loop_state["continue_loop"] == False
  </bpmn:conditionExpression>
</bpmn:sequenceFlow>
```

**Best Practices:**
- Use truthiness check first: `loop_state and loop_state["key"]`
- Use bracket notation: `loop_state["key"]` not `loop_state.key`
- Use Python booleans: `True`/`False` not `true`/`false`

### 4. Process Variables Declaration

Declare process variables in the extension elements:

```xml
<bpmn:process id="loop-with-functions" name="Simple Loop" isExecutable="true">
  <bpmn:extensionElements>
    <periscope:processVariables>
      <periscope:processVariable name="max_iterations" type="number"
                                 required="false" isInput="true"/>
      <periscope:processVariable name="loop_state" type="object"
                                 required="false" isInput="false"/>
    </periscope:processVariables>
  </bpmn:extensionElements>
  ...
</bpmn:process>
```

## Common Errors and Solutions

### Error 1: Maximum Recursion Depth Exceeded

```
Conversion failed: Template rendering error: maximum recursion depth exceeded
```

**Cause:** BPMN-to-Temporal converter was not tracking visited nodes during graph traversal.

**Solution:** Platform fix deployed - converter now tracks visited nodes.

### Error 2: WORKFLOW_TASK_FAILED on Startup

```
WORKFLOW_TASK_FAILED immediately after start (event 4)
```

**Cause:** Generated workflow code contained `import structlog` which is blocked by RestrictedPython.

**Solution:** Platform fix - removed structlog imports from workflow templates.

### Error 3: compile() arg 1 must be string

```
compile() arg 1 must be a string, bytes or AST object
```

**Cause:** Used JUEL/EL expression syntax `${variable.field == true}` instead of Python.

**Solution:** Use Python syntax: `variable["field"] == True`

### Error 4: Input Validation Failed

```
Input validation failed: 'counter' is a required property
```

**Cause:** BPMN input mapping wrapped data in nested structure, but function expected direct properties.

**Solution:** Update function to handle both formats:
```python
data = input_data.get("input_data", input_data)
counter = data.get("counter", 0)
```

### Error 5: Missing Activity Timeout

**Cause:** Activities had no timeout configured.

**Solution:** Platform added default 5-minute timeout to service task template.

## Input/Output Mapping Patterns

### Pattern 1: Direct Variable Mapping

```xml
<periscope:scriptTaskInputMapping source="max_iterations" target="max_iterations"/>
```

Maps workflow variable `max_iterations` directly to function input `max_iterations`.

### Pattern 2: Object Mapping

```xml
<periscope:scriptTaskInputMapping source="loop_state" target="input_data"/>
```

Maps entire `loop_state` object to function input `input_data`. Function receives:
```python
{"input_data": {"counter": 1, "max_iterations": 3, ...}}
```

### Pattern 3: Output Variable

```xml
<periscope:scriptTaskConfiguration outputVariable="loop_state" ...>
```

Function return value is stored in workflow context as `loop_state`.

## Complete BPMN Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
    xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:periscope="http://periscope.dev/schema/bpmn"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    id="Definitions_Loop"
    targetNamespace="http://periscope.io/bpmn">

  <bpmn:process id="loop-process" name="Loop Workflow" isExecutable="true">

    <bpmn:extensionElements>
      <periscope:processVariables>
        <periscope:processVariable name="max_iterations" type="number"
                                   required="false" isInput="true"/>
        <periscope:processVariable name="loop_state" type="object"
                                   required="false" isInput="false"/>
      </periscope:processVariables>
    </bpmn:extensionElements>

    <bpmn:startEvent id="start" name="Start">
      <bpmn:outgoing>flow_to_init</bpmn:outgoing>
    </bpmn:startEvent>

    <bpmn:scriptTask id="init_loop" name="Initialize Loop">
      <bpmn:extensionElements>
        <periscope:scriptTaskConfiguration
          functionId="YOUR_INIT_FUNCTION_ID"
          functionName="loop_init"
          version="1"
          outputVariable="loop_state">
          <periscope:scriptTaskInputMapping source="max_iterations" target="max_iterations"/>
        </periscope:scriptTaskConfiguration>
      </bpmn:extensionElements>
      <bpmn:incoming>flow_to_init</bpmn:incoming>
      <bpmn:outgoing>flow_to_process</bpmn:outgoing>
    </bpmn:scriptTask>

    <bpmn:scriptTask id="process_item" name="Process Item">
      <bpmn:extensionElements>
        <periscope:scriptTaskConfiguration
          functionId="YOUR_PROCESS_FUNCTION_ID"
          functionName="loop_process"
          version="1"
          outputVariable="loop_state">
          <periscope:scriptTaskInputMapping source="loop_state" target="input_data"/>
        </periscope:scriptTaskConfiguration>
      </bpmn:extensionElements>
      <bpmn:incoming>flow_to_process</bpmn:incoming>
      <bpmn:incoming>flow_loop_back</bpmn:incoming>
      <bpmn:outgoing>flow_to_gateway</bpmn:outgoing>
    </bpmn:scriptTask>

    <bpmn:exclusiveGateway id="check_continue" name="Continue?">
      <bpmn:incoming>flow_to_gateway</bpmn:incoming>
      <bpmn:outgoing>flow_loop_back</bpmn:outgoing>
      <bpmn:outgoing>flow_to_end</bpmn:outgoing>
    </bpmn:exclusiveGateway>

    <bpmn:endEvent id="end" name="End">
      <bpmn:incoming>flow_to_end</bpmn:incoming>
    </bpmn:endEvent>

    <!-- Sequence Flows -->
    <bpmn:sequenceFlow id="flow_to_init" sourceRef="start" targetRef="init_loop"/>
    <bpmn:sequenceFlow id="flow_to_process" sourceRef="init_loop" targetRef="process_item"/>
    <bpmn:sequenceFlow id="flow_to_gateway" sourceRef="process_item" targetRef="check_continue"/>

    <bpmn:sequenceFlow id="flow_loop_back" name="Yes"
                       sourceRef="check_continue" targetRef="process_item">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
        loop_state and loop_state["continue_loop"] == True
      </bpmn:conditionExpression>
    </bpmn:sequenceFlow>

    <bpmn:sequenceFlow id="flow_to_end" name="No"
                       sourceRef="check_continue" targetRef="end">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
        loop_state and loop_state["continue_loop"] == False
      </bpmn:conditionExpression>
    </bpmn:sequenceFlow>

  </bpmn:process>

</bpmn:definitions>
```

## Debugging Tips

1. **Check Workflow History**: Use `get_workflow_history` to trace execution events and find where failures occur.

2. **Test Functions Independently**: Use `test_function` MCP tool before deploying to workflows.

3. **Compare with Working Examples**: Reference the MicroStep invoice approval process for correct BPMN patterns.

4. **Version Management**: Always increment function version and update BPMN when making changes.

5. **Redeploy After Platform Fixes**: Workflows must be redeployed to regenerate with updated templates.

## Related Resources

- [BPMN Extensions Reference](./bpmn-extensions-reference.md)
- [Troubleshooting Guide](./troubleshooting.md)
- [MCP Tools Reference](./mcp-tools-reference.md)
