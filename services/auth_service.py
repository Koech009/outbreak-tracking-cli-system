# Handles user registration, login, and password hashing.

import uuid
from models.user import User
from utils.file_handler import load_json, save_json
from utils.validators import (
    validate_non_empty,
    validate_email,
    validate_password_strength,
    validate_role
)

USERS_FILE = "data/users.json"


class AuthService:
    """
    Handles authentication logic:
    - User registration
    - User login
    - Admin user management (delete/update role)
    """

    def __init__(self):
        self.users = self._load_users()

    # ----------------------------
    # Internal Utility Methods
    # ----------------------------
    def _load_users(self):
        """Load users from JSON file and convert to User objects."""
        data = load_json(USERS_FILE)
        return [User.from_dict(user) for user in data]

    def _save_users(self):
        """Save current users list to JSON file."""
        data = [user.to_dict() for user in self.users]
        save_json(USERS_FILE, data)

    def _email_exists(self, email: str) -> bool:
        """Check if email is already registered."""
        return any(user.email == email for user in self.users)

    def _find_user(self, user_id: str):
        """Helper: find a user by ID."""
        return next((user for user in self.users if user.id == user_id), None)

    # ----------------------------
    # Public Methods
    # ----------------------------
    def register(self):
        """Register a new user with validation."""
        try:
            name = input("Enter name: ")
            validate_non_empty(name, "Name")

            email = input("Enter email: ")
            validate_email(email)

            if self._email_exists(email):
                raise ValueError("Email already exists.")

            password = input("Enter password: ")
            validate_password_strength(password)

            role = input("Enter role (community/health_worker/admin): ")
            validate_role(role)

            # Create user (password is hashed in User.__init__)
            new_user = User(
                id=str(uuid.uuid4()),
                name=name,
                email=email,
                password=password,
                role=role
            )

            self.users.append(new_user)
            self._save_users()
            print(
                f"✅ User registered successfully. ID: {new_user.id}, Role: {new_user.role}")

        except ValueError as e:
            print(f"❌ Registration failed: {e}")

    def login(self):
        """Authenticate user. Returns User object if successful."""
        try:
            email = input("Enter email: ")
            password = input("Enter password: ")

            for user in self.users:
                if user.email == email and user.verify_password(password):
                    print("✅ Login successful.")
                    print(f"Name: {user.name}")
                    print(f"User ID: {user.id}")
                    print(f"Role: {user.role}")
                    return user

            raise ValueError("Invalid email or password.")

        except ValueError as e:
            print(f"❌ Login failed: {e}")
            return None

    def delete_user(self):
        """Admin deletes a user by ID."""
        try:
            user_id = input("Enter User ID to delete: ")
            user = self._find_user(user_id)
            if not user:
                raise ValueError("User not found.")

            self.users = [u for u in self.users if u.id != user_id]
            self._save_users()
            print(
                f"✅ User '{user.name}' (Role: {user.role}) deleted successfully.")

        except ValueError as e:
            print(f"❌ Deletion failed: {e}")

    def update_user_role(self):
        """Admin updates a user's role."""
        try:
            user_id = input("Enter User ID to update role: ")
            new_role = input(
                "Enter new role (community/health_worker/admin): ")
            validate_role(new_role)

            user = self._find_user(user_id)
            if not user:
                raise ValueError("User not found.")

            user.role = new_role
            self._save_users()
            print(f"✅ User '{user.name}' role updated to {new_role}.")

        except ValueError as e:
            print(f"❌ Update failed: {e}")
