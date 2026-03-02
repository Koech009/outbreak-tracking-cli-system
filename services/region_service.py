# services/region_service.py
# Handles region operations.

import uuid
from models.region import Region
from utils.file_handler import load_json, save_json
from utils.validators import validate_region_name, validate_non_empty

REGIONS_FILE = "data/regions.json"


class RegionService:
    """
    Handles region creation, deletion, and listing.
    Prevents duplicate regions.
    """

    def __init__(self):
        self.regions = self._load_regions()

    # ----------------------------
    # Internal Methods
    # ----------------------------

    def _load_regions(self):
        """
        Load regions from JSON and convert to Region objects.
        """
        data = load_json(REGIONS_FILE)
        return [Region.from_dict(region) for region in data]

    def _save_regions(self):
        """
        Save current regions to JSON file.
        """
        data = [region.to_dict() for region in self.regions]
        save_json(REGIONS_FILE, data)

    def _region_exists(self, name: str) -> bool:
        """
        Check if a region with the given name already exists.
        """
        return any(region.name.lower() == name.lower() for region in self.regions)

    # ----------------------------
    # Public Methods
    # ----------------------------

    def add_region(self):
        """
        Add a new region.
        Prevents duplicates.
        """
        try:
            name = input("Enter region name: ")
            validate_region_name(name)

            if self._region_exists(name):
                raise ValueError("Region already exists.")

            location = input("Enter region location: ")
            validate_non_empty(location, "Region location")

            new_region = Region(
                id=str(uuid.uuid4()),
                name=name,
                location=location
            )

            self.regions.append(new_region)
            self._save_regions()

            print("Region added successfully.")

        except ValueError as e:
            print(f"Failed to add region: {e}")

    def remove_region(self):
        """
        Remove a region by name.
        """
        try:
            name = input("Enter region name to remove: ")
            validate_non_empty(name, "Region name")

            for region in self.regions:
                if region.name.lower() == name.lower():
                    self.regions.remove(region)
                    self._save_regions()
                    print("Region removed successfully.")
                    return

            raise ValueError("Region not found.")

        except ValueError as e:
            print(f"Failed to remove region: {e}")

    def list_regions(self):
        """
        Display all regions.
        """
        if not self.regions:
            print("No regions found.")
            return

        for region in self.regions:
            print(region)
