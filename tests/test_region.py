from models.region import Region
import pytest


def test_region_creation():
    region = Region("1", "Nairobi", "Kenya")
    assert region.name == "Nairobi"
    assert region.location == "Kenya"


def test_region_to_dict_and_from_dict():
    region = Region("2", "Mombasa", "Kenya")
    data = region.to_dict()
    new_region = Region.from_dict(data)
    assert new_region.name == "Mombasa"
    assert new_region.location == "Kenya"
