---
name: analyze
description: Analyze workflow executions, diagnose failures, and get optimization recommendations
delegates-to: workflow-operator
---

# /analyze - Workflow Analysis & Diagnostics

Use this skill to understand workflow behavior, diagnose failures, and get optimization recommendations.

## What You Can Analyze

### 1. Failed Workflows
- Identify failure point in execution
- Understand error messages and stack traces
- Get root cause analysis
- Receive fix recommendations

### 2. Performance Issues
- Slow activity detection
- Bottleneck identification
- Resource utilization analysis
- Optimization suggestions

### 3. Process Patterns
- Execution frequency analysis
- Path distribution (which branches taken)
- Average duration by step
- User task completion times

## How to Use

### Diagnose a Failed Workflow
```
/analyze workflow wf-abc123
```

### Analyze Process Performance
```
/analyze process proc-xyz789 --last 7 days
```

### Compare Executions
```
/analyze compare wf-001 wf-002
```

## Diagnostic Output

### For Failed Workflows

```
## Workflow Diagnosis: wf-abc123

### Failure Summary
- **Status**: Failed
- **Failed At**: extract_invoice_data (Activity)
- **Error**: TimeoutError - Activity exceeded 30s timeout
- **Timestamp**: 2024-01-15 10:23:45 UTC

### Execution Path
1. ✓ Start Event (0.1s)
2. ✓ validate_input (0.3s)
3. ✗ extract_invoice_data (30.0s - TIMEOUT)
4. ○ approval_gateway (not reached)
5. ○ End Event (not reached)

### Root Cause Analysis
The `extract_invoice_data` activity is using the `invoice-extractor` agent
which calls OpenAI gpt-4o. The timeout indicates either:
1. Large document causing slow processing
2. OpenAI API latency issues
3. Agent prompt causing excessive token usage

### Recommendations
1. **Immediate**: Retry with extended timeout (60s)
2. **Short-term**: Add document size validation before extraction
3. **Long-term**: Switch to gpt-4o-mini for faster extraction

### Related Tools
- `get_workflow_history` - Full event history
- `update_agent_config` - Adjust agent timeout
- `get_agent_statistics` - Check agent performance
```

### For Process Performance

```
## Process Analysis: expense-approval

### Overview (Last 7 Days)
- **Executions**: 156
- **Success Rate**: 94.2%
- **Avg Duration**: 4.2 hours
- **Active Now**: 12

### Path Distribution
- Auto-approved (< $100): 45%
- Manager approved: 38%
- Finance approved: 12%
- Rejected: 5%

### Bottlenecks Identified
1. **manager_review** - Avg 3.1 hours wait time
   - Recommendation: Add escalation after 4 hours

2. **extract_receipt** - 8% failure rate
   - Recommendation: Add retry logic or fallback

### Optimization Suggestions
1. Add parallel notification to reduce wait time
2. Cache vendor lookup results
3. Consider async approval for repeat vendors
```

## Analysis Types

| Type | Command | Output |
|------|---------|--------|
| Single workflow | `/analyze workflow {id}` | Diagnosis report |
| Process overview | `/analyze process {id}` | Performance stats |
| Compare | `/analyze compare {id1} {id2}` | Difference report |
| Trends | `/analyze trends {process}` | Time-series analysis |

## Available Metrics

### Workflow Level
- Total duration
- Activity durations
- Wait times
- Retry counts
- Error messages

### Process Level
- Execution count
- Success/failure rates
- Path distribution
- Average duration by path
- User task completion times

### Agent Level
- Execution count
- Success rate
- Average latency
- Token usage
- Error patterns

## Example Conversations

**User**: Why did my expense workflow fail?

**Assistant**: Let me analyze the workflow.

[Runs get_workflow, get_workflow_history]

The workflow `wf-expense-001` failed at the `manager_review` user task. The error shows "Task deadline exceeded" - the manager didn't respond within the 24-hour SLA.

**Recommendations**:
1. Send reminder at 20 hours
2. Auto-escalate to backup approver at 24 hours
3. Consider shorter SLA for small amounts

---

**User**: My invoice processing is slow

**Assistant**: Let me analyze recent executions.

[Runs get_process_stats, list_workflow_executions]

Analysis of last 50 invoice workflows:
- Average duration: 8.3 minutes
- Slowest step: `extract_invoice_data` (6.2 min avg)

The extraction agent is using `gpt-4o` which is accurate but slow for this task. Since invoice extraction is structured, switching to `gpt-4o-mini` could reduce this to ~45 seconds with similar accuracy for standard invoices.

Want me to update the agent configuration?

## Reference Documentation

- [Troubleshooting Guide](../../../docs/troubleshooting.md) - Common issues and fixes
- [Temporal Concepts](../../../docs/temporal-concepts.md) - Workflow fundamentals

## Delegated Agent

This skill delegates to the **workflow-operator** agent which has access to:
- `periscope-workflows` - Execution history and status
- `periscope-tasks` - User task timing data
