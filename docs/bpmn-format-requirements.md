# BPMN Format Requirements

This document specifies the BPMN format requirements for Periscope process definitions, including supported elements, validation rules, and conversion constraints.

## Overview

Periscope accepts BPMN 2.0 XML files and converts them to Temporal workflows. Not all BPMN elements are supported—this guide documents what works and what doesn't.

## Extension Schema Reference

The canonical source for Periscope BPMN extensions is defined in:
```
services/frontend/src/components/process-designer/periscope.json
```

This moddle extension file defines all supported custom elements for bpmn-js. The namespace URI is:
```
http://periscope.dev/schema/bpmn
```

### Supported Extension Types

| Extension | Used In | Purpose |
|-----------|---------|---------|
| `ProcessVariables` | Process | Define workflow input/output variables |
| `ProcessVariable` | ProcessVariables | Individual variable definition |
| `AIAgentConfiguration` | Service Task | Configure AI agent execution |
| `TaskDefinition` | User Task | Human task assignment and forms |
| `FormData` / `Field` | TaskDefinition | Form field definitions |
| `ScriptTaskConfiguration` | Script Task | Python function execution |
| `SendTaskConfiguration` | Send Task | Email sending configuration |
| `EmailTriggerConfiguration` | Start Event | Email-triggered workflow start |
| `CallActivityConfiguration` | Call Activity | Child workflow invocation |
| `SubprocessConfiguration` | Subprocess | Embedded subprocess settings |
| `MultiInstanceConfiguration` | Any Task | Loop/iteration settings |
| `EmailNotificationConfig` | TaskDefinition | Task email notifications |

See [BPMN Extensions Reference](./bpmn-extensions-reference.md) for detailed attribute documentation.

---

## Required XML Namespaces

### Mandatory Namespaces

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  targetNamespace="http://example.com/bpmn"
  id="definitions_1">
```

### Optional Namespaces

```xml
<!-- Periscope custom extensions -->
xmlns:periscope="http://periscope.dev/schema/bpmn"

<!-- Compatibility with other engines -->
xmlns:zeebe="http://camunda.org/schema/zeebe/1.0"
xmlns:camunda="http://camunda.org/schema/1.0/bpmn"
```

---

## Supported BPMN Elements

### Start Events (4 types)

| Element | Temporal Mapping | Status |
|---------|------------------|--------|
| None Start Event | Workflow entry point | ✅ Supported |
| Timer Start Event | Temporal Schedule | ✅ Supported |
| Message Start Event | Signal-triggered start | ✅ Supported |
| Signal Start Event | Signal-triggered start | ✅ Supported |

```xml
<!-- None Start Event -->
<bpmn:startEvent id="start" name="Start">
  <bpmn:outgoing>flow1</bpmn:outgoing>
</bpmn:startEvent>

<!-- Timer Start Event (ISO 8601) -->
<bpmn:startEvent id="timer_start" name="Daily at 9 AM">
  <bpmn:timerEventDefinition>
    <bpmn:timeCycle>R/2024-01-01T09:00:00Z/P1D</bpmn:timeCycle>
  </bpmn:timerEventDefinition>
  <bpmn:outgoing>flow1</bpmn:outgoing>
</bpmn:startEvent>

<!-- Message Start Event -->
<bpmn:startEvent id="msg_start" name="Email Received">
  <bpmn:messageEventDefinition messageRef="InvoiceMessage" />
  <bpmn:outgoing>flow1</bpmn:outgoing>
</bpmn:startEvent>
```

### End Events (2 types)

| Element | Temporal Mapping | Status |
|---------|------------------|--------|
| None End Event | Workflow return | ✅ Supported |
| Error End Event | raise Exception | ✅ Supported |

```xml
<!-- None End Event -->
<bpmn:endEvent id="end" name="Complete">
  <bpmn:incoming>flow_final</bpmn:incoming>
</bpmn:endEvent>

<!-- Error End Event -->
<bpmn:endEvent id="error_end" name="Validation Failed">
  <bpmn:errorEventDefinition errorRef="ValidationError" />
  <bpmn:incoming>error_flow</bpmn:incoming>
</bpmn:endEvent>
```

### Intermediate Events (5 types)

| Element | Temporal Mapping | Status |
|---------|------------------|--------|
| Timer Catch | workflow.sleep() | ✅ Supported |
| Message Catch | Signal wait | ✅ Supported |
| Signal Catch | Signal wait | ✅ Supported |
| Conditional Catch | Polling condition | ✅ Supported |
| None Throw | Flow marker/logging | ✅ Supported |

```xml
<!-- Timer Intermediate (wait 1 hour) -->
<bpmn:intermediateCatchEvent id="wait_1h" name="Wait 1 Hour">
  <bpmn:timerEventDefinition>
    <bpmn:timeDuration>PT1H</bpmn:timeDuration>
  </bpmn:timerEventDefinition>
</bpmn:intermediateCatchEvent>

<!-- Message Intermediate -->
<bpmn:intermediateCatchEvent id="wait_approval" name="Wait for Approval">
  <bpmn:messageEventDefinition messageRef="ApprovalMessage" />
</bpmn:intermediateCatchEvent>
```

### Boundary Events (4 types)

| Element | Temporal Mapping | Status |
|---------|------------------|--------|
| Timer Boundary | Activity timeout | ✅ Supported |
| Message Boundary | Race condition | ✅ Supported |
| Signal Boundary | Race condition | ✅ Supported |
| Error Boundary | Exception handler | ✅ Supported |

```xml
<!-- Timer Boundary (timeout after 30 minutes) -->
<bpmn:boundaryEvent id="timeout" attachedToRef="long_task" cancelActivity="true">
  <bpmn:timerEventDefinition>
    <bpmn:timeDuration>PT30M</bpmn:timeDuration>
  </bpmn:timerEventDefinition>
  <bpmn:outgoing>timeout_flow</bpmn:outgoing>
</bpmn:boundaryEvent>

<!-- Error Boundary -->
<bpmn:boundaryEvent id="error_handler" attachedToRef="risky_task">
  <bpmn:errorEventDefinition errorRef="ProcessingError" />
  <bpmn:outgoing>error_recovery_flow</bpmn:outgoing>
</bpmn:boundaryEvent>
```

### Tasks (4 types)

| Element | Temporal Mapping | Status |
|---------|------------------|--------|
| Service Task | Temporal Activity | ✅ Supported |
| User Task | Signal wait + Human task | ✅ Supported |
| Script Task | Python function activity | ✅ Supported |
| Generic Task | Basic activity | ✅ Supported |

```xml
<!-- Service Task (AI Agent) -->
<bpmn:serviceTask id="extract_data" name="Extract Invoice Data">
  <bpmn:extensionElements>
    <periscope:aIAgentConfiguration agentId="invoice-extractor" />
  </bpmn:extensionElements>
  <bpmn:incoming>flow1</bpmn:incoming>
  <bpmn:outgoing>flow2</bpmn:outgoing>
</bpmn:serviceTask>

<!-- User Task -->
<bpmn:userTask id="approve" name="Manager Approval">
  <bpmn:extensionElements>
    <periscope:taskDefinition assignee="${manager}" />
  </bpmn:extensionElements>
  <bpmn:incoming>flow2</bpmn:incoming>
  <bpmn:outgoing>flow3</bpmn:outgoing>
</bpmn:userTask>

<!-- Script Task -->
<bpmn:scriptTask id="calculate" name="Calculate Totals">
  <bpmn:extensionElements>
    <periscope:scriptTaskConfiguration
      functionId="invoice-calculator"
      functionName="calculate_totals" />
  </bpmn:extensionElements>
  <bpmn:incoming>flow3</bpmn:incoming>
  <bpmn:outgoing>flow4</bpmn:outgoing>
</bpmn:scriptTask>
```

### Gateways (3 types)

| Element | Temporal Mapping | Status |
|---------|------------------|--------|
| Exclusive Gateway | if/elif/else | ✅ Supported |
| Parallel Gateway | asyncio.gather() | ✅ Supported |
| Inclusive Gateway | Multi-condition | ✅ Supported |

```xml
<!-- Exclusive Gateway -->
<bpmn:exclusiveGateway id="check_amount" name="Check Amount">
  <bpmn:incoming>flow1</bpmn:incoming>
  <bpmn:outgoing>high_value</bpmn:outgoing>
  <bpmn:outgoing>low_value</bpmn:outgoing>
</bpmn:exclusiveGateway>

<bpmn:sequenceFlow id="high_value" sourceRef="check_amount" targetRef="manager_approval">
  <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
    amount > 1000
  </bpmn:conditionExpression>
</bpmn:sequenceFlow>

<bpmn:sequenceFlow id="low_value" sourceRef="check_amount" targetRef="auto_approve">
  <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
    amount &lt;= 1000
  </bpmn:conditionExpression>
</bpmn:sequenceFlow>

<!-- Parallel Gateway -->
<bpmn:parallelGateway id="fork" name="Start Parallel">
  <bpmn:incoming>flow1</bpmn:incoming>
  <bpmn:outgoing>branch_a</bpmn:outgoing>
  <bpmn:outgoing>branch_b</bpmn:outgoing>
</bpmn:parallelGateway>

<bpmn:parallelGateway id="join" name="Join Parallel">
  <bpmn:incoming>branch_a_end</bpmn:incoming>
  <bpmn:incoming>branch_b_end</bpmn:incoming>
  <bpmn:outgoing>continue</bpmn:outgoing>
</bpmn:parallelGateway>
```

### Subprocesses (3 types)

| Element | Temporal Mapping | Status |
|---------|------------------|--------|
| Embedded Subprocess | Child workflow | ✅ Supported |
| Event Subprocess | Signal-triggered child | ✅ Supported |
| Call Activity | External workflow | ✅ Supported |

```xml
<!-- Embedded Subprocess -->
<bpmn:subProcess id="validation_subprocess" name="Validate Document">
  <bpmn:startEvent id="sub_start" />
  <bpmn:serviceTask id="validate_format" name="Validate Format" />
  <bpmn:serviceTask id="validate_content" name="Validate Content" />
  <bpmn:endEvent id="sub_end" />
  <!-- Sequence flows within subprocess -->
</bpmn:subProcess>

<!-- Call Activity (reusable process) -->
<bpmn:callActivity id="call_approval" name="Run Approval Process"
  calledElement="approval_workflow">
  <bpmn:incoming>flow1</bpmn:incoming>
  <bpmn:outgoing>flow2</bpmn:outgoing>
</bpmn:callActivity>
```

### Loop Constructs (3 types)

| Element | Temporal Mapping | Status |
|---------|------------------|--------|
| Standard Loop | while loop | ✅ Supported |
| Multi-Instance Sequential | for loop | ✅ Supported |
| Multi-Instance Parallel | asyncio.gather() | ✅ Supported |

```xml
<!-- Multi-Instance Sequential -->
<bpmn:serviceTask id="process_items" name="Process Each Item">
  <bpmn:multiInstanceLoopCharacteristics isSequential="true">
    <bpmn:loopCardinality>${items.length}</bpmn:loopCardinality>
  </bpmn:multiInstanceLoopCharacteristics>
</bpmn:serviceTask>

<!-- Multi-Instance Parallel -->
<bpmn:serviceTask id="notify_all" name="Notify All Reviewers">
  <bpmn:multiInstanceLoopCharacteristics isSequential="false">
    <bpmn:loopCardinality>${reviewers.length}</bpmn:loopCardinality>
  </bpmn:multiInstanceLoopCharacteristics>
</bpmn:serviceTask>
```

---

## Unsupported Elements

These BPMN elements are **not yet implemented**:

| Element | Reason |
|---------|--------|
| Business Rule Task | Use script functions instead |
| Send Task | Use service task with email config |
| Receive Task | Use message events instead |
| Manual Task | Use user task instead |
| Complex Gateway | Use multiple exclusive gateways |
| Event-based Gateway | Use parallel + message events |
| Ad-hoc Subprocess | Not supported in Temporal |
| Transaction | Use saga patterns manually |
| Data Object | Use process variables |
| Data Store | Use MCP servers |
| Pools/Lanes | Multi-tenant via queues |
| Compensation Events | Manual saga implementation |
| Escalation Events | Use signals instead |
| Message Flows | Use signals for inter-process |

---

## Validation Rules

### Priority Levels

| Level | Impact | Examples |
|-------|--------|----------|
| CRITICAL | Blocks deployment | Missing start/end, circular flows |
| HIGH | Affects reliability | Missing retry policies, timeout issues |
| MEDIUM | Performance concerns | Inefficient patterns, large history |
| LOW | Best practices | Audit trail, naming conventions |

### Critical Validators

**Flow Connectivity:**
- Every element must have incoming flow (except start events)
- Every element must have outgoing flow (except end events)
- All paths must lead to an end event

**Reachability:**
- No orphaned elements
- No dead-end paths
- All branches must converge or terminate

**Gateway Logic:**
- Exclusive gateways must have conditions on outgoing flows
- Parallel gateways must have matching fork/join pairs
- Default flow recommended for exclusive gateways

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Missing start event" | No `<bpmn:startEvent>` | Add start event |
| "Missing end event" | No `<bpmn:endEvent>` | Add end event |
| "Disconnected element" | Element with no flows | Connect with sequence flows |
| "Unreachable path" | Dead branch | Add end event or connect |
| "Circular flow" | Loop without exit | Add gateway with exit condition |
| "Invalid condition" | Syntax error in expression | Fix expression syntax |

---

## Process Naming Rules

### Process ID

Must follow Python identifier rules:

```
Pattern: ^[a-zA-Z][a-zA-Z0-9_]*$
```

| Valid | Invalid |
|-------|---------|
| `expense_approval` | `expense-approval` (hyphen) |
| `InvoiceProcess` | `123_process` (starts with number) |
| `process_v2` | `process v2` (space) |

### Variable Names

| Constraint | Value |
|------------|-------|
| Pattern | `^[a-zA-Z][a-zA-Z0-9_]*$` |
| Max length | 64 characters |
| Case | Sensitive |

Reserved words (cannot use):
```
input, output, result, error, context, workflow, activity,
signal, timer, process, task, start, end, true, false, null
```

---

## File Size Limits

| Threshold | Processing |
|-----------|------------|
| < 1 MB | Synchronous (immediate response) |
| ≥ 1 MB | Asynchronous (returns conversion_id) |

For large files, poll for status:
```python
get_async_conversion_status(conversion_id="<id>")
```

---

## BPMN Diagram Interchange (BPMNDI)

For BPMN files to render visually in bpmn-js, they **must include diagram interchange elements**. Without BPMNDI, the process logic is valid but won't display in the designer.

### Required BPMNDI Structure

```xml
<bpmndi:BPMNDiagram id="BPMNDiagram_1">
  <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="process_id">
    <!-- Shapes for nodes (events, tasks, gateways) -->
    <bpmndi:BPMNShape id="shape_id" bpmnElement="element_id">
      <dc:Bounds x="100" y="100" width="100" height="80" />
    </bpmndi:BPMNShape>

    <!-- Edges for flows -->
    <bpmndi:BPMNEdge id="edge_id" bpmnElement="flow_id">
      <di:waypoint x="200" y="140" />
      <di:waypoint x="300" y="140" />
    </bpmndi:BPMNEdge>
  </bpmndi:BPMNPlane>
</bpmndi:BPMNDiagram>
```

### Element Dimensions

Standard sizes for BPMN elements in bpmn-js:

| Element Type | Width | Height | Notes |
|--------------|-------|--------|-------|
| Start Event | 36 | 36 | Circle |
| End Event | 36 | 36 | Circle (bold) |
| Intermediate Event | 36 | 36 | Circle (double) |
| Task | 100 | 80 | Rounded rectangle |
| Gateway | 50 | 50 | Diamond (rotated square) |
| Subprocess | 350 | 200 | Expandable, min size |

### BPMNShape Attributes

```xml
<bpmndi:BPMNShape
  id="StartEvent_1_di"           <!-- Unique shape ID (typically: elementId + "_di") -->
  bpmnElement="StartEvent_1"     <!-- References the process element ID -->
  isExpanded="true"              <!-- For subprocesses: expanded view -->
  isHorizontal="true"            <!-- For pools/lanes: orientation -->
  isMarkerVisible="true">        <!-- For gateways: show marker -->
  <dc:Bounds x="179" y="99" width="36" height="36" />
  <bpmndi:BPMNLabel>             <!-- Optional: label position -->
    <dc:Bounds x="152" y="142" width="90" height="14" />
  </bpmndi:BPMNLabel>
</bpmndi:BPMNShape>
```

### BPMNEdge Attributes

```xml
<bpmndi:BPMNEdge
  id="Flow_1_di"                 <!-- Unique edge ID -->
  bpmnElement="Flow_1">          <!-- References the sequenceFlow ID -->
  <di:waypoint x="215" y="117" />   <!-- Start point -->
  <di:waypoint x="270" y="117" />   <!-- End point (can have multiple waypoints for bends) -->
  <bpmndi:BPMNLabel>             <!-- Optional: condition label position -->
    <dc:Bounds x="230" y="99" width="25" height="14" />
  </bpmndi:BPMNLabel>
</bpmndi:BPMNEdge>
```

### Layout Guidelines

**Horizontal flow (left-to-right):**
- Start events on the left (x: ~180)
- Tasks flow rightward with ~50px gaps
- End events on the right
- Y-coordinate typically consistent for main flow (~100-120)

**Vertical spacing for branches:**
- Gateway at decision point
- Upper branch: y - 100
- Lower branch: y + 100
- Merge gateway brings paths together

**Grid alignment:**
- Elements typically aligned to 10px grid
- Consistent vertical alignment improves readability

### Boundary Event Positioning

Boundary events attach to task edges:

```xml
<!-- Task at position (270, 77) with size (100, 80) -->
<bpmndi:BPMNShape id="Task_1_di" bpmnElement="Task_1">
  <dc:Bounds x="270" y="77" width="100" height="80" />
</bpmndi:BPMNShape>

<!-- Boundary event on bottom edge of task -->
<bpmndi:BPMNShape id="BoundaryEvent_1_di" bpmnElement="BoundaryEvent_1">
  <dc:Bounds x="302" y="139" width="36" height="36" />
  <!-- x: task.x + (task.width/2) - (event.width/2) = 270 + 50 - 18 = 302 -->
  <!-- y: task.y + task.height - (event.height/2) = 77 + 80 - 18 = 139 -->
</bpmndi:BPMNShape>
```

---

## Minimal Valid BPMN

The smallest valid BPMN process **with diagram elements for visual rendering**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  targetNamespace="http://example.com/bpmn"
  id="definitions_1">

  <!-- Process Definition -->
  <bpmn:process id="minimal_process" name="Minimal Process" isExecutable="true">
    <bpmn:startEvent id="start" name="Start">
      <bpmn:outgoing>flow1</bpmn:outgoing>
    </bpmn:startEvent>

    <bpmn:endEvent id="end" name="End">
      <bpmn:incoming>flow1</bpmn:incoming>
    </bpmn:endEvent>

    <bpmn:sequenceFlow id="flow1" sourceRef="start" targetRef="end" />
  </bpmn:process>

  <!-- Diagram Interchange (required for visual rendering) -->
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="minimal_process">
      <bpmndi:BPMNShape id="start_di" bpmnElement="start">
        <dc:Bounds x="179" y="99" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="185" y="142" width="25" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="end_di" bpmnElement="end">
        <dc:Bounds x="272" y="99" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="280" y="142" width="20" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNEdge id="flow1_di" bpmnElement="flow1">
        <di:waypoint x="215" y="117" />
        <di:waypoint x="272" y="117" />
      </bpmndi:BPMNEdge>
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>

</bpmn:definitions>
```

**Note:** Without the `<bpmndi:BPMNDiagram>` section, the process is logically valid but will not render in the bpmn-js designer.

---

## Complete Example

A realistic process with all common elements:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:periscope="http://periscope.dev/schema/bpmn"
  targetNamespace="http://example.com/bpmn"
  id="definitions_1">

  <bpmn:process id="invoice_processing" name="Invoice Processing" isExecutable="true">

    <!-- Process Variables -->
    <bpmn:extensionElements>
      <periscope:processVariables>
        <periscope:processVariable
          name="document_url"
          type="string"
          required="true"
          isInput="true" />
        <periscope:processVariable
          name="extracted_data"
          type="object" />
        <periscope:processVariable
          name="approval_result"
          type="object" />
      </periscope:processVariables>
    </bpmn:extensionElements>

    <!-- Start -->
    <bpmn:startEvent id="start" name="Invoice Received">
      <bpmn:outgoing>to_extract</bpmn:outgoing>
    </bpmn:startEvent>

    <!-- AI Extraction -->
    <bpmn:serviceTask id="extract" name="Extract Invoice Data">
      <bpmn:extensionElements>
        <periscope:aIAgentConfiguration
          agentId="invoice-extractor"
          modelProvider="openai"
          modelName="gpt-4o">
          <periscope:inputMapping source="document_url" target="file_url" />
          <periscope:outputMapping variable="extracted_data" />
        </periscope:aIAgentConfiguration>
      </bpmn:extensionElements>
      <bpmn:incoming>to_extract</bpmn:incoming>
      <bpmn:outgoing>to_check</bpmn:outgoing>
    </bpmn:serviceTask>

    <!-- Amount Check Gateway -->
    <bpmn:exclusiveGateway id="check_amount" name="Check Amount">
      <bpmn:incoming>to_check</bpmn:incoming>
      <bpmn:outgoing>high_value</bpmn:outgoing>
      <bpmn:outgoing>low_value</bpmn:outgoing>
    </bpmn:exclusiveGateway>

    <!-- High Value Path: Manager Approval -->
    <bpmn:userTask id="manager_approval" name="Manager Approval">
      <bpmn:extensionElements>
        <periscope:taskDefinition
          assignee="${extracted_data.approver}"
          priority="2"
          outputVariable="approval_result">
          <periscope:formData>
            <periscope:field name="approved" type="boolean" required="true" />
            <periscope:field name="comments" type="text" />
          </periscope:formData>
        </periscope:taskDefinition>
      </bpmn:extensionElements>
      <bpmn:incoming>high_value</bpmn:incoming>
      <bpmn:outgoing>from_approval</bpmn:outgoing>
    </bpmn:userTask>

    <!-- Approval Timeout -->
    <bpmn:boundaryEvent id="approval_timeout" attachedToRef="manager_approval">
      <bpmn:timerEventDefinition>
        <bpmn:timeDuration>P2D</bpmn:timeDuration>
      </bpmn:timerEventDefinition>
      <bpmn:outgoing>to_escalation</bpmn:outgoing>
    </bpmn:boundaryEvent>

    <!-- Low Value Path: Auto Approve -->
    <bpmn:serviceTask id="auto_approve" name="Auto Approve">
      <bpmn:incoming>low_value</bpmn:incoming>
      <bpmn:outgoing>from_auto</bpmn:outgoing>
    </bpmn:serviceTask>

    <!-- Merge -->
    <bpmn:exclusiveGateway id="merge" name="Merge Paths">
      <bpmn:incoming>from_approval</bpmn:incoming>
      <bpmn:incoming>from_auto</bpmn:incoming>
      <bpmn:outgoing>to_end</bpmn:outgoing>
    </bpmn:exclusiveGateway>

    <!-- End -->
    <bpmn:endEvent id="end" name="Complete">
      <bpmn:incoming>to_end</bpmn:incoming>
    </bpmn:endEvent>

    <!-- Escalation End -->
    <bpmn:endEvent id="escalation_end" name="Escalated">
      <bpmn:incoming>to_escalation</bpmn:incoming>
    </bpmn:endEvent>

    <!-- Sequence Flows -->
    <bpmn:sequenceFlow id="to_extract" sourceRef="start" targetRef="extract" />
    <bpmn:sequenceFlow id="to_check" sourceRef="extract" targetRef="check_amount" />

    <bpmn:sequenceFlow id="high_value" sourceRef="check_amount" targetRef="manager_approval">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
        extracted_data.total > 1000
      </bpmn:conditionExpression>
    </bpmn:sequenceFlow>

    <bpmn:sequenceFlow id="low_value" sourceRef="check_amount" targetRef="auto_approve">
      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">
        extracted_data.total &lt;= 1000
      </bpmn:conditionExpression>
    </bpmn:sequenceFlow>

    <bpmn:sequenceFlow id="from_approval" sourceRef="manager_approval" targetRef="merge" />
    <bpmn:sequenceFlow id="from_auto" sourceRef="auto_approve" targetRef="merge" />
    <bpmn:sequenceFlow id="to_end" sourceRef="merge" targetRef="end" />
    <bpmn:sequenceFlow id="to_escalation" sourceRef="approval_timeout" targetRef="escalation_end" />

  </bpmn:process>

  <!-- Diagram Interchange for Visual Rendering -->
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="invoice_processing">
      <!-- Start Event -->
      <bpmndi:BPMNShape id="start_di" bpmnElement="start">
        <dc:Bounds x="179" y="99" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="160" y="142" width="75" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>

      <!-- Extract Task -->
      <bpmndi:BPMNShape id="extract_di" bpmnElement="extract">
        <dc:Bounds x="270" y="77" width="100" height="80" />
      </bpmndi:BPMNShape>

      <!-- Check Amount Gateway -->
      <bpmndi:BPMNShape id="check_amount_di" bpmnElement="check_amount" isMarkerVisible="true">
        <dc:Bounds x="425" y="92" width="50" height="50" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="413" y="149" width="75" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>

      <!-- Manager Approval Task (upper branch) -->
      <bpmndi:BPMNShape id="manager_approval_di" bpmnElement="manager_approval">
        <dc:Bounds x="530" y="0" width="100" height="80" />
      </bpmndi:BPMNShape>

      <!-- Approval Timeout Boundary Event -->
      <bpmndi:BPMNShape id="approval_timeout_di" bpmnElement="approval_timeout">
        <dc:Bounds x="562" y="62" width="36" height="36" />
      </bpmndi:BPMNShape>

      <!-- Auto Approve Task (lower branch) -->
      <bpmndi:BPMNShape id="auto_approve_di" bpmnElement="auto_approve">
        <dc:Bounds x="530" y="160" width="100" height="80" />
      </bpmndi:BPMNShape>

      <!-- Merge Gateway -->
      <bpmndi:BPMNShape id="merge_di" bpmnElement="merge" isMarkerVisible="true">
        <dc:Bounds x="685" y="92" width="50" height="50" />
      </bpmndi:BPMNShape>

      <!-- End Event -->
      <bpmndi:BPMNShape id="end_di" bpmnElement="end">
        <dc:Bounds x="792" y="99" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="786" y="142" width="48" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>

      <!-- Escalation End Event -->
      <bpmndi:BPMNShape id="escalation_end_di" bpmnElement="escalation_end">
        <dc:Bounds x="562" y="152" width="36" height="36" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="554" y="195" width="52" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNShape>

      <!-- Sequence Flow Edges -->
      <bpmndi:BPMNEdge id="to_extract_di" bpmnElement="to_extract">
        <di:waypoint x="215" y="117" />
        <di:waypoint x="270" y="117" />
      </bpmndi:BPMNEdge>

      <bpmndi:BPMNEdge id="to_check_di" bpmnElement="to_check">
        <di:waypoint x="370" y="117" />
        <di:waypoint x="425" y="117" />
      </bpmndi:BPMNEdge>

      <bpmndi:BPMNEdge id="high_value_di" bpmnElement="high_value">
        <di:waypoint x="450" y="92" />
        <di:waypoint x="450" y="40" />
        <di:waypoint x="530" y="40" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="460" y="22" width="60" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>

      <bpmndi:BPMNEdge id="low_value_di" bpmnElement="low_value">
        <di:waypoint x="450" y="142" />
        <di:waypoint x="450" y="200" />
        <di:waypoint x="530" y="200" />
        <bpmndi:BPMNLabel>
          <dc:Bounds x="460" y="182" width="60" height="14" />
        </bpmndi:BPMNLabel>
      </bpmndi:BPMNEdge>

      <bpmndi:BPMNEdge id="from_approval_di" bpmnElement="from_approval">
        <di:waypoint x="630" y="40" />
        <di:waypoint x="710" y="40" />
        <di:waypoint x="710" y="92" />
      </bpmndi:BPMNEdge>

      <bpmndi:BPMNEdge id="from_auto_di" bpmnElement="from_auto">
        <di:waypoint x="630" y="200" />
        <di:waypoint x="710" y="200" />
        <di:waypoint x="710" y="142" />
      </bpmndi:BPMNEdge>

      <bpmndi:BPMNEdge id="to_end_di" bpmnElement="to_end">
        <di:waypoint x="735" y="117" />
        <di:waypoint x="792" y="117" />
      </bpmndi:BPMNEdge>

      <bpmndi:BPMNEdge id="to_escalation_di" bpmnElement="to_escalation">
        <di:waypoint x="580" y="98" />
        <di:waypoint x="580" y="152" />
      </bpmndi:BPMNEdge>
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>

</bpmn:definitions>
```

---

## Timer Format Reference

### ISO 8601 Durations

| Format | Example | Meaning |
|--------|---------|---------|
| `PTnS` | `PT30S` | 30 seconds |
| `PTnM` | `PT15M` | 15 minutes |
| `PTnH` | `PT2H` | 2 hours |
| `PnD` | `P1D` | 1 day |
| `PnW` | `P1W` | 1 week |
| `PnM` | `P1M` | 1 month |
| Combined | `P1DT2H30M` | 1 day, 2 hours, 30 minutes |

### Cycle Expressions

```xml
<!-- Every day at 9 AM, starting Jan 1, 2024 -->
<bpmn:timeCycle>R/2024-01-01T09:00:00Z/P1D</bpmn:timeCycle>

<!-- Every hour, 10 times -->
<bpmn:timeCycle>R10/PT1H</bpmn:timeCycle>

<!-- Every Monday at 8 AM -->
<bpmn:timeCycle>R/2024-01-01T08:00:00Z/P1W</bpmn:timeCycle>
```

### Date/Time

```xml
<!-- Specific date/time -->
<bpmn:timeDate>2024-12-31T23:59:59Z</bpmn:timeDate>
```

---

## Condition Expression Syntax

### Comparison Operators

```xml
<bpmn:conditionExpression>amount > 1000</bpmn:conditionExpression>
<bpmn:conditionExpression>status == "approved"</bpmn:conditionExpression>
<bpmn:conditionExpression>count >= 5</bpmn:conditionExpression>
<bpmn:conditionExpression>error != null</bpmn:conditionExpression>
```

### Boolean Operators

```xml
<bpmn:conditionExpression>amount > 1000 and urgent == true</bpmn:conditionExpression>
<bpmn:conditionExpression>category == "travel" or category == "meals"</bpmn:conditionExpression>
<bpmn:conditionExpression>not rejected</bpmn:conditionExpression>
```

### Membership

```xml
<bpmn:conditionExpression>status in ["approved", "pending"]</bpmn:conditionExpression>
<bpmn:conditionExpression>category not in ["blocked", "archived"]</bpmn:conditionExpression>
```

### Object Access

```xml
<bpmn:conditionExpression>result.confidence > 0.8</bpmn:conditionExpression>
<bpmn:conditionExpression>data.items[0].status == "ready"</bpmn:conditionExpression>
```

### Functions

```xml
<bpmn:conditionExpression>len(items) > 0</bpmn:conditionExpression>
<bpmn:conditionExpression>sum(amounts) > 10000</bpmn:conditionExpression>
```

### XML Escaping

Remember to escape special characters:

| Character | Escape |
|-----------|--------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |

```xml
<bpmn:conditionExpression>amount &lt;= 1000</bpmn:conditionExpression>
```

---

## Further Reading

- Periscope BPMN Extensions Reference
- Periscope Variables and Data Flow Guide
- Periscope Temporal Concepts Guide
- [BPMN 2.0 Specification](https://www.omg.org/spec/BPMN/2.0/)
