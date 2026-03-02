import pytest
from models.user import User


def test_user_creation_valid_role():
    user = User("1", "Alice", "alice@example.com", "hashed_pw", "community")
    assert user.role == "community"
    assert user.email == "alice@example.com"


def test_user_invalid_role():
    with pytest.raises(ValueError):
        User("2", "Bob", "bob@example.com", "pw", "invalid_role")


def test_password_hashing_and_verification():
    user = User("3", "Charlie", "charlie@example.com", "", "admin")
    user.set_password("Secret123")
    assert user.verify_password("Secret123") is True
    assert user.verify_password("WrongPass") is False


def test_user_to_dict_and_from_dict():
    user = User("4", "Dana", "dana@example.com", "hashed_pw", "health_worker")
    data = user.to_dict()
    new_user = User.from_dict(data)
    assert new_user.email == "dana@example.com"
    assert new_user.role == "health_worker"
