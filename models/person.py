class Person:
    """
    Base class representing a person in the system.
    All user types inherit from this.
    """

    def __init__(self, person_id: str, name: str, email: str):
        """
        Initialize a Person with common attributes.

        Args:
            person_id: Unique identifier (could be UUID or email-based)
            name: Full name of the person
            email: Email address (used for login)
        """
        self.id = person_id
        self.name = name
        self.email = email.lower()

    def __str__(self) -> str:
        """String representation of the person."""
        return f"{self.name} ({self.email})"

    def to_dict(self) -> dict:
        """
        Convert person object to dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Person instance from dictionary data.

        Args:
            data: Dictionary containing person data
        """
        return cls(
            person_id=data["id"],
            name=data["name"],
            email=data["email"]
        )
