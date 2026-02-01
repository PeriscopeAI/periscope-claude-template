---
name: function
description: Create and manage RestrictedPython script functions for deterministic workflow logic
delegates-to: integration-specialist
---

# /function - Create Script Functions

Use this skill to create serverless Python functions that execute within workflows for deterministic operations.

## What Script Functions Do

Script functions provide **sandboxed Python execution** for:
- Mathematical calculations and data transformations
- Business rule validation
- JSON/data manipulation
- Date/time calculations
- Text processing and formatting

## CRITICAL: Function Signature Requirement

**All functions MUST use this exact signature:**

```python
def execute(input_data: dict) -> dict:
    # Your logic here
    return {"result": value}
```

- Function name MUST be `execute`
- Parameter MUST be `input_data: dict`
- Return type MUST be `dict`
- Access inputs via `input_data.get("param_name")`

## When to Use Functions vs Agents

| Need | Solution |
|------|----------|
| AI reasoning, judgment | Use an Agent |
| Deterministic calculation | Use a Function |
| Pattern matching, rules | Use a Function |
| External API calls | Use MCP Server |

## RestrictedPython Constraints

Functions run in a security sandbox with limitations:
- No file system access
- No network calls
- No imports (except safe builtins)
- No exec/eval
- Limited to safe operations

## Available Built-ins

```python
# Allowed modules
math, datetime, json, re, decimal, collections

# Allowed builtins
len, str, int, float, bool, list, dict, tuple, set
range, enumerate, zip, map, filter, sorted, sum, min, max
```

## How to Create a Function

1. **Describe your need**: "Calculate variance between invoice and PO"
2. **Define inputs/outputs**: What data comes in, what goes out
3. **Test**: Validate with sample data
4. **Publish**: Make available for workflows

## Function Templates

### Variance Calculator
```python
def execute(input_data: dict) -> dict:
    """Calculate variance between invoice and PO amounts."""
    invoice_total = input_data.get("invoice_total", 0)
    po_total = input_data.get("po_total", 0)

    variance = invoice_total - po_total
    variance_pct = (variance / po_total * 100) if po_total else 0

    return {
        "variance_amount": round(variance, 2),
        "variance_percentage": round(variance_pct, 2),
        "exceeds_threshold": abs(variance_pct) > 5
    }
```

### Business Rule Validator
```python
def execute(input_data: dict) -> dict:
    """Validate expense claim against business rules."""
    amount = input_data.get("amount", 0)
    category = input_data.get("category", "")
    receipt_present = input_data.get("receipt_present", False)

    errors = []
    if amount <= 0:
        errors.append("Amount must be positive")
    if amount > 100 and not receipt_present:
        errors.append("Receipt required for amounts over $100")
    if category not in ["travel", "supplies", "meals", "other"]:
        errors.append(f"Invalid category: {category}")

    return {"valid": len(errors) == 0, "errors": errors}
```

### JSON Path Extractor
```python
def execute(input_data: dict) -> dict:
    """Extract fields from nested data using dot notation paths."""
    data = input_data.get("data", {})
    paths = input_data.get("paths", [])

    def get_path(obj, path):
        for key in path.split('.'):
            if isinstance(obj, dict):
                obj = obj.get(key)
            else:
                return None
        return obj

    return {path: get_path(data, path) for path in paths}
```

### Date Calculator
```python
def execute(input_data: dict) -> dict:
    """Calculate due date adding business days."""
    from datetime import datetime, timedelta

    start_date = input_data.get("start_date")
    business_days = input_data.get("business_days", 0)

    date = datetime.strptime(start_date, "%Y-%m-%d")
    start = date
    days_added = 0

    while days_added < business_days:
        date += timedelta(days=1)
        if date.weekday() < 5:  # Monday = 0, Friday = 4
            days_added += 1

    return {
        "due_date": date.strftime("%Y-%m-%d"),
        "calendar_days": (date - start).days
    }
```

### Amount Formatter
```python
def execute(input_data: dict) -> dict:
    """Format currency amount for display."""
    from decimal import Decimal, ROUND_HALF_UP

    amount = input_data.get("amount", 0)
    currency = input_data.get("currency", "USD")

    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    d = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    symbol = symbols.get(currency, currency + " ")

    return {
        "formatted": f"{symbol}{d:,}",
        "numeric": float(d),
        "currency": currency
    }
```

### PO Line Item Validator
```python
def execute(input_data: dict) -> dict:
    """Validate purchase order line items."""
    lines = input_data.get("lines", [])

    errors = []
    total = 0

    for i, line in enumerate(lines):
        if not line.get("description"):
            errors.append(f"Line {i+1}: Missing description")
        if not isinstance(line.get("quantity"), (int, float)) or line["quantity"] <= 0:
            errors.append(f"Line {i+1}: Invalid quantity")
        if not isinstance(line.get("unit_price"), (int, float)) or line["unit_price"] < 0:
            errors.append(f"Line {i+1}: Invalid unit price")
        else:
            total += line.get("quantity", 0) * line.get("unit_price", 0)

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "line_count": len(lines),
        "calculated_total": round(total, 2)
    }
```

## Input/Output Schema

When creating functions, define schemas for validation:

```json
{
  "input_schema": {
    "type": "object",
    "properties": {
      "invoice_total": {"type": "number"},
      "po_total": {"type": "number"}
    },
    "required": ["invoice_total", "po_total"]
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "variance_amount": {"type": "number"},
      "variance_percentage": {"type": "number"},
      "exceeds_threshold": {"type": "boolean"}
    }
  }
}
```

## Function Lifecycle

1. **Draft**: Function is created but not usable in workflows
2. **Published**: Function is versioned and available for use
3. Each publish creates an **immutable version snapshot**

## MCP Tools for Functions

| Tool | Purpose |
|------|---------|
| `create_function` | Create new function (draft) |
| `list_functions` | List all functions |
| `get_function` | Get function details |
| `update_function` | Update draft function |
| `test_function` | Test with sample input |
| `publish_version` | Publish for workflow use |
| `list_versions` | Get version history |

## Output

Functions are stored in the Periscope database and can be:
- Called from BPMN script tasks via `periscope:ScriptTaskConfiguration`
- Referenced by `functionName` or `functionId`
- Used in workflow conditions
