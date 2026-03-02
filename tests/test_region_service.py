import pytest
import uuid
from services.region_service import RegionService


@pytest.fixture
def region_service(tmp_path, monkeypatch):
    # Override REGIONS_FILE to use a temp file
    from services import region_service as module
    module.REGIONS_FILE = tmp_path / "regions.json"
    return RegionService()


def test_add_region_success(region_service, monkeypatch):
    inputs = iter(["Nairobi", "Kenya"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    region_service.add_region()
    assert len(region_service.regions) == 1
    assert region_service.regions[0].name == "Nairobi"


def test_add_region_duplicate(region_service, monkeypatch, capsys):
    # First region
    inputs = iter(["Mombasa", "Kenya"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    region_service.add_region()

    # Attempt duplicate
    inputs = iter(["Mombasa", "Kenya"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    region_service.add_region()

    captured = capsys.readouterr()
    assert "Region already exists" in captured.out


def test_remove_region_success(region_service, monkeypatch):
    # Add region first
    inputs = iter(["Kisumu", "Kenya"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    region_service.add_region()

    # Remove region
    inputs = iter(["Kisumu"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    region_service.remove_region()
    assert len(region_service.regions) == 0


def test_remove_region_not_found(region_service, monkeypatch, capsys):
    inputs = iter(["Nonexistent"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    region_service.remove_region()
    captured = capsys.readouterr()
    assert "Region not found" in captured.out


def test_list_regions_empty(region_service, capsys):
    region_service.list_regions()
    captured = capsys.readouterr()
    assert "No regions found" in captured.out


def test_list_regions_with_data(region_service, monkeypatch, capsys):
    inputs = iter(["Eldoret", "Kenya"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    region_service.add_region()

    region_service.list_regions()
    captured = capsys.readouterr()
    assert "Eldoret" in captured.out
