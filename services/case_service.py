# services/case_service.py
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
    """Service layer for managing outbreak cases."""

    def __init__(self):
        self.cases = self._load_cases()

    # ----------------------------
    # Internal Helpers
    # ----------------------------
    def _load_cases(self):
        data = load_json(CASES_FILE)
        return [Case.from_dict(case) for case in data]

    def _save_cases(self):
        save_json(CASES_FILE, [case.to_dict() for case in self.cases])

    def _find_case_or_raise(self, case_id: str) -> Case:
        case = next((c for c in self.cases if c.id == case_id), None)
        if not case:
            raise ValueError("Case not found.")
        return case

    def _authorize(self, condition: bool, message: str):
        if not condition:
            raise PermissionError(message)

    def _input_optional(self, prompt: str):
        """Helper for optional input fields."""
        value = input(prompt).strip()
        return value or None

    # ----------------------------
    # Public Methods
    # ----------------------------
    def add_case(self, current_user):
        """Add a new outbreak case."""
        try:
            patient_name = input("Patient name: ").strip()
            validate_non_empty(patient_name, "Patient name")

            age = int(input("Age: "))
            validate_age(age)

            region_id = input("Region ID: ").strip()
            validate_non_empty(region_id, "Region ID")

            notes = self._input_optional("Additional notes (optional): ")
            case_id = str(uuid.uuid4())
            date_reported = datetime.now().strftime("%Y-%m-%d")

            if current_user.role == "community":
                symptoms = [
                    s.strip() for s in input(
                        "Symptoms (comma separated): "
                    ).split(",") if s.strip()
                ]
                possible_disease = self._input_optional(
                    "Possible disease (optional): "
                )

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
                    confirmed_disease=None,
                    notes=notes
                )
            else:  # health_worker or admin
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
                    confirmed_disease=disease if classification_status == "confirmed" else None,
                    notes=notes
                )

            self.cases.append(new_case)
            self._save_cases()
            console.print(
                "[bold green]✅ Case added successfully.[/bold green]")

        except (ValueError, PermissionError) as e:
            console.print(f"[bold red]❌ Failed to add case: {e}[/bold red]")

    def update_case_status(self, current_user):
        """Update classification, patient status, and notes."""
        try:
            self._authorize(
                current_user.role != "community",
                "Community users cannot update case status."
            )

            case_id = input("Enter Case ID: ").strip()
            case = self._find_case_or_raise(case_id)

            # Update classification
            new_classification = input(
                "New classification (suspected/confirmed/discarded): "
            ).strip()
            if new_classification:
                validate_classification_status(new_classification)
                case.update_classification(new_classification)

                if new_classification == "confirmed":
                    disease = input("Confirmed disease: ").strip()
                    validate_non_empty(disease, "Confirmed disease")
                    case.confirm_disease(disease)

            # Update patient status
            new_patient_status = input(
                "New patient status (under_treatment/recovered/deceased): "
            ).strip()
            if new_patient_status:
                validate_patient_status(new_patient_status)
                case.update_patient_status(new_patient_status)

            # Update notes
            new_notes = self._input_optional("Update notes (optional): ")
            if new_notes:
                case.notes = new_notes

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
            case = self._find_case_or_raise(case_id)

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
            case = self._find_case_or_raise(case_id)

            if current_user.role == "admin":
                pass
            elif current_user.role == "health_worker":
                self._authorize(
                    case.reported_by == current_user.id,
                    "Health workers can only delete their own cases."
                )
            elif current_user.role == "community":
                self._authorize(
                    case.reported_by == current_user.id and case.classification_status == "suspected",
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

    # ----------------------------
    # Viewing Methods
    # ----------------------------
    def view_cases(self, user=None):
        """Display cases in a Rich table."""
        if not self.cases:
            console.print("[bold red]No cases found.[/bold red]")
            return

        table = Table(title="Outbreak Cases", show_lines=True)
        table.add_column("ID", style="cyan", overflow="fold")
        table.add_column("Patient", style="magenta")
        table.add_column("Age", style="green")
        table.add_column("Region", style="yellow")
        table.add_column("Symptoms", style="blue")
        table.add_column("Possible Disease", style="blue")
        table.add_column("Classification", style="red", justify="center")
        table.add_column("Patient Status", style="red", justify="center")
        table.add_column("Date", style="white")
        table.add_column("Notes", style="italic")

        for case in self.cases:
            # Community users only see their own cases
            if user and user.role == "community" and case.reported_by != user.id:
                continue

            # Display confirmed disease in classification
            classification_display = case.classification_status
            if case.classification_status == "confirmed" and case.confirmed_disease:
                classification_display = f"confirmed ({case.confirmed_disease})"

            table.add_row(
                case.id,
                case.patient_name,
                str(case.age),
                case.region_id,
                ", ".join(case.symptoms) if case.symptoms else "-",
                case.possible_disease or "-",
                classification_display,
                case.patient_status,
                case.date_reported,
                case.notes or "-"
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
            "suspected": 0, "confirmed": 0, "discarded": 0}
        patient_summary = {"under_treatment": 0, "recovered": 0, "deceased": 0}

        for case in self.cases:
            cls_status = case.classification_status.lower()
            if cls_status in classification_summary:
                classification_summary[cls_status] += 1

            pat_status = case.patient_status.lower()
            if pat_status in patient_summary:
                patient_summary[pat_status] += 1

        return {
            "classification_summary": classification_summary,
            "patient_summary": patient_summary
        }
