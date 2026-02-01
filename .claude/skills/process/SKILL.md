---
name: process
description: Design and create a new BPMN business process for Periscope
delegates-to: process-designer
---

# /process - Design a Business Process

Use this skill to design a new BPMN business process for the Periscope platform.

## What You Can Do

1. **Create a new process** - Design a BPMN workflow from scratch
2. **Validate BPMN** - Check your BPMN XML for errors
3. **Convert to Temporal** - Generate Temporal workflow code from BPMN
4. **Manage versions** - Track changes to your process definitions

## How to Use

Simply describe the business process you want to create. For example:

- "Create an expense approval workflow"
- "Design a document review process with multiple approvers"
- "Build an onboarding workflow for new employees"

## Process Design Steps

1. **Gather Requirements**
   - What triggers the process?
   - What steps are involved?
   - Who needs to approve/review?
   - What are the decision points?

2. **Design the Flow**
   - Start event
   - Service tasks (automated)
   - User tasks (human interaction)
   - Gateways (decisions)
   - End events

3. **Validate**
   - Check BPMN structure
   - Verify all paths lead to end events
   - Ensure sequence flows are connected

4. **Save to Workspace**
   - Save BPMN file to `workspace/processes/`

## Example Conversation

**User**: Create a leave request approval workflow

**Assistant**: I'll help you design a leave request approval process. Let me gather some requirements:

1. Who can submit leave requests?
2. Who needs to approve (manager, HR)?
3. What happens if rejected?
4. Should there be automatic notifications?

[Continues with design...]

## Delegated Agent

This skill delegates to the **process-designer** agent which has access to:
- `periscope-processes-dev` MCP server (18 tools)
- `periscope-context-dev` MCP server (5 tools)

## File Upload Flow (Required for BPMN)

Always use the file upload flow for BPMN operations:
1. `request_bpmn_upload` → get pre-signed URL
2. Upload file directly to MinIO
3. `create_process_from_file_ref` with file_id

This is the only way to create/update processes via MCP.

## Output

Your process will be saved to:
```
workspace/processes/<process-name>.bpmn
```
