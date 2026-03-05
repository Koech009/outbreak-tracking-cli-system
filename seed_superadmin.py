import uuid
from models.user import User
from utils.file_handler import load_json, save_json

USERS_FILE = "data/users.json"

def seed_super_admin():
    users = load_json(USERS_FILE)

    for user in users:
        if user.get("role") == "super_admin":
            print("❌ A super_admin already exists. Seeding aborted.")

        super_admin = User(
            id = str(uuid.uuid4()),
            name="Super Admin",
            email="superadmin@outbreaktracker.com",
            password="SuperAdmin1234!",
            role="super_admin"
        )

        users.append(super_admin.to_dict())
        save_json(USERS_FILE, users)
        print("✅ Super admin seeded successfully.")
        print("  Email: superadmin@outbreaktracker.com")
        print("  Password: SuperAdmin1234!")
        print("  ⚠️  Change this password immediately after your first login")

        seed_super_admin()