# tests/test_cli.py
import pytest
from main import OutbreakCLI


def test_cli_exit(monkeypatch):
    cli = OutbreakCLI()
    # Simulate user choosing "3" (Exit) in login menu
    monkeypatch.setattr("builtins.input", lambda _: "3")
    with pytest.raises(SystemExit):
        cli._show_login_menu()


def test_cli_invalid_choice(monkeypatch, capsys):
    cli = OutbreakCLI()
    monkeypatch.setattr("builtins.input", lambda _: "invalid")
    cli._show_login_menu()
    captured = capsys.readouterr()
    assert "Invalid choice." in captured.out


def test_cli_role_menu_unknown(monkeypatch, capsys):
    cli = OutbreakCLI()

    class DummyUser:
        role = "unknown"
    cli.current_user = DummyUser()
    cli._show_role_menu()
    captured = capsys.readouterr()
    assert "Unknown role" in captured.out