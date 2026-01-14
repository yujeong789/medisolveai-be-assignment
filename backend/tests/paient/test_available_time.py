from datetime import date, time
from app.common.models import Doctor, OperatingHour, Appointment

def test_get_available_time_success(client, db_session):
    doctor = Doctor(doctor_name="임윤아", department="피부과")

    operating = OperatingHour(
        day_of_week=date.today().weekday(),
        open_time=time(9, 0),
        close_time=time(18, 0),
        is_opened=True
    )

    db_session.add_all([doctor, operating])
    db_session.commit()

    response = client.get(
        "/api/v1/patient/reservation/available",
        params={
            "date": date.today().isoformat(),
            "doctor_id": doctor.doctor_id
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_available_time_invalid_doctor(client, db_session):

    db_session.query(Appointment).delete()
    db_session.query(Doctor).delete()
    db_session.commit()

    doctor1 = Doctor(doctor_name="임윤아", department="피부과")
    doctor2 = Doctor(doctor_name="김세정", department="레이저")
    db_session.add_all([doctor1, doctor2])
    db_session.commit()
    db_session.refresh(doctor1)
    db_session.refresh(doctor2)
    db_session.add_all([doctor1, doctor2])
    db_session.commit()

    invalid_id = max(doctor1.doctor_id, doctor2.doctor_id) + 9999

    response = client.get(
        "/api/v1/patient/reservation/available",
        params={
            "date": date.today().isoformat(),
            "doctor_id": invalid_id
        }
    )
    assert response.json() == []