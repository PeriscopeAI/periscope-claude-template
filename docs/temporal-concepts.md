# Temporal Workflow Concepts for Periscope

This document explains how Periscope uses Temporal for workflow execution and how BPMN elements map to Temporal constructs.

## Overview

Periscope translates BPMN process definitions into Temporal workflows. Understanding this mapping helps you design processes that fully leverage Temporal's durability, reliability, and scalability.

## Core Temporal Concepts

### Workflows

A **Workflow** is a durable function that orchestrates activities and maintains state. In Periscope:

- Each deployed BPMN process becomes a Temporal workflow class
- Workflow state survives process restarts and infrastructure failures
- Workflows can run for seconds to months

**Key Properties:**
- **Deterministic**: Same inputs must produce same outputs
- **Durable**: State is preserved across failures
- **Idempotent**: Safe to retry on failure

### Activities

An **Activity** is a single unit of work that can fail and be retried. In Periscope:

- Each BPMN Service Task becomes a Temporal activity
- Activities can call external APIs, AI agents, databases
- Activities have configurable retry policies and timeouts

**Periscope Activity Types:**
| Activity | Purpose |
|----------|---------|
| AI Agent Activity | Execute PydanticAI agent |
| Script Activity | Execute RestrictedPython function |
| Webhook Activity | Call external HTTP endpoints |
| Email Activity | Send emails via SMTP |
| Variable Activity | Initialize/update process variables |

### Signals

A **Signal** is an asynchronous message sent to a running workflow. In Periscope:

- BPMN User Tasks wait for signals to complete
- Signal events trigger workflow state changes
- Used for human-in-the-loop interactions

### Timers

**Timers** pause workflow execution for a duration or until a specific time:

- BPMN Timer Events become Temporal timers
- Support ISO 8601 durations (`PT1H`, `P1D`)
- Can be used for deadlines, reminders, delays

### Child Workflows

**Child Workflows** are workflows started by a parent workflow:

- BPMN Subprocesses become child workflows
- BPMN Call Activities invoke reusable workflows
- Parent can wait for child or detach

---

## BPMN to Temporal Mapping

### Start Events

| BPMN Element | Temporal Construct | Notes |
|--------------|-------------------|-------|
| None Start Event | Workflow entry point | Default start |
| Timer Start Event | Scheduled workflow | Uses Temporal schedules |
| Message Start Event | Signal-triggered start | Workflow waits for signal |
| Signal Start Event | Signal-triggered start | Similar to message |

### Tasks

| BPMN Element | Temporal Construct | Notes |
|--------------|-------------------|-------|
| Service Task | Activity | Executes agent/function |
| User Task | Signal wait | Waits for human completion |
| Script Task | Activity | Executes Python function |
| Generic Task | Activity | Basic activity wrapper |

### Gateways

| BPMN Element | Temporal Construct | Notes |
|--------------|-------------------|-------|
| Exclusive Gateway | if/elif/else | Conditional branching |
| Parallel Gateway | asyncio.gather() | Concurrent execution |
| Inclusive Gateway | Multi-condition eval | Multiple paths possible |

### Events

| BPMN Element | Temporal Construct | Notes |
|--------------|-------------------|-------|
| Timer Event | workflow.sleep() | Duration-based delay |
| Message Event | Signal handler | Waits for external message |
| Signal Event | Signal handler | Workflow-to-workflow communication |
| Error End Event | raise Exception | Terminates with error |

### Subprocesses

| BPMN Element | Temporal Construct | Notes |
|--------------|-------------------|-------|
| Embedded Subprocess | Child workflow | Inline subprocess |
| Event Subprocess | Signal-triggered child | Activated by events |
| Call Activity | External workflow call | Reusable process |

---

## Workflow Execution Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                     Workflow Lifecycle                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. START                                                        │
│     ├── Workflow ID generated (UUID)                             │
│     ├── Input variables validated                                │
│     └── Process variables initialized                            │
│                                                                  │
│  2. RUNNING                                                      │
│     ├── Activities execute in sequence/parallel                  │
│     ├── Variables updated after each activity                    │
│     ├── Signals received for user tasks                          │
│     └── State persisted after each step                          │
│                                                                  │
│  3. WAITING (optional)                                           │
│     ├── Timer events (sleep)                                     │
│     ├── User task signals                                        │
│     └── External signals                                         │
│                                                                  │
│  4. COMPLETED / FAILED / CANCELLED                               │
│     ├── Final state recorded                                     │
│     ├── Output variables returned                                │
│     └── History preserved for audit                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Retry Policies

Activities can fail. Temporal automatically retries with configurable policies.

### Default Retry Policy

```python
RetryPolicy(
    initial_interval = timedelta(seconds=1),
    maximum_interval = timedelta(minutes=1),
    maximum_attempts = 3,
    backoff_coefficient = 2.0
)
```

**What this means:**
1. First retry after 1 second
2. Second retry after 2 seconds
3. Third retry after 4 seconds (capped at 1 minute)
4. Fail after 3 attempts

### Configuring in BPMN

```xml
<bpmn:extensionElements>
  <periscope:RetryPolicy
    maxAttempts="5"
    initialInterval="2s"
    backoffCoefficient="1.5"
    maximumInterval="30s" />
</bpmn:extensionElements>
```

### Retry vs Non-Retryable Errors

**Retryable** (automatic retry):
- Network timeouts
- Service temporarily unavailable
- Rate limiting

**Non-Retryable** (immediate failure):
- Validation errors
- Authorization failures
- Business rule violations

---

## Timeouts

### Activity Timeouts

| Timeout | Default | Purpose |
|---------|---------|---------|
| Start-to-Close | 10 minutes | Total activity duration |
| Heartbeat | 30 seconds | Long-running activity liveness |
| Schedule-to-Start | None | Time in queue before worker picks up |

### Workflow Timeout

| Timeout | Default | Purpose |
|---------|---------|---------|
| Execution Timeout | 24 hours | Maximum workflow duration |
| Run Timeout | None | Single run duration |

### Configuring Timeouts in BPMN

```xml
<bpmn:extensionElements>
  <periscope:TimeoutConfig
    startToCloseTimeout="PT5M"
    heartbeatTimeout="PT30S" />
</bpmn:extensionElements>
```

---

## Signals and User Tasks

When a workflow reaches a User Task:

1. Workflow pauses and waits for signal
2. Human task created in Periscope
3. User completes task via UI/API
4. Signal sent to workflow with completion data
5. Workflow resumes with signal payload

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Workflow   │────▶│  User Task   │────▶│   Workflow   │
│   (running)  │     │  (waiting)   │     │  (resumed)   │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │    Human     │
                     │  Completes   │
                     │    Task      │
                     └──────────────┘
```

---

## Determinism Requirements

Temporal workflows must be deterministic. Avoid:

| Bad Pattern | Why | Alternative |
|-------------|-----|-------------|
| `datetime.now()` | Non-deterministic | Use `workflow.now()` |
| `random.random()` | Non-deterministic | Pass random value as input |
| External API calls in workflow | Side effects | Move to activity |
| Global mutable state | State inconsistency | Use workflow state |

### What Happens on Replay

When a workflow is replayed (after restart):
1. Temporal replays from event history
2. All activities return cached results
3. Workflow must reach same state
4. Non-deterministic code breaks replay

---

## Error Handling Patterns

### Try-Catch in Gateways

Use exclusive gateways with error conditions:

```xml
<bpmn:exclusiveGateway id="check_error" name="Check Error">
  <bpmn:outgoing>success_flow</bpmn:outgoing>
  <bpmn:outgoing>error_flow</bpmn:outgoing>
</bpmn:exclusiveGateway>

<bpmn:sequenceFlow id="success_flow">
  <bpmn:conditionExpression>extraction_error == null</bpmn:conditionExpression>
</bpmn:sequenceFlow>

<bpmn:sequenceFlow id="error_flow">
  <bpmn:conditionExpression>extraction_error != null</bpmn:conditionExpression>
</bpmn:sequenceFlow>
```

### Boundary Error Events

Catch activity failures:

```xml
<bpmn:boundaryEvent id="handle_error" attachedToRef="risky_task">
  <bpmn:errorEventDefinition />
  <bpmn:outgoing>recovery_flow</bpmn:outgoing>
</bpmn:boundaryEvent>
```

### Error End Events

Fail workflow with specific error:

```xml
<bpmn:endEvent id="fail_end" name="Validation Failed">
  <bpmn:errorEventDefinition errorRef="ValidationError" />
</bpmn:endEvent>
```

---

## Parallel Execution

Parallel gateways run branches concurrently:

```
        ┌───────────────┐
        │ Parallel Fork │
        └───────┬───────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌───────┐   ┌───────┐   ┌───────┐
│Task A │   │Task B │   │Task C │
└───────┘   └───────┘   └───────┘
    │           │           │
    └───────────┼───────────┘
                │
        ┌───────▼───────┐
        │ Parallel Join │
        └───────────────┘
```

**Implementation:**
- All branches start simultaneously
- Join waits for ALL branches to complete
- If any branch fails, entire parallel block fails
- Use boundary events for partial completion handling

---

## Best Practices

### 1. Keep Activities Idempotent

Activities may be retried. Ensure:
- Same input produces same result
- Side effects are safe to repeat
- Use unique identifiers for external operations

### 2. Use Appropriate Timeouts

Set timeouts based on expected duration:
- AI agents: 1-5 minutes
- External APIs: 30s-2 minutes
- Script functions: 10-30 seconds

### 3. Handle Signals Gracefully

User tasks may take days. Ensure:
- Clear task descriptions
- Reasonable deadlines
- Escalation for overdue tasks

### 4. Monitor Event History Size

Long-running workflows accumulate history. For workflows > 10K events:
- Use Continue-as-New pattern
- Break into child workflows
- Archive completed data

### 5. Version Workflow Changes

When updating deployed workflows:
- Use workflow versioning
- Handle in-flight executions
- Test migration paths

---

## Debugging and Troubleshooting

### Temporal UI

Access at `http://temporal-ui.periscope.local:8088`:
- View workflow history
- See activity inputs/outputs
- Check retry attempts
- Inspect signal payloads

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Workflow stuck | Waiting for signal | Check user tasks |
| Activity retrying | Transient failure | Check retry policy |
| Non-determinism error | Code changed | Redeploy with versioning |
| Timeout exceeded | Slow activity | Increase timeout or optimize |

### Workflow History Events

Key events to understand:
- `WorkflowExecutionStarted` - Workflow initiated
- `ActivityTaskScheduled` - Activity queued
- `ActivityTaskCompleted` - Activity succeeded
- `SignalReceived` - Signal processed
- `WorkflowExecutionCompleted` - Workflow finished

---

## Further Reading

- [Temporal Documentation](https://docs.temporal.io/)
- [BPMN 2.0 Specification](https://www.omg.org/spec/BPMN/2.0/)
- Periscope BPMN Extensions Reference
- Periscope Variables and Data Flow Guide
