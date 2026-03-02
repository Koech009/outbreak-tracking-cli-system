from utils.auth import register_user, login_user
from utils.file_handler import load_json, save_json
from models.region import Region
from models.case import Case
from datetime import datetime

# ================ ADMIN HELPERS =================

def add_health_worker():
    name = input("Enter health worker's name: ")
    email = input("Enter health worker's email: ")
    password = input("Enter a password for the health worker: ")
    register_user(name, email, password, "health_worker")
    print("Health worker added successfully.")

def view_all_health_workers():
    users = load_json("data/users.json")
    workers = [u for u in users if u["role"] == "health_worker"]
    if not workers:
        print("No health workers found.")
        #i like this added bit of making it more readable. what would it have looked like if i had
        #left it as was?
    for w in workers:
        print(f"- {w['name']} | {w['email']}")

def remove_health_worker():
    users = load_json("data/users.json")
    email = input("Enter the health worker's email to remove: ")
    # USING !=
    updated = [u for u in users if u["email"] != email]
    #checking length is such a smart and clean way to do it!
    if len(updated) == len(users):
        print("No user found with that email.")
    else:
        save_json("data/users.json", updated)
        print("Health worker removed.")



def remove_region():
    regions = load_json("data/regions.json")
    region_id = input("Enter the region ID to remove: ")
    updated = [r for r in regions if r["id"] != region_id]
    if len(updated) == len(regions):
        print("No region found with that ID.")
    else:
        save_json("data/regions.json", updated)
        print("Region removed.")

def add_region():
    regions = load_json("data/regions.json")
    region_id = len(regions) + 1
    name = input("Enter region name: ")
    location = input("Enter region location: ")    # replaces population
    new_region = Region(region_id, name, location)
    regions.append(new_region.to_dict())
    save_json("data/regions.json", regions)
    print(f"{name} region added successfully.")

def view_all_regions():
    regions = load_json("data/regions.json")
    if not regions:
        print("No regions found.")
    for r in regions:
        print(f"- ID: {r['id']} | Name: {r['name']} | Location: {r['location']}")

def view_all_cases():
    cases = load_json("data/cases.json")
    if not cases:
        print("No cases found.")
    for c in cases:
        print(f"- ID: {c['id']} | Name: {c['patient_name']} | Age:  {c['age']} | Gender:  {c['gender']} | Region ID:  {c['region_id']} | | Reported By:  {c['reported_by']} | | Date Reported:  {c['date_reported']} Classification Status: {c['classification_status']} | Patient Status:  {c['patient_status']}  ")

def generate_report():
    regions = load_json("data/regions.json")
    region_id = input("Enter the region ID to generate a report for: ")
    target = next((r for r in regions if r["id"] == region_id), None)
    if not target:
        print("Invalid region ID. Please try again.")
        return
    region = Region.from_dict(target)
    print(region.region_summary())

# ======================== HEALTH WORKER HELPERS ==============
def add_case(current_user):
    cases = load_json("data/cases.json")
    regions = load_json("data/regions.json")
    region_id = int(input("Enter the region ID to add a case to: "))
    target = next((r for r in regions if r["id"] == region_id), None)
    if not target:
        print("Invalid region ID. Please try again.")
        return
    
    case_id = len(cases) + 1            
    patient_name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))
    gender = input("Enter gender: ")    
    classification_status = input("Enter classification status (suspected/confirmed/discarded): ")
    patient_status = input("Enter patient status (under_treatment/recovered/deceased): ")
    
    new_case = {
        "id": case_id,
        "patient_name": patient_name,
        "age": age,
        "gender": gender,                               
        "region_id": region_id,                       
        "reported_by": current_user["id"],             
        "date_reported": datetime.now().date().isoformat(),
        "classification_status": classification_status, 
        "patient_status": patient_status,               
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    cases.append(new_case)
    save_json("data/cases.json", cases)
    print("Case added successfully.")

def update_case():
    cases = load_json("data/cases.json")
    case_id = input("Enter the case ID to update: ")
    target = next((c for c in cases if (c["id"]) == case_id), None)
    if not target:
        print("Invalid case ID. Please try again.")
        return
    
    print("What would you like to update?\n1. Classification status\n2. Patient status")
    choice = input("> ")
    
    if choice == "1":
        new_status = input("Enter new classification status (suspected/confirmed/discarded): ")
        field = "classification_status"
    elif choice == "2":
        new_status = input("Enter new patient status (under_treatment/recovered/deceased): ")
        field = "patient_status"
    else:
        print("Invalid choice.")
        return
    
    updated_cases = [
        {**c, field: new_status, "updated_at": datetime.now().isoformat()} 
        if (c["id"]) == case_id else c
        for c in cases
    ]
    save_json("data/cases.json", updated_cases)
    print("Case updated successfully.")


def view_cases_in_region():
    regions = load_json("data/regions.json")
    region_id = input("Enter your region ID: ")
    target = next((r for r in regions if r["id"] == region_id), None)
    if not target:
        print("Invalid region ID.")
        return
    cases = load_json("data/cases.json")
    regional_cases = [c for c in cases if c["id"] in target["case_list"]]
    if not regional_cases:
        print("No cases in this region.")
    for c in regional_cases:
        print(f"- {c['id']} | {c['patient_name']} | Status: {c['status']}")

# ================== COMMUNITY USER HELPERS =======================

def report_suspected_case(current_user):
    regions = load_json("data/regions.json")
    region_id = input("Enter your region ID: ")
    target = next((r for r in regions if r["id"] == region_id), None)
    if not target:
        print("Invalid region ID.")
        return
    case_id = input("Enter a case ID: ")
    patient_name = input("Enter patient name: ")
    age = input("Enter patient age: ")
    location = input("Enter location: ")
    new_case = Case(case_id, patient_name, int(age), location, "suspected", current_user["id"])
    region = Region.from_dict(target)
    region.add_case(new_case)
    updated_regions = [region.to_dict() if r["id"] == region_id else r for r in regions]
    save_json("data/regions.json", updated_regions)
    cases = load_json("data/cases.json")
    cases.append(new_case.to_dict())
    save_json("data/cases.json", cases)
    print("Suspected case reported successfully.")

def view_outbreak_summary():
    regions = load_json("data/regions.json")
    region_id = input("Enter your region ID: ")
    target = next((r for r in regions if r["id"] == region_id), None)
    if not target:
        print("Invalid region ID.")
        return
    region = Region.from_dict(target)
    print(region.region_summary())

# ====================== MENUS ======================

def show_admin_menu(current_user):
    while True:
        print("\n1. Manage Health Workers\n2. Manage Regions\n3. View All Cases\n4. Generate Report\n5. Logout")
        choice = input("> ")

        if choice == "1":
            print("\n1. Add Health Worker\n2. Remove Health Worker\n3. View All Health Workers")
            selection = input("> ")
            if selection == "1":
                add_health_worker()
            elif selection == "2":
                remove_health_worker()
            elif selection == "3":
                view_all_health_workers()

        elif choice == "2":
            print("\n1. Add Region\n2. Remove Region\n3. View All Regions")
            selection = input("> ")
            if selection == "1":
                add_region()
            elif selection == "2":
                remove_region()
            elif selection == "3":
                view_all_regions()

        elif choice == "3":
            view_all_cases()

        elif choice == "4":
            generate_report()

        elif choice == "5":
            print("Logging out...")
            break

        else:
            print("Invalid input. Please try again.")

def show_health_worker_menu(current_user):
    while True:
        print("\n1. Add New Case\n2. Update Case Status\n3. View Cases In My Region\n4. Logout")
        choice = input("> ")

        if choice == "1":
            add_case(current_user)
        elif choice == "2":
            update_case()
        elif choice == "3":
            view_cases_in_region(current_user)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid input. Please try again.")

def show_community_menu(current_user):
    while True:
        print("\n1. Report Suspected Case\n2. View Outbreak Summary\n3. Logout")
        choice = input("> ")

        if choice == "1":
            report_suspected_case(current_user)
        elif choice == "2":
            view_outbreak_summary()
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid input. Please try again.")

# ==================== MAIN ENTRY POINT ============================

def main():
    menus = {
        "admin": show_admin_menu,
        "health_worker": show_health_worker_menu,
        "community_user": show_community_menu
    }

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("> ")

        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Create a password: ")
            role = input("Enter your role (admin/health_worker/community_user): ")
            register_user(name, email, password, role)
            print("Registered successfully. Please log in.")

        elif choice == "2":
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            current_user = login_user(email, password)
            print(f"Welcome back {current_user['name']}!")
            menus[current_user["role"]](current_user)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()

