import pytest
import uuid
from services.auth_service import AuthService
from models.user import User


@pytest.fixture
def auth_service(tmp_path, monkeypatch):
    # Override USERS_FILE to use a temp file
    from services import auth_service as module
    module.USERS_FILE = tmp_path / "users.json"
    return AuthService()


def test_register_and_login_success(auth_service, monkeypatch):
    inputs = iter(["Alice", "alice@example.com", "Secret123", "community"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    auth_service.register()
    assert len(auth_service.users) == 1

    # Login with correct credentials
    inputs = iter(["alice@example.com", "Secret123"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    user = auth_service.login()
    assert isinstance(user, User)
    assert user.email == "alice@example.com"


def test_register_duplicate_email(auth_service, monkeypatch, capsys):
    # First registration
    inputs = iter(["Bob", "bob@example.com", "Pass123", "admin"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    auth_service.register()

    # Attempt duplicate registration
    inputs = iter(["Bob", "bob@example.com", "Pass123", "admin"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    auth_service.register()

    captured = capsys.readouterr()

    assert "Email already exists" in captured.out


def test_login_invalid_credentials(auth_service, monkeypatch, capsys):
    inputs = iter(["wrong@example.com", "WrongPass"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    user = auth_service.login()
    assert user is None
    captured = capsys.readouterr()
    assert "Login failed" in captured.out
