

class Case:
    
    VALID_STATUSES = {"Suspected", "Confirmed", "Recovered", "Deceased"}

    #Define allowed transitions
    ALLOWED_TRANSITIONS = {
        "Suspected": {"Confirmed"},
        "Confirmed": {"Recovered", "Deceased"},
        "Recovered": set(),
        "Deceased": set()
    }

    def __init__(self, case_id, disease_name, patient_code, patient_age, patient_gender, date_reported, region_id, assigned_officer, status="Suspected"):
        self.__case_id = case_id
        self.disease_name = disease_name
        self.__patient_code = patient_code
        self.__patient_age = patient_age
        self.__patient_gender = patient_gender
        self.__date_reported = date_reported
        self.region_id = region_id
        self.__assigned_officer = assigned_officer

        if status not in Case.VALID_STATUSES:
            raise ValueError("Invalid initial status")
        
        self.__status = status
        

        #Getters
    @property
    def case_id(self):
        return self.__case_id
    
    @property
    def patient_code(self):
        return self.__patient_code
    
    @property
    def patient_age(self):
        return self.__patient_age
    
    @property
    def patient_gender(self):
        return self.__patient_gender
    
    @property
    def date_reported(self):
        return self.__date_reported

    @property
    def status(self):
        return self.__status
    
    #Controlled mutations

    def update_status(self, new_status):
        if new_status not in Case.VALID_STATUSES:
            raise ValueError("Invalid status")
        
        allowed = Case.ALLOWED_TRANSITIONS[self.__status]

        if new_status not in allowed:
            raise ValueError(f"Invalid transition from {self.__status} to {new_status}")
        
        self.__status = new_status

    def set_patient_age(self, age):
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Patient age must be a positive integer.")
        
        self.__patient_age = age

    def set_patient_gender(self, gender):
        valid_genders = {"Male", "Female", "Other"}
        if gender not in valid_genders:
            raise ValueError("Invalid gender.")
        
        self.__patient_gender = gender


    #Serialization

    def to_dict(self):
        return {
            "case_id": self.__case_id,
            "disease_name": self.disease_name,
            "patient_code": self.__patient_code,
            "patient_age": self.__patient_age,
            "patient_gender": self.__patient_gender,
            "date_reported": self.__date_reported,
            "region_id": self.region_id,
            "assigned_officer": self.__assigned_officer,
            "status": self.__status
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            case_id=data["case_id"],
            disease_name=data["disease_name"],
            patient_code=data["patient_code"],
            patient_age=data["patient_age"],
            patient_gender=data["patient_gender"],
            date_reported=data["date_reported"],
            region_id=data["region_id"],
            assigned_officer=data.get("assigned_officer"),
            status=data.get("status", "Suspected")
        )
    
    #String representation
    def display_summary(self):
        return f"{self.__case_id} | {self.disease_name} | {self.__status}"

        

