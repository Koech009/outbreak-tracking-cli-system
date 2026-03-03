
import re

# Centralized constants
VALID_ROLES = ["community", "health_worker", "admin"]
VALID_CLASSIFICATIONS = ["suspected", "confirmed", "discarded"]
VALID_PATIENT_STATUSES = ["under_treatment", "recovered", "deceased"]


def validate_non_empty(value: str, field_name: str = "Field") -> None:
    """Ensure a string is not empty."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")


def validate_email(email: str) -> None:
    """Validate email format using regex."""
    validate_non_empty(email, "Email")
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email.strip()):
        raise ValueError("Invalid email format.")


def validate_password_strength(password: str) -> None:
    """Validate password strength."""
    validate_non_empty(password, "Password")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one number.")
    if not any(c.isupper() for c in password):
        raise ValueError(
            "Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        raise ValueError(
            "Password must contain at least one lowercase letter.")


def validate_age(age: int) -> None:
    """Validate age is a positive integer within reasonable range."""
    if not isinstance(age, int):
        raise ValueError("Age must be a number.")
    if age <= 0 or age > 120:
        raise ValueError("Age must be between 1 and 120.")


def validate_role(role: str) -> None:
    """Validate system user role."""
    validate_non_empty(role, "Role")
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role. Must be one of {VALID_ROLES}")


def validate_classification_status(status: str) -> None:
    """Validate outbreak case classification status."""
    validate_non_empty(status, "Classification status")
    if status not in VALID_CLASSIFICATIONS:
        raise ValueError(
            f"Invalid classification status. Must be one of {VALID_CLASSIFICATIONS}")


def validate_patient_status(status: str) -> None:
    """Validate patient health status."""
    validate_non_empty(status, "Patient status")
    if status not in VALID_PATIENT_STATUSES:
        raise ValueError(
            f"Invalid patient status. Must be one of {VALID_PATIENT_STATUSES}")


def validate_region_name(name: str) -> None:
    """Validate region name length."""
    validate_non_empty(name, "Region name")
    if len(name.strip()) < 3 or len(name.strip()) > 100:
        raise ValueError("Region name must be between 3 and 100 characters.")


def validate_name(name: str) -> None:
    """Validate person's name."""
    validate_non_empty(name, "Name")
    if len(name.strip()) < 2 or len(name.strip()) > 100:
        raise ValueError("Name must be between 2 and 100 characters.")
