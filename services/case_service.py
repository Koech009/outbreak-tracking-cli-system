"""
Case Service
Handles outbreak case creation, updates, deletion, viewing, and reporting.
"""

import uuid
from datetime import datetime
from rich.console import Console
from rich.table import Table

from models.case import Case
from utils.file_handler import load_json, save_json
from utils.validators import (
    validate_non_empty,
    validate_age,
    validate_classification_status,
    validate_patient_status
)

CASES_FILE = "data/cases.json"
console = Console()


class CaseService:
    """
    Service layer for managing outbreak cases.
    Handles business logic and role-based permissions.
    """
    #

    def __init__(self):
        self.cases = self._load_cases()

    # Internal Helpers-encapsulation

    def _load_cases(self):
        """Load cases from JSON and convert to Case objects."""
        data = load_json(CASES_FILE)
        return [Case.from_dict(case) for case in data]

    def _save_cases(self):
        """Persist cases to JSON file."""
        save_json(CASES_FILE, [case.to_dict() for case in self.cases])

    def _find_case(self, case_id):
        """Find case by ID."""
        return next((c for c in self.cases if c.id == case_id), None)

    def _authorize(self, condition, message):
        """Helper for role-based permission checks."""
        if not condition:
            raise PermissionError(message)

    # =====================================================
    # Public Methods
    # =====================================================

    def add_case(self, current_user):
        """Add a new outbreak case."""
        try:
            patient_name = input("Patient name: ").strip()
            validate_non_empty(patient_name, "Patient name")

            age = int(input("Age: "))
            validate_age(age)

            region_id = input("Region ID: ").strip()
            validate_non_empty(region_id, "Region ID")

            case_id = str(uuid.uuid4())
            date_reported = datetime.now().strftime("%Y-%m-%d")

            # COMMUNITY USER
            if current_user.role == "community":
                symptoms = input("Symptoms (comma separated): ").split(",")
                symptoms = [s.strip() for s in symptoms if s.strip()]

                possible_disease = input(
                    "Possible disease (optional): "
                ).strip() or None

                new_case = Case(
                    id=case_id,
                    patient_name=patient_name,
                    age=age,
                    region_id=region_id,
                    reported_by=current_user.id,
                    date_reported=date_reported,
                    classification_status="suspected",
                    patient_status="under_treatment",
                    symptoms=symptoms,
                    possible_disease=possible_disease,
                    confirmed_disease=None
                )

            # HEALTH WORKER OR ADMIN
            else:
                disease = input("Disease name: ").strip()
                validate_non_empty(disease, "Disease name")

                classification_status = input(
                    "Classification (suspected/confirmed/discarded): "
                ).strip()
                validate_classification_status(classification_status)

                patient_status = input(
                    "Patient status (under_treatment/recovered/deceased): "
                ).strip()
                validate_patient_status(patient_status)

                new_case = Case(
                    id=case_id,
                    patient_name=patient_name,
                    age=age,
                    region_id=region_id,
                    reported_by=current_user.id,
                    date_reported=date_reported,
                    classification_status=classification_status,
                    patient_status=patient_status,
                    symptoms=[],
                    possible_disease=None,
                    confirmed_disease=disease
                )

            self.cases.append(new_case)
            self._save_cases()
            console.print(
                "[bold green]✅ Case added successfully.[/bold green]")

        except (ValueError, PermissionError) as e:
            console.print(f"[bold red]❌ Failed to add case: {e}[/bold red]")

    def update_case_status(self, current_user):
        """Update classification and/or patient status."""
        try:
            self._authorize(
                current_user.role != "community",
                "Community users cannot update case status."
            )

            case_id = input("Enter Case ID: ").strip()
            case = self._find_case(case_id)

            if not case:
                raise ValueError("Case not found.")

            new_classification = input(
                "New classification (suspected/confirmed/discarded): "
            ).strip()

            if new_classification:
                validate_classification_status(new_classification)
                case.update_classification(new_classification)

            new_patient_status = input(
                "New patient status (under_treatment/recovered/deceased): "
            ).strip()

            if new_patient_status:
                validate_patient_status(new_patient_status)
                case.update_patient_status(new_patient_status)

            self._save_cases()
            console.print(
                "[bold green]✅ Case updated successfully.[/bold green]")

        except (ValueError, PermissionError) as e:
            console.print(f"[bold red]❌ Update failed: {e}[/bold red]")

    def confirm_disease(self, current_user):
        """Confirm disease for a suspected case."""
        try:
            self._authorize(
                current_user.role == "health_worker",
                "Only health workers can confirm diseases."
            )

            case_id = input("Enter Case ID: ").strip()
            case = self._find_case(case_id)

            if not case:
                raise ValueError("Case not found.")

            disease = input("Confirmed disease: ").strip()
            validate_non_empty(disease, "Confirmed disease")

            case.confirm_disease(disease)
            self._save_cases()

            console.print("[bold green]✅ Disease confirmed.[/bold green]")

        except (ValueError, PermissionError) as e:
            console.print(f"[bold red]❌ Confirmation failed: {e}[/bold red]")

    def delete_case(self, current_user):
        """Delete a case with role-based permissions."""
        try:
            case_id = input("Enter Case ID to delete: ").strip()
            case = self._find_case(case_id)

            if not case:
                raise ValueError("Case not found.")

            if current_user.role == "admin":
                pass
            elif current_user.role == "health_worker":
                self._authorize(
                    case.reported_by == current_user.id,
                    "Health workers can only delete their own cases."
                )
            elif current_user.role == "community":
                self._authorize(
                    case.reported_by == current_user.id and
                    case.classification_status == "suspected",
                    "Community users can only delete their own suspected cases."
                )
            else:
                raise PermissionError("Invalid role.")

            self.cases = [c for c in self.cases if c.id != case_id]
            self._save_cases()

            console.print(
                "[bold green]✅ Case deleted successfully.[/bold green]")

        except (ValueError, PermissionError) as e:
            console.print(f"[bold red]❌ Deletion failed: {e}[/bold red]")

    def view_cases(self, user=None):
        """Display cases in a Rich table."""
        if not self.cases:
            console.print("[bold red]No cases found.[/bold red]")
            return

        table = Table(title="Outbreak Cases")
        table.add_column("ID", style="cyan")
        table.add_column("Patient", style="magenta")
        table.add_column("Age", style="green")
        table.add_column("Region", style="yellow")
        table.add_column("Symptoms", style="blue")
        table.add_column("Possible", style="blue")
        table.add_column("Confirmed", style="blue")
        table.add_column("Classification", style="red")
        table.add_column("Patient Status", style="red")
        table.add_column("Date", style="white")

        for case in self.cases:
            if user and user.role == "community" and case.reported_by != user.id:
                continue

            table.add_row(
                case.id,
                case.patient_name,
                str(case.age),
                case.region_id,
                ", ".join(case.symptoms) if case.symptoms else "-",
                case.possible_disease or "-",
                case.confirmed_disease or "-",
                case.classification_status,
                case.patient_status,
                case.date_reported
            )

        console.print(table)

    def view_summary(self):
        """Display outbreak and patient summaries."""
        summary = self.generate_summary()

        classification_table = Table(title="Outbreak Classification Summary")
        classification_table.add_column("Status", style="cyan")
        classification_table.add_column("Count", style="magenta")

        for status, count in summary["classification_summary"].items():
            classification_table.add_row(status, str(count))

        patient_table = Table(title="Patient Outcome Summary")
        patient_table.add_column("Status", style="green")
        patient_table.add_column("Count", style="yellow")

        for status, count in summary["patient_summary"].items():
            patient_table.add_row(status, str(count))

        console.print(classification_table)
        console.print(patient_table)

    def generate_summary(self):
        """Generate summary statistics for cases."""

        classification_summary = {
            "suspected": 0,
            "confirmed": 0,
            "discarded": 0
        }

        patient_summary = {
            "under_treatment": 0,
            "recovered": 0,
            "deceased": 0
        }

        for case in self.cases:
            if case.classification_status in classification_summary:
                classification_summary[case.classification_status] += 1

            if case.patient_status in patient_summary:
                patient_summary[case.patient_status] += 1

        return {
            "classification_summary": classification_summary,
            "patient_summary": patient_summary
        }
