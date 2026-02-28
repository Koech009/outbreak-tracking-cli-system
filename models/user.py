# Represents system users and roles

import hashlib
from models.person import Person


class User(Person):
    """
    Represents a system user.
    Inherits from Person.
    Supports password hashing and role validation.
    """

    VALID_ROLES = ["community", "health_worker", "admin"]

    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        password: str,
        role: str,
        region_id: str = None
    ):
        super().__init__(id, name)

        if role not in self.VALID_ROLES:
            raise ValueError(
                f"Invalid role. Must be one of {self.VALID_ROLES}")

        self.email = email
        self.password = password
        self.role = role
        self.region_id = region_id

    def set_password(self, raw_password: str):
        """
        Hash and set the user's password.
        """
        self.password = hashlib.sha256(raw_password.encode()).hexdigest()

    def verify_password(self, raw_password: str) -> bool:
        """
        Verify a raw password against the stored hash.
        """
        return self.password == hashlib.sha256(raw_password.encode()).hexdigest()

    def to_dict(self) -> dict:
        """
        Convert user object to dictionary for JSON storage.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "region_id": self.region_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create User object from dictionary.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password=data["password"],
            role=data["role"],
            region_id=data.get("region_id")
        )

    def __str__(self):
        return f"{self.name} ({self.role})"
