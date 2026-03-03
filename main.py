# CLI entry point for outbreak management system

from rich.console import Console
from rich.panel import Panel

from services.auth_service import AuthService
from services.case_service import CaseService
from services.region_service import RegionService


class OutbreakCLI:
    """
    CLI controller for outbreak management system.
    Provides menus based on user roles.
    """

    def __init__(self):
        self.console = Console()
        self.auth_service = AuthService()
        self.case_service = CaseService()
        self.region_service = RegionService()
        self.current_user = None

    def run(self):
        """Main loop for CLI."""
        while True:
            if not self.current_user:
                self._show_login_menu()
            else:
                self._show_role_menu()

    # ----------------------------
    # Login Menu
    # ----------------------------
    def _show_login_menu(self):
        self.console.print(Panel.fit("Login/Register Menu", style="bold cyan"))
        self.console.print("1. Login", style="green")
        self.console.print("2. Register", style="green")
        self.console.print("3. Exit", style="red")

        choice = input("Choose an option: ")

        if choice == "1":
            user = self.auth_service.login()
            if user:
                self.current_user = user
        elif choice == "2":
            self.auth_service.register()
        elif choice == "3":
            self.console.print("Exiting system...", style="bold red")
            exit()
        else:
            self.console.print("Invalid choice.", style="bold yellow")

    # ----------------------------
    # Role Menu
    # ----------------------------
    def _show_role_menu(self):
        role_title = f"{self.current_user.role.capitalize()} Menu"
        self.console.print(Panel.fit(role_title, style="bold magenta"))

        if self.current_user.role == "admin":
            self._admin_menu()
        elif self.current_user.role == "health_worker":
            self._health_worker_menu()
        elif self.current_user.role == "community":
            self._community_menu()
        else:
            self.console.print("Unknown role. Logging out.", style="bold red")
            self.current_user = None

    # ----------------------------
    # Admin Menu
    # ----------------------------
    def _admin_menu(self):
        self.console.print("1. Add Region", style="cyan")
        self.console.print("2. Remove Region", style="cyan")
        self.console.print("3. List Regions", style="cyan")
        self.console.print("4. Add Case", style="green")
        self.console.print("5. Update Case Status", style="green")
        self.console.print("6. Delete Case", style="red")
        self.console.print("7. View Cases", style="green")
        self.console.print("8. View Summary", style="green")   # NEW
        self.console.print("9. Delete User", style="red")
        self.console.print("10. Update User Role", style="red")
        self.console.print("11. Logout", style="red")

        choice = input("Choose an option: ")

        if choice == "1":
            self.region_service.add_region()
        elif choice == "2":
            self.region_service.remove_region()
        elif choice == "3":
            self.region_service.list_regions()
        elif choice == "4":
            self.case_service.add_case(self.current_user)
        elif choice == "5":
            self.case_service.update_case_status(self.current_user)
        elif choice == "6":
            self.case_service.delete_case(self.current_user)
        elif choice == "7":
            self.case_service.view_cases()
        elif choice == "8":   # NEW
            self.case_service.view_summary()
        elif choice == "9":
            self.auth_service.delete_user()
        elif choice == "10":
            self.auth_service.update_user_role()
        elif choice == "11":
            self.current_user = None
        else:
            self.console.print("Invalid choice.", style="bold yellow")

    # ----------------------------
    # Health Worker Menu
    # ----------------------------
    def _health_worker_menu(self):
        self.console.print("1. Add Case", style="green")
        self.console.print("2. Confirm Disease", style="green")
        self.console.print("3. Update Case Status", style="green")
        self.console.print("4. Delete My Case", style="red")
        self.console.print("5. View Cases", style="green")
        self.console.print("6. View Summary", style="green")   # NEW
        self.console.print("7. Logout", style="red")

        choice = input("Choose an option: ")

        if choice == "1":
            self.case_service.add_case(self.current_user)
        elif choice == "2":
            self.case_service.confirm_disease(self.current_user)
        elif choice == "3":
            self.case_service.update_case_status(self.current_user)
        elif choice == "4":
            self.case_service.delete_case(self.current_user)
        elif choice == "5":
            self.case_service.view_cases()
        elif choice == "6":
            self.case_service.view_summary()
        elif choice == "7":
            self.current_user = None
        else:
            self.console.print("Invalid choice.", style="bold yellow")

    # ----------------------------
    # Community Menu
    # ----------------------------
    def _community_menu(self):
        self.console.print("1. Report Suspected Case", style="green")
        self.console.print("2. View My Cases", style="green")
        self.console.print("3. Delete My Unconfirmed Case", style="red")
        self.console.print("4. Logout", style="red")

        choice = input("Choose an option: ")

        if choice == "1":
            self.case_service.add_case(self.current_user)
        elif choice == "2":
            self.case_service.view_cases(user=self.current_user)
        elif choice == "3":
            self.case_service.delete_case(self.current_user)
        elif choice == "4":
            self.current_user = None
        else:
            self.console.print("Invalid choice.", style="bold yellow")


if __name__ == "__main__":
    cli = OutbreakCLI()
    cli.run()
