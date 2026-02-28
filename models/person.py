# Base class representing a generic person in the system

class Person:
    """
    Base class for all person types in the system.
    Demonstrates inheritance (User will inherit from this).
    """

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def to_dict(self) -> dict:
        """
        Convert object to dictionary for JSON storage.
        """
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create object from dictionary.
        """
        return cls(
            id=data["id"],
            name=data["name"]
        )
