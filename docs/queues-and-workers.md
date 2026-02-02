# Task Queues and Workers Guide

This document explains the Periscope task queue architecture, worker configuration, and subscription tier limits.

## Overview

Periscope uses a **multi-tenant queue system** built on Temporal. Each subscription tier has different resource allocations and capabilities.

---

## Subscription Tiers

### Tier Comparison

| Feature | Free | Starter | Professional | Enterprise |
|---------|------|---------|--------------|------------|
| Max Concurrent Workflows | 5 | 20 | 100 | 500 |
| Max Daily Workflows | 100 | 1,000 | 10,000 | Unlimited |
| Max Concurrent Activities | 20 | 50 | 200 | 1,000 |
| Priority Queue | No | No | Yes | Yes |
| Dedicated Namespace | No | No | No | Yes |
| Custom Queue Names | No | No | No | Yes |
| SLA Guarantee | None | 99.5% | 99.9% | 99.99% |

---

## Available Task Queues

### Free Tier Queues

| Queue | Purpose | Concurrency |
|-------|---------|-------------|
| `free-default-queue` | General purpose workflows | 20 activities, 5 workflows |
| `free-ai-queue` | AI agent workflows | 10 activities, 3 workflows |
| `free-integration-queue` | Data integration workflows | 10 activities, 3 workflows |

### Starter Tier Queues

| Queue | Purpose | Concurrency |
|-------|---------|-------------|
| `starter-default-queue` | General purpose workflows | 50 activities, 20 workflows |
| `starter-ai-queue` | AI agent workflows | 25 activities, 10 workflows |
| `starter-integration-queue` | Data integration workflows | 25 activities, 10 workflows |

### Professional Tier Queues

| Queue | Purpose | Concurrency |
|-------|---------|-------------|
| `pro-default-queue` | General purpose workflows | 200 activities, 100 workflows |
| `pro-ai-queue` | AI agent workflows | 100 activities, 50 workflows |
| `pro-priority-queue` | High-priority workflows | 50 activities, 25 workflows |
| `pro-integration-queue` | Data integration workflows | 75 activities, 30 workflows |

### Enterprise Tier Queues

Enterprise organizations get **dedicated queues** with custom naming:

| Queue Pattern | Purpose | Concurrency |
|---------------|---------|-------------|
| `{org-slug}-default-queue` | General purpose | 500 activities, 200 workflows |
| `{org-slug}-ai-queue` | AI agent workflows | 200 activities, 100 workflows |
| `{org-slug}-priority-queue` | High-priority | 100 activities, 50 workflows |
| `{org-slug}-integration-queue` | Data integration | 150 activities, 75 workflows |

---

## Queue Selection

### Automatic Queue Routing

When starting a workflow, Periscope automatically routes to the appropriate queue based on:

1. **Organization tier** - Determines base queue prefix
2. **Workflow type** - Default, AI, or integration
3. **Priority** - Normal or high (Professional/Enterprise only)

### Using Default Queue

```python
create_workflow(
    workflow_type="expense_approval",
    input_data={...}
)
# Routes to tier-appropriate default queue
```

### Specifying Workflow Type

```python
create_workflow(
    workflow_type="document_extraction",
    input_data={...},
    task_queue="ai"  # Routes to tier-ai-queue
)
```

### Using Priority Queue (Pro/Enterprise)

```python
create_workflow(
    workflow_type="urgent_approval",
    input_data={...},
    task_queue="priority"  # Routes to tier-priority-queue
)
```

---

## Worker Configuration

### Worker Pools

Each queue has a dedicated worker pool with configurable resources:

#### Free Tier Workers

```
free-default:
  Min workers: 1
  Max workers: 2
  Memory per worker: 256MB
  CPU per worker: 0.5

free-ai:
  Min workers: 1
  Max workers: 2
  Memory per worker: 512MB
  CPU per worker: 1.0

free-integration:
  Min workers: 1
  Max workers: 2
  Memory per worker: 256MB
  CPU per worker: 0.5
```

#### Professional Tier Workers

```
pro-default:
  Min workers: 2
  Max workers: 10
  Memory per worker: 1024MB
  CPU per worker: 2.0

pro-ai:
  Min workers: 2
  Max workers: 8
  Memory per worker: 2048MB
  CPU per worker: 2.0

pro-priority:
  Min workers: 2
  Max workers: 5
  Memory per worker: 1024MB
  CPU per worker: 2.0

pro-integration:
  Min workers: 1
  Max workers: 4
  Memory per worker: 512MB
  CPU per worker: 1.0
```

#### Enterprise Tier Workers

```
{org}-default:
  Min workers: 5
  Max workers: 25
  Memory per worker: 2048MB
  CPU per worker: 2.0

{org}-ai:
  Min workers: 3
  Max workers: 15
  Memory per worker: 4096MB
  CPU per worker: 4.0

{org}-priority:
  Min workers: 3
  Max workers: 10
  Memory per worker: 2048MB
  CPU per worker: 2.0

{org}-integration:
  Min workers: 2
  Max workers: 8
  Memory per worker: 1024MB
  CPU per worker: 1.5
```

### Auto-Scaling

Workers scale automatically based on queue utilization:

| Threshold | Action |
|-----------|--------|
| > 80% utilization | Scale up (add workers) |
| < 20% utilization | Scale down (remove workers) |

Health checks run every 30 seconds with automatic recovery after 3 consecutive failures.

---

## Timeouts and Retry Policies

### Default Timeouts

| Timeout Type | Default Value |
|--------------|---------------|
| Activity Start-to-Close | 10 minutes |
| Activity Heartbeat | 30 seconds |
| Workflow Execution | 24 hours |

### Default Retry Policy

```
Initial interval: 1 second
Maximum interval: 1 minute
Maximum attempts: 3
Backoff coefficient: 2.0
```

**Retry sequence:**
1. First retry: 1 second
2. Second retry: 2 seconds
3. Third retry: 4 seconds
4. Fail after 3 attempts

### Priority Queue Retry Policy (Pro/Enterprise)

More aggressive retry for critical workflows:

```
Initial interval: 500 milliseconds
Maximum interval: 30 seconds
Maximum attempts: 5
Backoff coefficient: 1.5
```

---

## Namespace Configuration

### Shared Namespaces

| Tier | Namespace |
|------|-----------|
| Free | `periscope-prod` |
| Starter | `periscope-prod` |
| Professional | `periscope-prod` |

### Dedicated Namespaces (Enterprise)

Enterprise organizations get isolated namespaces:
- `{org-slug}-prod` for production
- Complete workflow isolation
- Custom retention policies
- Dedicated monitoring

---

## Circuit Breaker

Prevents cascade failures when services are unhealthy:

| Setting | Value |
|---------|-------|
| Enable | true (default) |
| Failure threshold | 5 consecutive failures |
| Recovery timeout | 5 minutes |

When triggered:
1. Circuit opens (no new requests)
2. Wait 5 minutes
3. Allow single test request
4. If success, circuit closes
5. If failure, restart timeout

---

## Monitoring Queues

### Queue Statistics

```python
get_deployment_stats()

# Returns:
{
    "total_deployments": 45,
    "static_workflows": 12,
    "generated_workflows": 33,
    "deployment_status_counts": {
        "active": 42,
        "pending": 2,
        "failed": 1
    },
    "task_queues": [
        "free-default-queue",
        "free-ai-queue",
        "pro-default-queue"
    ]
}
```

### Worker Status

```python
get_worker_status()

# Returns worker health, active workflows, queue depths
```

### Queue Health

```python
get_deployment_health()

# Returns overall system health including:
# - Worker availability
# - Queue depths
# - Error rates
# - Latency metrics
```

---

## Choosing the Right Queue

### Decision Matrix

| Workflow Type | Queue | When to Use |
|---------------|-------|-------------|
| General business processes | `default` | Standard workflows, approvals |
| AI/ML operations | `ai` | Document processing, classification |
| Data pipelines | `integration` | ETL, data sync, bulk operations |
| Time-sensitive | `priority` | Urgent approvals, SLA-bound tasks |

### AI Queue Characteristics

- Higher memory allocation (for model loading)
- Longer default timeouts (AI can be slow)
- Optimized for burst workloads
- Better suited for LLM operations

### Integration Queue Characteristics

- Optimized for I/O operations
- Good for database-heavy workflows
- Handles bulk data efficiently
- Lower memory, higher throughput

### Priority Queue Benefits

- Faster retry policies
- Dedicated worker pool
- Higher resource allocation
- Never starved by regular workloads

---

## Quota Management

### Checking Current Usage

```python
# Via MCP context tools
get_current_context()

# Returns organization and project context
# Including current tier limits
```

### Quota Enforcement

When quota is exceeded:
1. New workflow creation blocked
2. Error returned with quota details
3. Running workflows continue
4. Queued workflows continue

### Upgrading Tiers

Contact Periscope support to upgrade:
- Free → Starter: Self-service
- Starter → Professional: Sales assisted
- Professional → Enterprise: Custom agreement

---

## Process Deployment

### Selecting Queue at Deployment

```python
deploy_process(
    process_id="<uuid>",
    temporal_workflow_type="ExpenseApprovalWorkflow",
    task_queue="pro-default-queue"  # Explicit queue
)
```

### Default Queue Resolution

If not specified, queue is resolved from:
1. Process configuration
2. Organization tier
3. Workflow type hint
4. Falls back to `free-default-queue`

---

## Best Practices

### 1. Match Queue to Workload

Use AI queue for AI agents, integration queue for data pipelines:
```python
# Good: AI agent on AI queue
deploy_process(..., task_queue="ai")

# Bad: AI agent on default queue (may timeout)
deploy_process(..., task_queue="default")
```

### 2. Use Priority for Critical Paths

Reserve priority queue for business-critical workflows:
```python
# Critical approval that affects revenue
create_workflow(
    workflow_type="sales_deal_approval",
    task_queue="priority"
)
```

### 3. Monitor Queue Depths

High queue depth indicates:
- Need more workers
- Workflows taking too long
- Possible quota issues

### 4. Set Appropriate Timeouts

Match timeouts to expected duration:
```xml
<periscope:TimeoutConfig startToCloseTimeout="PT2M" />
```

### 5. Configure Retry Policies

Customize retry for your use case:
```xml
<periscope:RetryPolicy
  maxAttempts="5"
  initialInterval="5s"
  backoffCoefficient="1.5" />
```

---

## Troubleshooting

### Workflow Not Starting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Queued indefinitely | No available workers | Check worker status |
| Quota exceeded | Hit tier limits | Upgrade tier or wait |
| Queue not found | Wrong queue name | Use valid queue name |

### Slow Execution

| Symptom | Cause | Solution |
|---------|-------|----------|
| High latency | Queue backlog | Scale workers or upgrade tier |
| Timeouts | Activity too slow | Increase timeout or optimize |
| Retries | Transient failures | Check error logs |

### Worker Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Workers unavailable | Circuit breaker open | Wait for recovery or check health |
| Workers crashing | Resource exhaustion | Check memory/CPU limits |
| Workflows not registering | Discovery not run | Reload workflows |

---

## Further Reading

- Periscope Temporal Concepts Guide
- Periscope Process Deployment Guide
- Temporal Documentation
