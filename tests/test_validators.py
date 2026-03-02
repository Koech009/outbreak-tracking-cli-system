import pytest
from utils import validators


def test_validate_non_empty_success():
    validators.validate_non_empty("Hello", "TestField")


def test_validate_non_empty_failure():
    with pytest.raises(ValueError):
        validators.validate_non_empty("", "TestField")


def test_validate_email_success():
    validators.validate_email("user@example.com")


def test_validate_email_failure():
    with pytest.raises(ValueError):
        validators.validate_email("invalid-email")


def test_validate_password_strength_success():
    validators.validate_password_strength("Pass123")


def test_validate_password_strength_too_short():
    with pytest.raises(ValueError):
        validators.validate_password_strength("P1")


def test_validate_password_strength_no_letter():
    with pytest.raises(ValueError):
        validators.validate_password_strength("123456")


def test_validate_password_strength_no_number():
    with pytest.raises(ValueError):
        validators.validate_password_strength("abcdef")


def test_validate_age_success():
    validators.validate_age(25)


def test_validate_age_invalid_type():
    with pytest.raises(ValueError):
        validators.validate_age("twenty")


def test_validate_age_out_of_range():
    with pytest.raises(ValueError):
        validators.validate_age(0)
    with pytest.raises(ValueError):
        validators.validate_age(150)


def test_validate_role_success():
    for role in validators.VALID_ROLES:
        validators.validate_role(role)


def test_validate_role_failure():
    with pytest.raises(ValueError):
        validators.validate_role("invalid_role")


def test_validate_classification_status_success():
    for status in ["suspected", "confirmed", "discarded"]:
        validators.validate_classification_status(status)


def test_validate_classification_status_failure():
    with pytest.raises(ValueError):
        validators.validate_classification_status("invalid_status")


def test_validate_patient_status_success():
    for status in ["under_treatment", "recovered", "deceased"]:
        validators.validate_patient_status(status)


def test_validate_patient_status_failure():
    with pytest.raises(ValueError):
        validators.validate_patient_status("invalid_status")


def test_validate_region_name_success():
    validators.validate_region_name("Nairobi")


def test_validate_region_name_too_short():
    with pytest.raises(ValueError):
        validators.validate_region_name("Na")
