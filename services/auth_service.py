# Handles user registration, login, and password hashing.

import uuid
from models.user import User
from utils.file_handler import load_json, save_json
from utils.validators import (
    validate_non_empty,
    validate_email,
    validate_password_strength,
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

            allowed_roles = ["community", "health_worker"]
            role = input("Enter role (community/health_worker): ")
            if role not in allowed_roles:
                raise ValueError("Invalid role. Please input either community or health_worker.")
            

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

                    if not user.is_active:
                        raise ValueError(
                        "This account has currently been suspended. " \
                        "Please contact your administrator for further assistance." )
                    
                    print("✅ Login successful.")
                    print(f"Name: {user.name}")
                    print(f"User ID: {user.id}")
                    print(f"Role: {user.role}")
                    return user

            raise ValueError("Invalid email or password.")

        except ValueError as e:
            print(f"❌ Login failed: {e}")
            return None

    def update_base_role(self, current_user):
        """
        Update a user's role between community and health_worker only.
        Admin promotions are handled by promote_to_admin().
        Admin demotions are handled by manage_admin().
        Only admin and super_admin can do this.
        """
        try:
            # Gate 1: must be admin or super_admin
            if current_user.role not in ["admin", "super_admin"]:
                raise PermissionError(
                "Only admins or super admin can update user roles."
            )

            # Show only community and health_worker users
            base_users = [
                u for u in self.users
                if u.role in ["community", "health_worker"]
            ]

            if not base_users:
                print("No community or health worker users found.")
                return

            print("\n--- Community & Health Worker Users ---")
            for user in base_users:
                status = "🔴 SUSPENDED" if not user.is_active else "🟢 Active"
                print(
                    f"ID: {user.id} | "
                    f"Name: {user.name} | "
                    f"Role: {user.role} | "
                    f"Status: {status}"
                )

            user_id = input("\nEnter User ID to update: ").strip()
            target_user = self._find_user(user_id)

            if not target_user:
                raise ValueError("User not found.")

            # Gate 2: can only touch community and health_worker
            if target_user.role not in ["community", "health_worker"]:
                raise ValueError(
                    f"'{target_user.name}' is a {target_user.role}. "
                    "Use the appropriate admin management function instead."
                )

            # Gate 3: can't update a suspended user's role
            # reactivate them first, then update their role
            if not target_user.is_active:
                raise ValueError(
                    f"'{target_user.name}' is currently suspended. "
                    "Reactivate their account before updating their role."
                )

            # Show only valid base roles — admin is not an option here
            print(f"\nUpdate '{target_user.name}' to which role?")
            print("1. community")
            print("2. health_worker")

            choice = input("Enter choice (1/2): ").strip()

            if choice == "1":
                new_role = "community"
            elif choice == "2":
                new_role = "health_worker"
            else:
                raise ValueError("Invalid choice. Please enter 1 or 2.")

            # Gate 4: prevent pointless updates
            if target_user.role == new_role:
                raise ValueError(
                    f"'{target_user.name}' is already a {new_role}."
                )

            confirm = input(
                f"\nUpdate '{target_user.name}' from "
                f"{target_user.role} to {new_role}? (yes/no): "
            ).strip().lower()

            if confirm != "yes":
                print("Update cancelled.")
                return

            target_user.role = new_role
            self._save_users()
            print(
                f"✅ '{target_user.name}' successfully updated "
                f"to {new_role}."
            )
        except (ValueError, PermissionError) as e:
            print(f"❌ Update failed: {e}")


    def delete_user(self, current_user):
        """
        Delete a user account permanently.
        super_admin can delete anyone except themselves.
        admin can delete any community or health_worker.
        Nobody can delete a super_admin.
        """
        try:
            # Gate 1: must be admin or super_admin
            if current_user.role not in ["admin", "super_admin"]:
                raise PermissionError(
                    "Only admins or super admin can delete users."
                )

            # Build deletable list based on who's asking
            if current_user.role == "super_admin":
                deletable = [
                    u for u in self.users
                    if u.role != "super_admin"
                ]
            else:
                # admins can only see and delete community + health_worker
                deletable = [
                    u for u in self.users
                    if u.role in ["community", "health_worker"]
                ]

            if not deletable:
                print("No users available to delete.")
                return

            print("\n--- Deletable Users ---")
            for user in deletable:
                status = "🔴 SUSPENDED" if not user.is_active else "🟢 Active"
                print(
                    f"ID: {user.id} | "
                    f"Name: {user.name} | "
                    f"Role: {user.role} | "
                    f"Status: {status}"
                )

            user_id = input("\nEnter User ID to delete: ").strip()
            target_user = self._find_user(user_id)

            if not target_user:
                raise ValueError("User not found.")

            # Gate 2: nobody deletes super_admin
            if target_user.role == "super_admin":
                raise PermissionError(
                    "The super admin account cannot be deleted."
                )

            # Gate 3: admins can only delete community and health_worker
            if (current_user.role == "admin" and
                    target_user.role not in ["community", "health_worker"]):
                raise PermissionError(
                    f"Admins cannot delete a {target_user.role} account. "
                    "Contact the super admin for admin-level deletions."
                )

            # Gate 4: can't delete yourself
            if target_user.id == current_user.id:
                raise ValueError(
                    "You cannot delete your own account."
                )

            # Show full user details before confirming —
            # this is the accountability gate
            print(f"\n--- User To Be Deleted ---")
            print(f"Name:   {target_user.name}")
            print(f"Email:  {target_user.email}")
            print(f"Role:   {target_user.role}")
            print(
                f"Status: {'🔴 SUSPENDED' if not target_user.is_active else '🟢 Active'}"
            )

            confirm = input(
                f"\n⚠️  Permanently delete '{target_user.name}'? "
                "This cannot be undone. (yes/no): "
            ).strip().lower()

            if confirm != "yes":
                print("Deletion cancelled.")
                return

            self.users = [u for u in self.users if u.id != user_id]
            self._save_users()
            print(
                f"✅ '{target_user.name}' ({target_user.role}) "
                "has been permanently deleted."
            )

        except (ValueError, PermissionError) as e:
            print(f"❌ Deletion failed: {e}")
        
   
    def suspend_user(self, current_user):

        try: 
            if current_user.role not in ["admin", "super_admin"]:
                raise PermissionError(
                    "Only admins or super admin can suspend users."
                )
            
            if current_user.role == "super_admin":
                to_suspend = [
                    u for u in self.users
                    if u.role != "super_admin" and u.is_active
                ]
            else:
                to_suspend = [
                    u for u in self.users
                    if u.role in ["community", "health_worker"] and u.is_active
                ]

            if not to_suspend:
                print("No users available to suspend.")
                return

            print("\n---Users available for suspension ---")
            for user in to_suspend:
                print(
                    f"ID: {user.id} | "
                    f"Name: {user.name} | "
                    f"Role: {user.role} | "
                )
            user_id = input("Please input the id of the user to suspend: ")
            target_user = self._find_user(user_id)


            if not target_user:
                raise ValueError("User not found.")


            if current_user.role == "admin" and target_user.role == "admin":
                raise PermissionError(
                    "Admins cannot suspend other admins."
                )

            if target_user.role == "super_admin":
                raise PermissionError(
                    "The super admin account cannot be suspended."
                )

            if not target_user.is_active:
                raise ValueError(
                    f"'{target_user.name}' is already suspended."
                )
            
            if target_user.id == current_user.id:
                raise ValueError("You cannot suspend yourself.")

            confirm = input(
                f"Suspend '{target_user.name}' ({target_user.role})?"
                "They will not be able to log in. (yes/no): "
            ).strip().lower()

            if confirm != "yes":
                print("Suspension cancelled.")
                return

            target_user.is_active = False
            self._save_users()
            print(f"✅ '{target_user.name}' has been suspended.")

        except(ValueError, PermissionError) as e:
            print(f"❌ Suspension failed: {e}")

    
    def reactivate_user(self, current_user):
        """Reactivate a suspended user account.
           Same permission rules as suspend_user."""
                                

        try:
            if current_user.role not in ["admin", "super_admin"]:
                raise PermissionError(
                    "Only admins or super admin can reactivate users."
                )
            
            suspended = [u for u in self.users if not u.is_active]
            if not suspended:
                print("No suspended users found")
                return

            print("\n--- Suspended Users ---")
            for user in suspended:
                print(f"ID: {user.id} | Name: {user.name} | Role: {user.role}")

            user_id = input("\n Enter User ID to reactivate: ").strip()
            target_user = self._find_user(user_id)


            if not target_user:
                raise ValueError("User not found.")
            
            if target_user.is_active:
                raise ValueError(
                    f"'{target_user.name}' is not suspended."
                )

            if current_user.role == "admin" and target_user.role in ["admin", "super_admin"]:
                raise PermissionError(
                    "Admins cannot reactivate admin-level accounts."
                )

            target_user.is_active = True
            self._save_users()
            print(f"✅ '{target_user.name}' has been reactivated.")

        except(ValueError, PermissionError) as e:
            print(f"❌ Reactivation failed: {e}")

    def manage_admin(self, current_user):
        """
        Super admin command centre for handling rogue or compromised admins.
        Offers demotion, suspension, or both together.
        Only super_admin can access this.
        """
        #1st check: ensuring that the super_admin is the current user
        try:
            if current_user.role != "super_admin":
                raise PermissionError(
                    "Only the super admin can manage admin accounts."
                )

            admins = [u for u in self.users if u.role == "admin"]
            if not admins:
                print("No admins found.")
                return

            print("\n--- Current Admins ---")
            for user in admins:
                status = "🔴 SUSPENDED" if not user.is_active else "🟢 Active"
                print(
                    f"ID: {user.id} | "
                    f"Name: {user.name} | "
                    f"Status: {status}"
                )

            user_id = input("\nEnter User ID to manage: ").strip()
            target_user = self._find_user(user_id)

            #implementing three checks:

            #1. user not found
            if not target_user:
                raise ValueError("User not found.")

            #2. user is not an admin
            if target_user.role != "admin":
                raise ValueError(
                    f"'{target_user.name}' is not an admin."
                )
            
            #3. user is the super_admin
            if target_user.id == current_user.id:
                raise ValueError(
                    "You cannot manage your own account here."
                )

            # Present the three tiers clearly
            print(f"\nManaging: {target_user.name}")
            print("─" * 40)
            print("1. Demote only      → strips privileges, keeps login access")
            print("2. Suspend only     → blocks login, keeps admin role frozen")
            print("3. Demote + Suspend → full lockdown, strips privileges AND blocks login")
            print("4. Cancel")
            print("─" * 40)

            choice = input("Choose action (1/2/3/4): ").strip()

            if choice == "4":
                print("Action cancelled.")
                return

            if choice not in ["1", "2", "3"]:
                raise ValueError("Invalid choice. Please enter 1, 2, 3, or 4.")

            # ─────────────────────────────────────
            # TIER 1: Demote only
            # ─────────────────────────────────────
            if choice == "1":
                print(f"\nDemote '{target_user.name}' to which role?")
                print("1. health_worker")
                print("2. community")

                role_choice = input("Enter choice (1/2): ").strip()

                if role_choice == "1":
                    new_role = "health_worker"
                elif role_choice == "2":
                    new_role = "community"
                else:
                    raise ValueError("Invalid choice.")

                confirm = input(
                    f"\nDemote '{target_user.name}' to {new_role}? (yes/no): "
                ).strip().lower()

                if confirm != "yes":
                    print("Action cancelled.")
                    return

                target_user.role = new_role
                self._save_users()
                print(
                    f"✅ '{target_user.name}' demoted to {new_role}. "
                    f"Login access retained."
                )

            # ─────────────────────────────────────
            # TIER 2: Suspend only
            # ─────────────────────────────────────
            elif choice == "2":
                if not target_user.is_active:
                    raise ValueError(
                        f"'{target_user.name}' is already suspended."
                    )

                confirm = input(
                    f"\nSuspend '{target_user.name}'? "
                    "They will not be able to log in. (yes/no): "
                ).strip().lower()

                if confirm != "yes":
                    print("Action cancelled.")
                    return

                target_user.is_active = False
                self._save_users()
                print(
                    f"✅ '{target_user.name}' suspended. "
                    f"Admin privileges retained but login blocked."
                )

            # ─────────────────────────────────────
            # TIER 3: Demote + Suspend (full lockdown)
            # ─────────────────────────────────────
            elif choice == "3":
                print(f"\nDemote '{target_user.name}' to which role?")
                print("1. health_worker")
                print("2. community")

                role_choice = input("Enter choice (1/2): ").strip()

                if role_choice == "1":
                    new_role = "health_worker"
                elif role_choice == "2":
                    new_role = "community"
                else:
                    raise ValueError("Invalid choice.")

                confirm = input(
                    f"\n⚠️  Full lockdown: demote '{target_user.name}' to "
                    f"{new_role} AND suspend login access? (yes/no): "
                ).strip().lower()

                if confirm != "yes":
                    print("Action cancelled.")
                    return

                target_user.role = new_role
                target_user.is_active = False
                self._save_users()
                print(
                    f"✅ Full lockdown applied to '{target_user.name}'. "
                    f"Demoted to {new_role} and login suspended."
                )

        except (ValueError, PermissionError) as e:
            print(f"❌ Action failed: {e}")
    
    def promote_to_admin(self, current_user):
        """
        Update a user's role from health_worker to admin.
        Only  super_admin can do this.
        """

        try:
            # Gate 1: must be super_admin
            if current_user.role != "super_admin":
                raise PermissionError(
                "Only the super admin can promote to admin."
            )

            # Show all health workers
            health_workers = [
                u for u in self.users
                if u.role == "health_worker" and u.is_active
            ]

            if not health_workers:
                print("No health workers found to promote to admin.")
                return

            print("\n--- Available Health Workers")
            for user in health_workers:
                print(
                    f"ID: {user.id} | "
                    f"Name: {user.name} | "
                )

            user_id = input("\nEnter User ID to update: ").strip()
            target_user = self._find_user(user_id)

            if not target_user:
                raise ValueError("User not found.")

            # Gate 2: can only promote a health_worker
            if target_user.role != "health_worker":
                raise ValueError(
                    f"'{target_user.name}' is a {target_user.role}. "
                    "You can only promote active health workers to the admin role."
                )

            # Gate 3: can't update a suspended user's role
            # reactivate them first, then update their role
            if not target_user.is_active:
                raise ValueError(
                    f"'{target_user.name}' is currently suspended. "
                    "Reactivate their account before promoting them to an admin."
                )


            confirm = input(
                f"\nUpdate '{target_user.name}' from health worker to admin (yes/no): "
            ).strip().lower()

            if confirm != "yes":
                print("Update cancelled.")
                return

            target_user.role = "admin"
            self._save_users()
            print(
                f"✅ '{target_user.name}' successfully updated to admin."
            )
        except (ValueError, PermissionError) as e:
            print(f"❌ Update failed: {e}")
