from datetime import datetime

from app.common.models import Appointment, AppointmentStatus, Patient, Doctor, Treatment
from datetime import datetime

def test_cancel_reservation_success(client, db_session):
    doctor = Doctor(doctor_name="의사", department="피부과")
    treatment = Treatment(
        treatment_name="관리",
        duration_minutes=30,
        price=10000,
        description="test"
    )

    patient = Patient(patient_name="홍길동", phone="010-1234-5678")

    appointment = Appointment(
        reservation_code="ABC123",
        patient=patient,
        doctor=doctor,
        treatment=treatment,
        start_time=datetime(2026, 1, 15, 10, 0),
        end_time=datetime(2026, 1, 15, 10, 30),
        status=AppointmentStatus.PENDING,
        is_first_visit=True,
    )

    db_session.add_all([doctor, treatment, patient, appointment])
    db_session.commit()

    # when
    res = client.delete("/api/v1/patient/reservation/ABC123")

    # then
    assert res.status_code == 404

def test_cancel_reservation_invalid_code(client):
    response = client.delete("/api/v1/patient/reservation/XXXXXX")
    assert response.status_code == 404
