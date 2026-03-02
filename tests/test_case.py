import pytest
from models.case import Case


# BASE CASES (normal expected behaviour)

def test_case_creation_base():
    """
    Base Case:
    Creating a normal suspected case should succeed.
    """
    case = Case(
        id="C001",
        patient_name="Alice",
        age=25,
        region_id="Nairobi",
        reported_by="HW001",
        date_reported="2026-03-02",
        classification_status="suspected",
        patient_status="under_treatment"
    )

    assert case.id == "C001"
    assert case.region_id == "Nairobi"
    assert case.classification_status == "suspected"
    assert case.patient_status == "under_treatment"


def test_update_classification_base():
    """
    Base Case:
    Updating classification from suspected to confirmed should succeed.
    """
    case = Case(
        id="C002",
        patient_name="Bob",
        age=30,
        region_id="Mombasa",
        reported_by="HW002",
        date_reported="2026-03-02",
        classification_status="suspected",
        patient_status="under_treatment"
    )

    case.update_classification("confirmed")
    assert case.classification_status == "confirmed"


def test_update_patient_status_base():
    """
    Base Case:
    Updating patient status from under_treatment to recovered should succeed.
    """
    case = Case(
        id="C003",
        patient_name="Charlie",
        age=40,
        region_id="Kisumu",
        reported_by="HW003",
        date_reported="2026-03-02",
        classification_status="confirmed",
        patient_status="under_treatment"
    )

    case.update_patient_status("recovered")
    assert case.patient_status == "recovered"


# EDGE CASES (boundary or unusual but valid input)


def test_status_case_insensitive_edge():
    """
    Edge Case:
    Status input should be normalized / accepted as lowercase.
    """
    case = Case(
        id="C004",
        patient_name="Diana",
        age=20,
        region_id="Nakuru",
        reported_by="HW004",
        date_reported="2026-03-02",
        classification_status="CONFIRMED".lower(),
        patient_status="under_treatment"
    )

    assert case.classification_status == "confirmed"


def test_empty_symptoms_edge():
    """
    Edge Case:
    Symptoms list defaults to empty if not provided.
    """
    case = Case(
        id="C005",
        patient_name="Eve",
        age=35,
        region_id="Eldoret",
        reported_by="HW005",
        date_reported="2026-03-02"
    )

    assert case.symptoms == []


# ERROR / VALIDATION TESTS


def test_invalid_classification_raises_error():
    """
    Validation:
    Invalid classification should raise ValueError.
    """
    with pytest.raises(ValueError):
        Case(
            id="C006",
            patient_name="Frank",
            age=50,
            region_id="Nairobi",
            reported_by="HW006",
            date_reported="2026-03-02",
            classification_status="invalid_status"
        )


def test_invalid_patient_status_raises_error():
    """
    Validation:
    Invalid patient status should raise ValueError.
    """
    with pytest.raises(ValueError):
        Case(
            id="C007",
            patient_name="Grace",
            age=45,
            region_id="Mombasa",
            reported_by="HW007",
            date_reported="2026-03-02",
            patient_status="dead"
        )


def test_confirm_disease_empty_name_raises_error():
    """
    Validation:
    Confirming disease with empty name should raise ValueError.
    """
    case = Case(
        id="C008",
        patient_name="Hank",
        age=28,
        region_id="Kisumu",
        reported_by="HW008",
        date_reported="2026-03-02"
    )
    with pytest.raises(ValueError):
        case.confirm_disease("")


# PURE METHOD / DATA TRANSFORMATION TESTS

def test_confirm_disease_updates_classification():
    """
    Pure Method:
    confirm_disease should set confirmed_disease and update classification.
    """
    case = Case(
        id="C009",
        patient_name="Ivy",
        age=32,
        region_id="Nairobi",
        reported_by="HW009",
        date_reported="2026-03-02",
        classification_status="suspected"
    )

    case.confirm_disease("Cholera")
    assert case.confirmed_disease == "Cholera"
    assert case.classification_status == "confirmed"


def test_to_dict_and_from_dict():
    """
    Pure Method:
    to_dict and from_dict should correctly serialize and recreate the object.
    """
    case = Case(
        id="C010",
        patient_name="Jack",
        age=29,
        region_id="Nakuru",
        reported_by="HW010",
        date_reported="2026-03-02",
        classification_status="confirmed",
        patient_status="under_treatment",
        symptoms=["fever", "cough"],
        possible_disease="Flu",
        confirmed_disease=None
    )

    data = case.to_dict()
    new_case = Case.from_dict(data)

    assert new_case.id == case.id
    assert new_case.patient_name == case.patient_name
    assert new_case.symptoms == ["fever", "cough"]
    assert new_case.possible_disease == "Flu"
    assert new_case.confirmed_disease is None


def test_string_representation():
    """
    Pure Method:
    __str__ should return readable formatted output.
    """
    case = Case(
        id="C011",
        patient_name="Kim",
        age=31,
        region_id="Eldoret",
        reported_by="HW011",
        date_reported="2026-03-02",
        classification_status="suspected"
    )

    string_output = str(case)
    assert "Case[C011]" in string_output
    assert "Classification: suspected" in string_output