"""
User model.
Inherits from Person.
Handles role-based users (admin, health_worker, community_user).
Includes secure password handling, role validation, and serialization.
"""

import uuid
import hashlib
from models.person import Person

# Allowed roles for system users
VALID_ROLES = {"admin", "health_worker", "community"}


class User(Person):
    def __init__(self, name, email, password, role="community", user_id=None, is_hashed=False):

        super().__init__(name, email)

        # Generate unique ID
        self._id = user_id or str(uuid.uuid4())

        # Defensive integrity check for role validity
        if role not in VALID_ROLES:
            raise ValueError(
                f"Invalid role: {role}. Must be one of {VALID_ROLES}"
            )
        self._role = role

        # Store password securely
        self._password = (
            password if is_hashed else self._hash_password(password)
        )

    # ---------------- Properties ----------------
    @property
    def id(self):
        """Return unique user ID."""
        return self._id

    @property
    def role(self):
        """Return user role."""
        return self._role

    # ---------------- Password Handling ----------------
    def _hash_password(self, raw_password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(raw_password.encode()).hexdigest()

    def verify_password(self, raw_password: str) -> bool:
        """Verify raw password against stored hash."""
        return self._password == self._hash_password(raw_password)

    # ---------------- Serialization ----------------
    def to_dict(self) -> dict:
        """Convert User object to dictionary for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self._password,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Recreate User object from stored dictionary."""
        return cls(
            data["name"],
            data["email"],
            data["password"],
            data.get("role", "community"),
            data.get("id"),
            is_hashed=True  # Prevent double hashing
        )

    # ---------------- Utility Methods ----------------
    def __repr__(self):
        """Readable representation for debugging."""
        return f"<User {self.name} ({self.role})>"

    def __eq__(self, other):
        """Equality check based on unique ID."""
        return isinstance(other, User) and self.id == other.id
