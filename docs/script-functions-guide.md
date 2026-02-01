# Script Functions Guide

This document provides comprehensive details on creating, testing, and using RestrictedPython script functions in Periscope workflows.

## Overview

Script functions provide **sandboxed Python execution** for deterministic operations within workflows. They are ideal for:

- Mathematical calculations
- Data transformations
- Business rule validation
- Text processing
- Date/time operations

---

## Execution Environment

### Security Sandbox

Functions run in **RestrictedPython**, which provides:
- AST-level code restriction (blocks dangerous patterns at parse time)
- No OS-level isolation needed (language-level security)
- Thread-based execution (ThreadPoolExecutor with 4 workers)
- Asyncio-compatible with timeout enforcement

### Hard Limits

| Constraint | Value | Notes |
|------------|-------|-------|
| Default timeout | 30 seconds | Per execution |
| Maximum timeout | 60 seconds | Cannot be exceeded |
| Print output | 10,000 characters | Truncated after limit |
| Thread pool | 4 workers | Concurrent executions |
| Function name | 255 characters | Maximum length |
| Description | 2,000 characters | Maximum length |

---

## Available Modules

### Whitelisted Standard Library

| Module | Available Functions |
|--------|-------------------|
| `math` | All functions: `sqrt`, `sin`, `cos`, `tan`, `log`, `ceil`, `floor`, `pow`, `pi`, `e` |
| `decimal` | `Decimal`, `ROUND_HALF_UP` |
| `datetime` | `datetime`, `date`, `timedelta`, `timezone` |
| `json` | `loads`, `dumps` |
| `re` | `match`, `search`, `findall`, `sub`, `split`, `compile` |
| `collections` | `OrderedDict`, `Counter`, `defaultdict` |
| `itertools` | `chain`, `groupby`, `combinations`, `permutations` |
| `functools` | `reduce`, `partial` |
| `uuid` | `uuid4` |
| `hashlib` | `md5`, `sha256`, `sha1` |
| `base64` | `b64encode`, `b64decode`, `urlsafe_b64encode`, `urlsafe_b64decode` |
| `copy` | `copy`, `deepcopy` |
| `statistics` | `mean`, `median`, `stdev`, `variance` |
| `typing` | Type hints: `Any`, `Dict`, `List`, `Optional`, `Union`, etc. |

### Whitelisted Builtins

**Type Constructors:**
```python
str, int, float, bool, list, dict, set, tuple, frozenset, bytes
```

**Iteration & Sequences:**
```python
len, range, enumerate, zip, map, filter, sorted, reversed, next, iter, slice
```

**Math & Aggregation:**
```python
abs, all, any, divmod, max, min, sum, round, pow
```

**Type Checking:**
```python
type, isinstance, issubclass
```

**String & Conversion:**
```python
chr, ord, repr, hex, hash
```

**Special:**
```python
print  # Redirected to PrintCollector (captured, not sent to stdout)
```

---

## Blocked Operations

### Not Available

| Category | Blocked Items |
|----------|--------------|
| File System | `open`, `file`, `os`, `pathlib`, `shutil` |
| Network | `requests`, `urllib`, `socket`, `http` |
| Subprocess | `subprocess`, `os.system`, `exec`, `eval` |
| Introspection | `globals`, `locals`, `getattr`, `setattr`, `delattr` |
| Code Manipulation | `compile`, `__import__` (except via restricted importer) |
| Dangerous | `__builtins__`, `__class__`, `__dict__`, `__code__` |

### Why These Are Blocked

Functions execute in a shared process. Blocking these prevents:
- Data exfiltration (no network/file access)
- System compromise (no shell access)
- Resource exhaustion (timeouts enforced)
- State leakage (no global access)

---

## Function Signature

### Required Format

Functions must define an `execute` function:

```python
def execute(input_data: dict) -> dict:
    """
    Your function must:
    - Be named 'execute'
    - Accept a dict parameter
    - Return a dict
    """
    # Your logic here
    return {"result": "value"}
```

### Parameter Handling

**Single Parameter (recommended):**
```python
def execute(input_data):
    amount = input_data["amount"]
    rate = input_data.get("rate", 0.1)  # With default
    return {"total": amount * (1 + rate)}
```

**Named Parameters (unpacked automatically):**
```python
def execute(amount, rate=0.1):
    """Parameters unpacked from input dict"""
    return {"total": amount * (1 + rate)}
```

Accepted parameter names for single-param style:
- `input_data` (recommended)
- `data`
- `params`
- `input`
- `inputs`

---

## Input/Output Schemas

Define JSON schemas for type validation:

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "amount": {"type": "number", "minimum": 0},
    "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"]},
    "items": {
      "type": "array",
      "items": {"type": "object"}
    }
  },
  "required": ["amount"]
}
```

### Output Schema

```json
{
  "type": "object",
  "properties": {
    "total": {"type": "number"},
    "formatted": {"type": "string"},
    "valid": {"type": "boolean"}
  },
  "required": ["total"]
}
```

### Type Coercion

Form submissions send strings. Periscope auto-coerces:

| From | To | Recognized Values |
|------|----|--------------------|
| String | Number | Valid numeric strings |
| String | Boolean | `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off` |
| String | Array | Valid JSON array strings |
| String | Object | Valid JSON object strings |

---

## Versioning System

### Lifecycle

1. **Create** - Function created as draft (version 0)
2. **Develop** - Modify code, test with sample data
3. **Publish** - Create immutable version snapshot
4. **Use** - Reference specific version in workflows
5. **Update** - Modify draft, publish new version
6. **Deprecate** - Mark old versions as deprecated

### Version Properties

| Property | Description |
|----------|-------------|
| `version` | Auto-incrementing integer (1, 2, 3...) |
| `code` | Immutable snapshot of code at publish time |
| `code_hash` | SHA-256 hash for integrity verification |
| `change_notes` | Optional changelog for this version |
| `published_by` | User who published |
| `published_at` | Timestamp of publication |

### Using Specific Versions

```xml
<periscope:scriptTaskConfiguration
  functionId="calculate-totals"
  functionName="calculate_totals"
  version="2" />
```

Omitting `version` uses the latest published version.

---

## Creating Functions

### Via MCP Tool

```python
create_function(
    name="calculate_variance",
    description="Calculate variance between invoice and PO amounts",
    code='''
def execute(input_data):
    invoice = input_data["invoice_total"]
    po = input_data["po_total"]
    variance = invoice - po
    variance_pct = (variance / po * 100) if po else 0
    return {
        "variance_amount": round(variance, 2),
        "variance_percentage": round(variance_pct, 2),
        "exceeds_threshold": abs(variance_pct) > 5
    }
''',
    input_schema={
        "type": "object",
        "properties": {
            "invoice_total": {"type": "number"},
            "po_total": {"type": "number"}
        },
        "required": ["invoice_total", "po_total"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "variance_amount": {"type": "number"},
            "variance_percentage": {"type": "number"},
            "exceeds_threshold": {"type": "boolean"}
        }
    },
    category="finance",
    tags=["calculation", "variance"],
    visibility="organization"
)
```

### Testing Before Publishing

```python
test_function(
    function_id="<uuid>",
    input_data={
        "invoice_total": 1050.00,
        "po_total": 1000.00
    }
)

# Returns:
# {
#   "success": true,
#   "result": {
#     "variance_amount": 50.0,
#     "variance_percentage": 5.0,
#     "exceeds_threshold": false
#   },
#   "execution_time_ms": 12.5
# }
```

### Publishing

```python
publish_version(
    function_id="<uuid>",
    change_notes="Initial release - variance calculation"
)

# Returns:
# {
#   "version": 1,
#   "published_at": "2024-01-15T10:30:00Z",
#   "code_hash": "sha256:..."
# }
```

---

## Common Patterns

### Validation Functions

```python
def execute(input_data):
    """Validate expense claims"""
    amount = input_data.get("amount", 0)
    category = input_data.get("category", "")
    has_receipt = input_data.get("has_receipt", False)

    errors = []
    warnings = []

    if amount <= 0:
        errors.append("Amount must be positive")

    if amount > 100 and not has_receipt:
        errors.append("Receipt required for amounts over $100")

    if amount > 500:
        warnings.append("Amounts over $500 require manager approval")

    valid_categories = ["travel", "meals", "supplies", "equipment", "other"]
    if category not in valid_categories:
        errors.append(f"Invalid category. Must be one of: {valid_categories}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "requires_approval": amount > 500
    }
```

### Calculation Functions

```python
from decimal import Decimal, ROUND_HALF_UP

def execute(input_data):
    """Calculate invoice totals with tax"""
    line_items = input_data.get("line_items", [])
    tax_rate = Decimal(str(input_data.get("tax_rate", 0.10)))

    subtotal = Decimal("0")
    for item in line_items:
        qty = Decimal(str(item.get("quantity", 0)))
        price = Decimal(str(item.get("unit_price", 0)))
        subtotal += qty * price

    tax = (subtotal * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total = subtotal + tax

    return {
        "subtotal": float(subtotal),
        "tax": float(tax),
        "total": float(total),
        "line_count": len(line_items)
    }
```

### Data Transformation Functions

```python
import json
from datetime import datetime

def execute(input_data):
    """Transform raw data to standardized format"""
    raw = input_data.get("raw_data", {})

    # Normalize date formats
    date_str = raw.get("date", "")
    try:
        parsed = datetime.strptime(date_str, "%m/%d/%Y")
        normalized_date = parsed.strftime("%Y-%m-%d")
    except ValueError:
        normalized_date = None

    # Extract and clean fields
    result = {
        "vendor_name": raw.get("vendor", "").strip().upper(),
        "invoice_number": raw.get("inv_num", raw.get("invoice_number", "")),
        "date": normalized_date,
        "amount": float(raw.get("total", raw.get("amount", 0))),
        "currency": raw.get("currency", "USD").upper()[:3]
    }

    return {
        "transformed": result,
        "has_all_fields": all(result.values())
    }
```

### Date/Time Functions

```python
from datetime import datetime, timedelta

def execute(input_data):
    """Calculate business days and due dates"""
    start_str = input_data.get("start_date")
    business_days = input_data.get("business_days", 5)

    start = datetime.strptime(start_str, "%Y-%m-%d")
    current = start
    days_added = 0

    while days_added < business_days:
        current += timedelta(days=1)
        # Skip weekends (Monday = 0, Friday = 4)
        if current.weekday() < 5:
            days_added += 1

    calendar_days = (current - start).days

    return {
        "start_date": start.strftime("%Y-%m-%d"),
        "due_date": current.strftime("%Y-%m-%d"),
        "business_days": business_days,
        "calendar_days": calendar_days,
        "day_of_week": current.strftime("%A")
    }
```

### Text Processing Functions

```python
import re
import hashlib

def execute(input_data):
    """Extract and validate email addresses"""
    text = input_data.get("text", "")

    # Email regex pattern
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    emails = re.findall(pattern, text)
    unique_emails = list(set(emails))

    # Validate each email
    validated = []
    for email in unique_emails:
        email_lower = email.lower()
        validated.append({
            "email": email_lower,
            "domain": email_lower.split("@")[1],
            "hash": hashlib.sha256(email_lower.encode()).hexdigest()[:16]
        })

    return {
        "emails": validated,
        "count": len(validated),
        "has_emails": len(validated) > 0
    }
```

---

## Error Handling

### Error Types

| Error Type | Cause |
|------------|-------|
| `syntax_error` | Invalid Python syntax |
| `compilation_error` | RestrictedPython rejected code |
| `definition_error` | Error during function definition |
| `missing_function` | No `execute` function found |
| `runtime_error` | Exception during execution |
| `input_validation_error` | Input doesn't match schema |
| `output_validation_error` | Output doesn't match schema |
| `timeout` | Execution exceeded time limit |

### Execution Result

```python
{
    "success": False,
    "result": None,
    "error_type": "runtime_error",
    "error_message": "KeyError: 'missing_key'",
    "execution_time_ms": 15.2,
    "warnings": []
}
```

### Handling Errors in Code

```python
def execute(input_data):
    """Graceful error handling"""
    try:
        amount = input_data["amount"]
        rate = input_data.get("rate", 0.1)

        if rate < 0 or rate > 1:
            return {
                "success": False,
                "error": "Rate must be between 0 and 1"
            }

        result = amount * (1 + rate)
        return {
            "success": True,
            "result": round(result, 2)
        }
    except KeyError as e:
        return {
            "success": False,
            "error": f"Missing required field: {e}"
        }
    except (TypeError, ValueError) as e:
        return {
            "success": False,
            "error": f"Invalid data type: {e}"
        }
```

---

## Using in BPMN

### Script Task Configuration

```xml
<bpmn:scriptTask id="calculate_totals" name="Calculate Totals">
  <bpmn:extensionElements>
    <periscope:scriptTaskConfiguration
      functionId="invoice-calculator"
      functionName="calculate_invoice_totals"
      version="2"
      description="Calculate subtotal, tax, and total"
      outputVariable="invoice_totals">
      <periscope:scriptTaskInputMapping
        source="line_items"
        target="line_items"
        mappingType="variable" />
      <periscope:scriptTaskInputMapping
        source="tax_rate"
        target="tax_rate"
        mappingType="variable" />
    </periscope:scriptTaskConfiguration>
  </bpmn:extensionElements>
</bpmn:scriptTask>
```

### Referencing Versions

| Value | Behavior |
|-------|----------|
| `version="1"` | Use exactly version 1 |
| `version="latest"` | Use most recent published |
| (omitted) | Use most recent published |

---

## Multi-Tenancy

### Organization Scoping

Functions belong to an organization and project:
- Functions are visible within their organization
- Cross-organization function sharing not supported
- Use `visibility` to control access within org

### Visibility Options

| Visibility | Who Can Use |
|------------|-------------|
| `private` | Only the creator |
| `organization` | Anyone in the organization |

---

## Performance Tips

### 1. Minimize Iterations

```python
# Good: Single pass
def execute(input_data):
    items = input_data["items"]
    total = sum(item["amount"] for item in items)
    return {"total": total}

# Bad: Multiple passes
def execute(input_data):
    items = input_data["items"]
    total = 0
    for item in items:
        total += item["amount"]
    return {"total": total}
```

### 2. Use Built-in Functions

```python
# Good: Use built-ins
max_value = max(values)
sorted_items = sorted(items, key=lambda x: x["date"])

# Bad: Manual implementation
max_value = values[0]
for v in values:
    if v > max_value:
        max_value = v
```

### 3. Avoid Large String Concatenation

```python
# Good: Join
result = ",".join(strings)

# Bad: Concatenation in loop
result = ""
for s in strings:
    result += s + ","
```

### 4. Handle Missing Data Early

```python
def execute(input_data):
    # Validate early
    required = ["amount", "currency"]
    missing = [f for f in required if f not in input_data]
    if missing:
        return {"error": f"Missing fields: {missing}"}

    # Process with confidence
    ...
```

---

## Execution Statistics

Track function performance via MCP:

```python
get_function_stats(function_id="<uuid>")

# Returns:
{
    "total_executions": 1523,
    "success_count": 1498,
    "error_count": 20,
    "timeout_count": 5,
    "success_rate": 98.36,
    "avg_execution_time_ms": 28.5,
    "min_execution_time_ms": 5.2,
    "max_execution_time_ms": 145.8
}
```

---

## Further Reading

- Periscope Variables and Data Flow Guide
- Periscope BPMN Extensions Reference
- Periscope Temporal Concepts Guide
