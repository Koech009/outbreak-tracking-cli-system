# models/region.py
# Represents a geographic region where cases are reported


class Region:
    """
    Represents a geographic region.
    One region can have many cases.
    """

    def __init__(self, id: str, name: str, location: str):
        self.id = id
        self.name = name
        self.location = location

    def to_dict(self) -> dict:
        """
        Convert Region object to dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create Region object from dictionary.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            location=data["location"]
        )

    def __str__(self):
        return f"{self.name} ({self.location})"
