import pytest
from models.case import Case

def create_sample_case():
    return Case(
        case_id=1,
        disease_name="Cholera",
        patient_code="P001",
        patient_age=15,
        patient_gender="Male",
        date_reported="2026-02-27",
        region_id="Nairobi",
        assigned_officer="OFF123",
        status="Suspected"
    )

def test_case_creation():
    case = create_sample_case()
    assert case.case_id == 1
    assert case.status == "Suspected"

def test_valid_transition_suspected_to_confirmed():
    case = create_sample_case()
    case.update_status("Confirmed")
    assert case.status == "Confirmed"

def test_invalid_transition_suspected_to_recovered():
    case = create_sample_case()
    with pytest.raises(ValueError):
        case.update_status("Recovered")

def test_valid_transition_confirmed_to_recovered():
    case = create_sample_case()
    case.update_status("Confirmed")
    case.update_status("Recovered")
    assert case.status == "Recovered"

def test_terminal_state_no_transition():
    case = create_sample_case()
    case.update_status("Confirmed")
    case.update_status("Recovered")
    with pytest.raises(ValueError):
        case.update_status("Confirmed")

def test_invalid_status():
    case = create_sample_case()
    with pytest.raises(ValueError):
        case.update_status("InvalidStatus")

def test_invalid_age():
    case = create_sample_case()
    with pytest.raises(ValueError):
        case.set_patient_age(-5)

def test_serialization():
    case = create_sample_case()
    data = case.to_dict()
    new_case = Case.from_dict(data)

    assert new_case.case_id == case.case_id
    assert new_case.status == case.status