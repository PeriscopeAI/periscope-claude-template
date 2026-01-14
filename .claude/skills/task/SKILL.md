---
name: task
description: View and manage human tasks assigned to you in Periscope workflows
delegates-to: task-handler
---

# /task - Manage Human Tasks

Use this skill to view and manage human tasks assigned to you in Periscope workflows.

## What You Can Do

1. **View tasks** - See tasks assigned to you
2. **Get details** - View task information and form fields
3. **Complete tasks** - Approve, reject, or submit data
4. **Delegate tasks** - Transfer to another user
5. **Add comments** - Discuss tasks with team

## How to Use

Describe what you want to do with tasks:

- "Show me my pending tasks"
- "What urgent tasks do I have?"
- "Complete task xyz with approval"
- "Delegate task abc to the finance team"
- "Add a comment to task 123"

## Task Views

### My Tasks
View all tasks assigned to you with filtering:
- By status: pending, in_progress, assigned
- By priority: urgent, high, medium, low
- By type: approval, review, data_entry, decision

### Task Statistics
Get a quick overview:
- Total assigned
- Pending count
- Completed today
- Overdue count

## Task Actions

### Complete Task
```
Complete task: task-uuid
Action: approve
Data: {"approved_amount": 5000}
Comment: "Approved after review"
```

### Delegate Task
```
Delegate task: task-uuid
To: user@company.com
Note: "Please review - needs finance expertise"
```

### Add Comment
```
Comment on task: task-uuid
Text: "I have questions about line item 3"
```

## Task Types

| Type | Actions |
|------|---------|
| approval | approve, reject |
| review | approve, reject, submit |
| data_entry | submit, complete |
| decision | complete with choice |

## Priority Levels

| Priority | Description |
|----------|-------------|
| urgent | Immediate attention required |
| high | Complete today |
| medium | Normal priority |
| low | When time permits |

## Delegated Agent

This skill delegates to the **task-handler** agent which has access to:
- `periscope-tasks-dev` MCP server (10 tools)
- `periscope-users-dev` MCP server (5 tools)
