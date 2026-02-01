# Process Variables and Data Flow

This document explains how to declare, manage, and use variables in Periscope workflows.

## Overview

Process variables are the data that flows through your workflow. They:
- Store workflow state
- Pass data between activities
- Control gateway decisions
- Enable human task forms
- Persist for audit compliance

---

## Variable Type System

Periscope supports a unified type system across BPMN, Temporal, and the database.

### Supported Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text values | `"Hello World"` |
| `integer` | Whole numbers | `42` |
| `number` | Decimal numbers | `3.14159` |
| `boolean` | True/false | `true` |
| `datetime` | ISO 8601 dates | `"2024-01-15T09:30:00Z"` |
| `array` | Lists of values | `["a", "b", "c"]` |
| `object` | Key-value pairs | `{"key": "value"}` |
| `any` | Any type (use sparingly) | Any valid JSON |

### Type Constraints

Variables can have validation constraints:

| Constraint | Applies To | Description |
|------------|------------|-------------|
| `min` | integer, number | Minimum value |
| `max` | integer, number | Maximum value |
| `minLength` | string | Minimum string length |
| `maxLength` | string | Maximum string length |
| `pattern` | string | Regex pattern to match |
| `enum` | any | List of allowed values |
| `minItems` | array | Minimum array length |
| `maxItems` | array | Maximum array length |
| `uniqueItems` | array | All items must be unique |

---

## Declaring Variables

### In BPMN

Declare variables in the process-level `extensionElements`:

```xml
<bpmn:process id="expense_approval" name="Expense Approval">
  <bpmn:extensionElements>
    <periscope:processVariables>
      <!-- Required input variable -->
      <periscope:processVariable
        name="expense_amount"
        type="number"
        required="true"
        isInput="true"
        description="Amount to be approved">
        <periscope:constraints>
          <periscope:constraint name="min" value="0" />
          <periscope:constraint name="max" value="100000" />
        </periscope:constraints>
      </periscope:processVariable>

      <!-- Optional input with default -->
      <periscope:processVariable
        name="currency"
        type="string"
        required="false"
        isInput="true"
        defaultValue="USD" />

      <!-- Computed output variable -->
      <periscope:processVariable
        name="approval_result"
        type="object"
        required="false"
        description="Approval decision and metadata" />

      <!-- Sensitive variable (masked in logs) -->
      <periscope:processVariable
        name="employee_ssn"
        type="string"
        sensitive="true" />

      <!-- Immutable variable (set once) -->
      <periscope:processVariable
        name="request_id"
        type="string"
        immutable="true" />
    </periscope:processVariables>
  </bpmn:extensionElements>
</bpmn:process>
```

### Variable Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | String | Required | Variable identifier (alphanumeric + underscore, max 64 chars) |
| `type` | String | Required | Data type from type system |
| `required` | Boolean | false | Must have value at workflow end |
| `isInput` | Boolean | false | Must be provided when starting workflow |
| `defaultValue` | String | null | Default value if not provided |
| `description` | String | null | Human-readable description |
| `sensitive` | Boolean | false | Mask value in logs and UI |
| `immutable` | Boolean | false | Cannot be changed after first set |
| `transient` | Boolean | false | Not persisted to database |
| `scope` | String | "process" | Visibility scope |

### Variable Name Rules

Valid names:
- Start with letter
- Contain letters, numbers, underscores
- Maximum 64 characters
- Case-sensitive

Reserved words (cannot use):
```
input, output, result, error, context, workflow, activity,
signal, timer, process, task, start, end, true, false, null
```

---

## Variable Scopes

Variables have visibility based on scope:

| Scope | Visibility | Use Case |
|-------|------------|----------|
| `process` | Entire process | Most variables |
| `subprocess` | Subprocess and children | Isolated subprocess data |
| `task` | Single task only | Temporary task state |

**Note:** Currently all variables are process-scoped. Subprocess and task scopes are planned for future releases.

---

## Data Flow Between Activities

### Input Mapping

Map process variables to activity inputs:

```xml
<bpmn:serviceTask id="analyze_document">
  <bpmn:extensionElements>
    <periscope:aIAgentConfiguration agentId="document-analyzer">
      <periscope:inputMapping source="document_url" target="file_url" />
      <periscope:inputMapping source="document_type" target="doc_type" />
    </periscope:aIAgentConfiguration>
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

| Attribute | Description |
|-----------|-------------|
| `source` | Process variable name |
| `target` | Activity parameter name |
| `mappingType` | `variable` (default), `literal`, `expression` |

### Output Mapping

Map activity results to process variables:

```xml
<periscope:outputMapping
  variable="extracted_data"
  errorVariable="extraction_error" />
```

| Attribute | Description |
|-----------|-------------|
| `variable` | Target process variable for success result |
| `errorVariable` | Target variable for error information |

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Process Variables                           │
│  { expense_amount: 500, currency: "USD", ... }                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   │
            ┌───────────────┐           │
            │ Input Mapping │           │
            │ source→target │           │
            └───────────────┘           │
                    │                   │
                    ▼                   │
            ┌───────────────┐           │
            │   Activity    │           │
            │   Executes    │           │
            └───────────────┘           │
                    │                   │
                    ▼                   │
            ┌───────────────┐           │
            │Output Mapping │           │
            │ result→var    │           │
            └───────────────┘           │
                    │                   │
                    └─────────┬─────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Updated Process Variables                        │
│  { expense_amount: 500, currency: "USD", approval_result: {...}}│
└─────────────────────────────────────────────────────────────────┘
```

---

## Expression Evaluation

Periscope uses safe expression evaluation for gateway conditions and variable transformations.

### Supported Operations

| Category | Operations |
|----------|------------|
| Arithmetic | `+`, `-`, `*`, `/`, `%`, `**` |
| Comparison | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Boolean | `and`, `or`, `not` |
| Membership | `in`, `not in` |
| Identity | `is`, `is not` |

### Safe Functions

```python
len()     # Length of string/list
str()     # Convert to string
int()     # Convert to integer
float()   # Convert to decimal
bool()    # Convert to boolean
max()     # Maximum value
min()     # Minimum value
sum()     # Sum of values
abs()     # Absolute value
round()   # Round number
sorted()  # Sort list
```

### Gateway Condition Examples

```xml
<!-- Simple comparison -->
<bpmn:conditionExpression>amount > 1000</bpmn:conditionExpression>

<!-- Multiple conditions -->
<bpmn:conditionExpression>
  amount > 1000 and category == "travel"
</bpmn:conditionExpression>

<!-- Membership check -->
<bpmn:conditionExpression>
  status in ["approved", "pending_final"]
</bpmn:conditionExpression>

<!-- Null check -->
<bpmn:conditionExpression>
  error_message == null or error_message == ""
</bpmn:conditionExpression>

<!-- Nested object access -->
<bpmn:conditionExpression>
  result.confidence > 0.8
</bpmn:conditionExpression>

<!-- Array length -->
<bpmn:conditionExpression>
  len(line_items) > 0
</bpmn:conditionExpression>
```

### Forbidden Patterns (Security)

These patterns are blocked for security:
```
__import__, __builtins__, eval, exec, compile,
open, file, input, globals, locals, getattr,
setattr, delattr, __class__, __dict__
```

---

## Variable Storage Architecture

Periscope uses a three-layer architecture for variables:

### Layer 1: Declarations (Design Time)

Stored when process is deployed:
- Variable metadata (name, type, constraints)
- Default values
- Flags (required, sensitive, immutable)

### Layer 2: Runtime Values (Execution Time)

Stored for each workflow execution:
- Current variable values
- Previous values (for rollback)
- Modification timestamps
- Modifier identity

### Layer 3: History (Audit Trail)

Complete change log:
- Old value → New value
- Who changed it
- When it was changed
- Which activity made the change

```
┌──────────────────────────────────────────────────────────────────┐
│  Declarations (process_variable_declarations)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ process_id | version | name | type | constraints | flags │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  Runtime Values (workflow_variable_values)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ execution_id | name | current_value | previous_value     │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  History (workflow_variable_history)                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ execution_id | name | old | new | modified_by | timestamp │  │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Starting Workflows with Variables

When starting a workflow, provide input variables:

### Via MCP Tool

```
create_workflow(
  workflow_type="expense_approval",
  input_data={
    "expense_amount": 1500.00,
    "currency": "USD",
    "category": "travel",
    "employee_id": "emp-123"
  }
)
```

### Required vs Optional

- Variables with `isInput="true"` and `required="true"` must be provided
- Variables with `defaultValue` use default if not provided
- Missing required inputs cause workflow start to fail

---

## Accessing Variables in Activities

### AI Agent Activities

Variables are available in `business_context`:

```python
# Agent receives
{
  "agent_config": {...},
  "business_context": {
    "expense_amount": 1500.00,
    "currency": "USD",
    "category": "travel"
  }
}
```

### Script Function Activities

Variables are passed via input mapping:

```python
def execute(input_data):
    amount = input_data["expense_amount"]
    currency = input_data["currency"]
    # Process data
    return {"formatted": f"{currency} {amount:,.2f}"}
```

### User Task Activities

Variables populate form fields and are updated by user input:

```xml
<periscope:formData>
  <periscope:field name="approved" type="boolean" />
  <periscope:field name="comments" type="text" />
</periscope:formData>
```

---

## Variable Best Practices

### 1. Declare All Variables

Always declare variables at the process level:
```xml
<periscope:processVariables>
  <!-- Declare everything -->
</periscope:processVariables>
```

### 2. Use Appropriate Types

Choose the most specific type:
- Use `integer` instead of `number` for whole numbers
- Use `enum` constraints for fixed values
- Use `object` for structured data

### 3. Mark Sensitive Data

Protect PII and secrets:
```xml
<periscope:processVariable name="ssn" type="string" sensitive="true" />
```

### 4. Use Immutable for IDs

Prevent accidental changes:
```xml
<periscope:processVariable name="order_id" type="string" immutable="true" />
```

### 5. Provide Descriptions

Document variable purpose:
```xml
<periscope:processVariable
  name="approval_threshold"
  type="number"
  description="Amount above which manager approval is required" />
```

### 6. Handle Null Values

Check for null in conditions:
```xml
<bpmn:conditionExpression>
  result != null and result.status == "approved"
</bpmn:conditionExpression>
```

### 7. Use Error Variables

Always capture potential errors:
```xml
<periscope:outputMapping
  variable="result"
  errorVariable="error" />
```

---

## Debugging Variables

### View in Temporal UI

1. Open `http://temporal-ui.periscope.local:8088`
2. Find your workflow execution
3. View activity inputs/outputs
4. Check signal payloads for user task data

### Check Variable History

Query the audit trail via MCP tools or API to see:
- When variable was changed
- What the previous value was
- Who made the change

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Variable null | Not initialized | Add default value or check isInput |
| Type mismatch | Wrong type in activity | Validate activity output schema |
| Immutable error | Tried to change | Check if variable should be immutable |
| Validation failed | Constraint violated | Check min/max/pattern constraints |

---

## Further Reading

- Periscope BPMN Extensions Reference
- Periscope Temporal Concepts Guide
- Periscope Script Functions Guide
