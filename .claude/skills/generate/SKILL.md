---
name: generate
description: Transform natural language requirements into a complete, running business process. The primary skill for going from idea to deployment.
delegates-to: process-generator
---

# /generate - Natural Language to Running Process

**The fastest path from idea to running workflow.**

Simply describe what you want, and the AI will:
1. Understand your requirements
2. Design the process flow
3. Create necessary AI agents and functions
4. Deploy to Temporal
5. Run a test execution

## How to Use

Just describe your business process in plain language:

```
/generate When an invoice arrives, extract the data, validate against
our PO database, flag anything over $1000 variance for CFO review,
otherwise route to AP for payment processing.
```

```
/generate Create an employee onboarding workflow that collects documents,
runs background check, sets up IT accounts, and schedules orientation.
```

```
/generate Build a customer support ticket triage that classifies urgency,
routes to the right team, and escalates if not responded within 4 hours.
```

## What You'll Get

After a few moments, you'll have:

### 1. Running Process
- Deployed to Temporal
- Ready to accept real data
- Visible in your dashboard

### 2. AI Agents (automatically created)
- Document extractors for understanding inputs
- Decision makers for routing logic
- Communication agents for notifications

### 3. Functions (automatically created)
- Validation rules
- Calculations
- Data transformations

### 4. Test Results
- Sample execution with test data
- Confirmation everything works

## Tips for Best Results

**Be Specific About:**
- What triggers the process (email, API, schedule, manual)
- Who needs to approve/review (roles, not people)
- What happens in exception cases
- Time limits or SLAs

**You Don't Need To Specify:**
- Technical implementation details
- BPMN elements or XML
- Agent configurations
- Temporal workflow settings

## Example Conversation

**You**:
```
/generate Create an expense approval workflow where employees submit
expenses with receipts. Amounts under $100 auto-approve. $100-500
needs manager approval. Over $500 needs finance approval. Send Slack
notifications at each stage.
```

**Periscope**:
```
✓ Analyzing requirements...
✓ Designing process flow...
✓ Creating expense-extractor agent (haiku)
✓ Creating validate-expense function
✓ Creating calculate-approval-level function
✓ Generating BPMN process...
✓ Deploying to Temporal...
✓ Running test execution...

## Expense Approval Process Created!

**Process ID**: proc_abc123
**Status**: Active

### Flow
[Submit] → [Extract Receipt] → [Validate] → [Route by Amount]
                                                ↓
                              [$0-100: Auto] [$100-500: Manager] [$500+: Finance]
                                                ↓
                                           [Notify via Slack]

### Components Created
- 1 AI Agent: expense-extractor
- 2 Functions: validate-expense, calculate-approval-level
- 3 User Tasks: manager-review, finance-review, submitter-fix

### Test Execution
- Input: $250 meal expense with receipt
- Path: Manager approval route
- Result: ✓ Completed successfully

### Next Steps
1. Start processing real expenses:
   /workflow start expense-approval

2. View pending approvals:
   /task list

3. Monitor in dashboard:
   http://localhost:3000/processes/proc_abc123
```

## After Generation

Your process is live! Use these skills to operate it:

| Need | Skill |
|------|-------|
| Start a workflow | `/workflow start [name]` |
| Check status | `/workflow status [id]` |
| Handle approvals | `/task` |
| Diagnose issues | `/analyze` |
| Improve performance | `/optimize` |

## Regenerating or Modifying

Made a mistake or need changes? Just describe what's different:

```
/generate Update expense-approval to also require VP approval for
anything over $5000
```

The AI will modify the existing process while preserving what works.
