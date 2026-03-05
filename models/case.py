# Represents a disease outbreak case

class Case:
    """
    Represents a reported outbreak case.

    Relationships:
    - Many cases belong to one Region (region_id)
    - Many cases reported by one User (reported_by)

    Fields:
    - symptoms: list of reported symptoms (community user)
    - possible_disease: suspected disease (community user)
    - confirmed_disease: verified disease (health worker)
    - notes: optional notes for both community and health worker entries
    - classification_status: outbreak classification (suspected, confirmed, discarded)
    - patient_status: patient outcome (under_treatment, recovered, deceased)
    """

    VALID_CLASSIFICATIONS = ["suspected", "confirmed", "discarded"]
    VALID_PATIENT_STATUSES = ["under_treatment", "recovered", "deceased"]

    def __init__(
        self,
        id: str,
        patient_name: str,
        age: int,
        region_id: str,
        reported_by: str,
        date_reported: str,
        classification_status: str = "suspected",
        patient_status: str = "under_treatment",
        symptoms=None,
        possible_disease=None,
        confirmed_disease=None,
        notes=None
    ):
        if classification_status not in self.VALID_CLASSIFICATIONS:
            raise ValueError(
                f"Invalid classification status. Must be one of {self.VALID_CLASSIFICATIONS}"
            )
        if patient_status not in self.VALID_PATIENT_STATUSES:
            raise ValueError(
                f"Invalid patient status. Must be one of {self.VALID_PATIENT_STATUSES}"
            )

        self.id = id
        self.patient_name = patient_name
        self.age = age
        self.region_id = region_id
        self.reported_by = reported_by
        self.date_reported = date_reported
        self.classification_status = classification_status
        self.patient_status = patient_status
        self.symptoms = symptoms or []
        self.possible_disease = possible_disease
        self.confirmed_disease = confirmed_disease
        self.notes = notes

    # ----------------------------
    # Helper Methods
    # ----------------------------
    def update_classification(self, new_status: str):
        if new_status not in self.VALID_CLASSIFICATIONS:
            raise ValueError(
                f"Invalid classification status. Must be one of {self.VALID_CLASSIFICATIONS}"
            )
        self.classification_status = new_status

    def update_patient_status(self, new_status: str):
        if new_status not in self.VALID_PATIENT_STATUSES:
            raise ValueError(
                f"Invalid patient status. Must be one of {self.VALID_PATIENT_STATUSES}"
            )
        self.patient_status = new_status

    def confirm_disease(self, disease_name: str):
        if not disease_name:
            raise ValueError("Confirmed disease name cannot be empty.")
        self.confirmed_disease = disease_name
        self.classification_status = "confirmed"

    # ----------------------------
    # Serialization
    # ----------------------------
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "age": self.age,
            "region_id": self.region_id,
            "reported_by": self.reported_by,
            "date_reported": self.date_reported,
            "classification_status": self.classification_status,
            "patient_status": self.patient_status,
            "symptoms": self.symptoms,
            "possible_disease": self.possible_disease,
            "confirmed_disease": self.confirmed_disease,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            patient_name=data["patient_name"],
            age=data["age"],
            region_id=data["region_id"],
            reported_by=data["reported_by"],
            date_reported=data["date_reported"],
            classification_status=data.get(
                "classification_status", "suspected"),
            patient_status=data.get("patient_status", "under_treatment"),
            symptoms=data.get("symptoms", []),
            possible_disease=data.get("possible_disease"),
            confirmed_disease=data.get("confirmed_disease"),
            notes=data.get("notes")
        )

    def __str__(self):
        return (
            f"Case[{self.id}] - {self.patient_name}, "
            f"Symptoms: {', '.join(self.symptoms) if self.symptoms else 'None'}, "
            f"Possible: {self.possible_disease or 'N/A'}, "
            f"Confirmed: {self.confirmed_disease or 'N/A'}, "
            f"Classification: {self.classification_status}, "
            f"Patient Status: {self.patient_status} ({self.date_reported}), "
            f"Notes: {self.notes or 'N/A'}"
        )
