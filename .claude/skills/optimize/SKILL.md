---
name: optimize
description: Improve your processes automatically. Reduce costs, increase speed, fix recurring issues.
delegates-to: workflow-operator
---

# /optimize - Make Your Processes Better

Let AI analyze your running processes and suggest improvements.

## How to Use

```
/optimize expense-approval
```

```
/optimize --all
```

```
/optimize --cost
```

## What Gets Analyzed

### Performance
- Slow steps that could be faster
- Sequential work that could run in parallel
- Bottlenecks in human task completion

### Cost
- AI agents using expensive models when cheaper ones work
- Redundant agent calls
- Opportunities for caching

### Reliability
- Steps that frequently fail
- Timeout patterns
- Error handling gaps

### User Experience
- Long wait times for approvals
- Confusing task assignments
- Missing notifications

## Example Output

```
## Optimization Report: expense-approval

### Performance (3 improvements found)

1. **Parallelize notifications**
   Currently: Send Slack → Send Email (sequential)
   Suggested: Send both simultaneously
   Impact: -2 seconds per execution

2. **Cache vendor lookups**
   Currently: API call for every expense
   Suggested: Cache for 1 hour
   Impact: -500ms average, -80% API costs

3. **Auto-approve returning vendors**
   Pattern detected: Same vendor approved 20+ times
   Suggested: Skip manager for known vendors under $200
   Impact: 40% fewer manual approvals

### Cost (2 improvements found)

1. **Downgrade receipt extraction model**
   Currently: claude-sonnet ($0.003/call)
   Suggested: claude-haiku ($0.00025/call)
   Test results: 98% same accuracy
   Impact: -$45/month at current volume

2. **Batch similar expenses**
   Pattern: Multiple small expenses from same trip
   Suggested: Group into single approval
   Impact: -60% agent calls

### Reliability (1 improvement found)

1. **Add retry for Slack notifications**
   Current failure rate: 3%
   Suggested: 3 retries with backoff
   Impact: 99.9% delivery rate

### Ready to Apply?

Say "apply all" or specify which improvements:
- "apply performance improvements"
- "apply #1 and #3"
- "show me more details on #2"
```

## Automatic Optimization

Enable continuous improvement:

```
/optimize --enable-auto
```

With auto-optimization:
- Minor improvements applied automatically
- You're notified of changes
- Major changes require your approval
- All changes can be rolled back

## Optimization History

See what's been improved:

```
/optimize --history expense-approval
```

```
## Optimization History

| Date | Change | Impact |
|------|--------|--------|
| Jan 15 | Parallelized notifications | -2s latency |
| Jan 10 | Cached vendor lookups | -$32 cost |
| Jan 5 | Added Slack retry | 99.9% delivery |
```

## Cost-Focused Optimization

When budget matters most:

```
/optimize --cost --aggressive
```

This prioritizes cost reduction even if it slightly impacts other metrics.

## Performance-Focused Optimization

When speed matters most:

```
/optimize --performance --target 5s
```

Get recommendations to hit a specific latency target.
