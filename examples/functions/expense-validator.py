# Expense Validator Function
# A RestrictedPython-compatible script function for workflow use

def validate_expense(expense: dict) -> dict:
    """
    Validate an expense submission before processing.

    Args:
        expense: Dictionary with expense details
            - amount: float (required)
            - category: str (required)
            - receipt_url: str (optional)
            - description: str (optional)
            - date: str YYYY-MM-DD (required)

    Returns:
        Dictionary with validation results:
            - valid: bool
            - errors: list of error messages
            - approval_level: str (auto/manager/finance)
            - warnings: list of warning messages
    """
    errors = []
    warnings = []

    # Required field validation
    if not expense.get("amount"):
        errors.append("Amount is required")
    elif not isinstance(expense.get("amount"), (int, float)):
        errors.append("Amount must be a number")
    elif expense["amount"] <= 0:
        errors.append("Amount must be positive")

    valid_categories = ["travel", "meals", "supplies", "equipment", "training", "other"]
    category = expense.get("category", "").lower()
    if not category:
        errors.append("Category is required")
    elif category not in valid_categories:
        errors.append(f"Invalid category. Must be one of: {', '.join(valid_categories)}")

    if not expense.get("date"):
        errors.append("Date is required")
    else:
        # Basic date format validation
        date_str = expense.get("date", "")
        if len(date_str) != 10 or date_str[4] != "-" or date_str[7] != "-":
            errors.append("Date must be in YYYY-MM-DD format")

    # Amount-based receipt requirement
    amount = expense.get("amount", 0)
    if amount > 25 and not expense.get("receipt_url"):
        if amount > 100:
            errors.append("Receipt required for expenses over $100")
        else:
            warnings.append("Receipt recommended for expenses over $25")

    # Description requirement for large amounts
    if amount > 500 and not expense.get("description"):
        warnings.append("Description recommended for expenses over $500")

    # Determine approval level
    if amount < 100:
        approval_level = "auto"
    elif amount < 500:
        approval_level = "manager"
    else:
        approval_level = "finance"

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "approval_level": approval_level,
        "amount": amount,
        "category": category
    }


# Test cases for validation
if __name__ == "__main__":
    # These would be run via the script-functions test endpoint
    test_cases = [
        {
            "input": {"amount": 50, "category": "meals", "date": "2024-01-15"},
            "expected_valid": True,
            "expected_approval": "auto"
        },
        {
            "input": {"amount": 250, "category": "travel", "date": "2024-01-15", "receipt_url": "https://..."},
            "expected_valid": True,
            "expected_approval": "manager"
        },
        {
            "input": {"amount": 1500, "category": "equipment", "date": "2024-01-15"},
            "expected_valid": False,  # Missing receipt
            "expected_approval": "finance"
        }
    ]
