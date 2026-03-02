import re
from typing import Any


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Returns:
        True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def validate_name(name: str) -> bool:
    """
    Validate that name is not empty and has reasonable length.
    
    Returns:
        True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    name = name.strip()
    return 2 <= len(name) <= 100


def validate_age(age: Any) -> bool:
    """
    Validate age is a positive number within reasonable range.
    
    Returns:
        True if valid, False otherwise
    """
    try:
        age_int = int(age)
        return 0 <= age_int <= 150
    except (ValueError, TypeError):
        return False


def validate_case_status(status: str) -> bool:
    """
    Validate outbreak case status.
    
    Options: suspected, confirmed, discarded
    """
    if not isinstance(status, str):
        return False
    
    valid_statuses = ["suspected", "confirmed", "discarded"]
    return status.lower().strip() in valid_statuses


def validate_patient_status(status: str) -> bool:
    """
    Validate patient health status.
    
    Options: under_treatment, recovered, deceased
    """
    if not isinstance(status, str):
        return False
    
    valid_statuses = ["under_treatment", "recovered", "deceased"]
    return status.lower().strip() in valid_statuses


def validate_region_name(region_name: str) -> bool:
    """
    Validate region name.
    
    Returns:
        True if valid, False otherwise
    """
    if not region_name or not isinstance(region_name, str):
        return False
    
    return 2 <= len(region_name.strip()) <= 100


def validate_role(role: str) -> bool:
    """
    Validate user role.
    
    Options: community, health_worker, admin
    """
    if not isinstance(role, str):
        return False
    
    valid_roles = ["community", "health_worker", "admin"]
    return role.lower().strip() in valid_roles


def validate_non_empty(value: str, field_name: str = "Value") -> bool:
    """
    Validate that a string is not empty after stripping.
    
    Raises:
        ValueError with field name if empty
    """
    if not value or not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return True


def validate_password_strength(password: str) -> bool:
    """
    Validate password meets minimum strength requirements.
    
    Requirements:
    - At least 8 characters
    - At least one digit
    - At least one uppercase letter
    - At least one lowercase letter
    
    Raises:
        ValueError with requirements if invalid
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one number.")
    
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter.")
    
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase letter.")
    
    return True