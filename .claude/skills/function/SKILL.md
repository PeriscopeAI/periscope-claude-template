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
# Allowed
math, datetime, json, re, decimal, collections
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
def calculate_variance(invoice_total: float, po_total: float) -> dict:
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
def validate_expense(amount: float, category: str, receipt_present: bool) -> dict:
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
def extract_fields(data: dict, paths: list) -> dict:
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
from datetime import datetime, timedelta

def calculate_due_date(start_date: str, business_days: int) -> dict:
    date = datetime.strptime(start_date, "%Y-%m-%d")
    days_added = 0
    while days_added < business_days:
        date += timedelta(days=1)
        if date.weekday() < 5:  # Monday = 0, Friday = 4
            days_added += 1
    return {
        "due_date": date.strftime("%Y-%m-%d"),
        "calendar_days": (date - datetime.strptime(start_date, "%Y-%m-%d")).days
    }
```

### Amount Formatter
```python
from decimal import Decimal, ROUND_HALF_UP

def format_currency(amount: float, currency: str = "USD") -> dict:
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    d = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    symbol = symbols.get(currency, currency + " ")
    return {
        "formatted": f"{symbol}{d:,}",
        "numeric": float(d),
        "currency": currency
    }
```

## API Usage

### Create Function
```
POST /api/v1/orchestration/script-functions
{
  "name": "calculate_variance",
  "description": "Calculate variance between invoice and PO amounts",
  "code": "def calculate_variance(...): ...",
  "input_schema": {"invoice_total": "float", "po_total": "float"},
  "output_schema": {"variance_amount": "float", "variance_percentage": "float"}
}
```

### Test Function
```
POST /api/v1/orchestration/script-functions/{id}/test
{
  "test_input": {"invoice_total": 1050.00, "po_total": 1000.00}
}
```

### Publish Function
```
POST /api/v1/orchestration/script-functions/{id}/publish
```

## Example Conversation

**User**: Create a function to validate purchase order line items

**Assistant**: I'll create a validation function for PO line items:

```python
def validate_po_lines(lines: list) -> dict:
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

Want me to create this function and test it with sample data?

## Output

Functions are stored in the Periscope database and can be:
- Called from BPMN service tasks
- Invoked by AI agents as tools
- Used in workflow conditions
