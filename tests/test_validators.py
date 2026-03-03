
import pytest
from utils import validators

# Non-empty validation


def test_validate_non_empty_success():
    validators.validate_non_empty("Hello", "TestField")


def test_validate_non_empty_failure():
    with pytest.raises(ValueError):
        validators.validate_non_empty("", "TestField")

# Email validation


@pytest.mark.parametrize("email", [
    "user@example.com",
    "test.user@domain.co",
    "alice+bob@sub.domain.org"
])
def test_validate_email_success(email):
    validators.validate_email(email)


@pytest.mark.parametrize("email", [
    "",
    "invalid-email",
    "user@com",
    "user@.com"
])
def test_validate_email_failure(email):
    with pytest.raises(ValueError):
        validators.validate_email(email)

# Password validation


@pytest.mark.parametrize("password", [
    "StrongPass1",
    "Valid123Password",
    "MyPass2023"
])
def test_validate_password_strength_success(password):
    validators.validate_password_strength(password)


@pytest.mark.parametrize("password", [
    "short1A",      # too short
    "12345678",     # no letters
    "ABCDEFGH1",    # no lowercase
    "abcdefgh1",    # no uppercase
    "",             # empty
])
def test_validate_password_strength_failure(password):
    with pytest.raises(ValueError):
        validators.validate_password_strength(password)

# Age validation


@pytest.mark.parametrize("age", [1, 25, 120])
def test_validate_age_success(age):
    validators.validate_age(age)


@pytest.mark.parametrize("age", [0, 121, "twenty", None])
def test_validate_age_failure(age):
    with pytest.raises(ValueError):
        validators.validate_age(age)

# Role validation


@pytest.mark.parametrize("role", validators.VALID_ROLES)
def test_validate_role_success(role):
    validators.validate_role(role)


def test_validate_role_failure():
    with pytest.raises(ValueError):
        validators.validate_role("invalid_role")

# Case classification status


@pytest.mark.parametrize("status", ["suspected", "confirmed", "discarded"])
def test_validate_classification_status_success(status):
    validators.validate_classification_status(status)


def test_validate_classification_status_failure():
    with pytest.raises(ValueError):
        validators.validate_classification_status("invalid_status")

# Patient status validation


@pytest.mark.parametrize("status", ["under_treatment", "recovered", "deceased"])
def test_validate_patient_status_success(status):
    validators.validate_patient_status(status)


def test_validate_patient_status_failure():
    with pytest.raises(ValueError):
        validators.validate_patient_status("invalid_status")

# Region name validation


def test_validate_region_name_success():
    validators.validate_region_name("Nairobi")
    validators.validate_region_name("Western Kenya")


@pytest.mark.parametrize("name", ["Na", "", "  "])
def test_validate_region_name_failure(name):
    with pytest.raises(ValueError):
        validators.validate_region_name(name)

# Name validation


def test_validate_name_success():
    validators.validate_name("Alice")
    validators.validate_name("Bob Smith")


@pytest.mark.parametrize("name", ["A", "", "  "])
def test_validate_name_failure(name):
    with pytest.raises(ValueError):
        validators.validate_name(name)
