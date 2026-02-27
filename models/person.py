"""
Base Person class.
Demonstrates inheritance and encapsulation.
"""


class Person:
    def __init__(self, name: str, email: str):
        # Basic validation
        if not name:
            raise ValueError("Name cannot be empty.")

        if "@" not in email:
            raise ValueError("Invalid email format.")

        # Encapsulated (protected) attributes
        self._name = name
        self._email = email

    # Getter for name
    @property
    def name(self):
        """Return person's name."""
        return self._name

    # Getter for email
    @property
    def email(self):
        """Return person's email."""
        return self._email

    def __str__(self):
        """User-friendly string representation."""
        return f"{self.name} ({self.email})"
