# models/region.py
# Represents a geographic region where cases are reported


class Region:
    """
    Represents a geographic region.
    One region can have many cases.
    """
    def __init__(self, id: str, name: str, location: str):
        # Validate id
        if not id or not isinstance(id, str) or not id.strip():
            raise ValueError("Region id cannot be empty or blank.")
        
        # Validate name
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Region name cannot be empty or blank.")
        
        # Validate location
        if not location or not isinstance(location, str) or not location.strip():
            raise ValueError("Region location cannot be empty or blank.")

        self.id = id.strip()
        self.name = name.strip()
        self.location = location.strip()

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
