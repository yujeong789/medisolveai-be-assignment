from datetime import datetime, time, date
from app.common.models import Doctor, Treatment, HospitalSlot, OperatingHour, Appointment
from sqlalchemy import text

def test_create_reservation_success(client, db_session):
    # 1. 데이터 완전 초기화 (모든 테이블)
    db_session.execute(text("DELETE FROM appointments"))
    db_session.execute(text("DELETE FROM hospital_slots"))
    db_session.execute(text("DELETE FROM operating_hours"))
    db_session.execute(text("DELETE FROM patients"))
    db_session.execute(text("DELETE FROM treatments"))
    db_session.execute(text("DELETE FROM doctors"))
    db_session.commit()
    db_session.expire_all()
    
    # 2. 고유한 의사 생성 (이름에 타임스탬프를 넣어 중복 방지)
    doctor = Doctor(doctor_name="테스트의사", department="피부과", is_active=True)
    treatment = Treatment(treatment_name="기본관리", duration_minutes=30, price=50000)
    db_session.add(doctor)
    db_session.add(treatment)
    db_session.commit()
    db_session.refresh(doctor)
    db_session.refresh(treatment)

    # 3. 2026-01-20 (화요일, weekday=1) 로 날짜 변경 (이전 테스트와 겹치지 않게)
    target_date = date(2026, 1, 20)
    test_start_time = datetime.combine(target_date, time(14, 0)) # 오후 2시

    operating = OperatingHour(
        day_of_week=target_date.weekday(), # 1
        open_time=time(9, 0),
        close_time=time(18, 0),
        is_opened=True,
    )

    # 4. 슬롯 생성 (예약하려는 14:00 시간대에 딱 맞춰 생성)
    slot = HospitalSlot(
        start_time=time(14, 0), 
        end_time=time(14, 30), 
        max_capacity=10
    )

    db_session.add_all([operating, slot])
    db_session.commit()

    # 5. API 요청
    payload = {
        "patient_name": "신규환자",
        "phone": "010-9999-8888",
        "doctor_id": doctor.doctor_id,
        "treatment_id": treatment.treatment_id,
        "start_time": test_start_time.isoformat() # "2026-01-20T14:00:00"
    }

    response = client.post("/api/v1/patient/reservation", json=payload)
    
    # 실패 시 에러 메시지 확인용
    if response.status_code != 200:
        print(f"\n[FAIL REASON]: {response.json()}")

    assert response.status_code == 200


def test_create_reservation_duplicate_fail(client, db_session):
    # given
    doctor = Doctor(doctor_name="이유리", department="피부과")

    treatment = Treatment(
        treatment_name="기본관리",
        duration_minutes=30,
        price=50000,
        description="기본"
    )

    operating = OperatingHour(
        day_of_week=3,
        open_time=time(9, 0),
        close_time=time(18, 0),
        is_opened=True
    )

    slot = HospitalSlot(
        start_time=time(10, 0),
        end_time=time(11, 0),
        max_capacity=3
    )

    db_session.add_all([doctor, treatment, operating, slot])
    db_session.commit()

    # 기존 예약 (중복 유발)
    appointment = Appointment(
        patient_id="test",
        doctor_id=doctor.doctor_id,
        treatment_id=treatment.treatment_id,
        start_time=datetime(2026, 1, 15, 10, 0),
        end_time=datetime(2026, 1, 15, 10, 30),
    )

    db_session.add(appointment)
    db_session.commit()

    payload = {
        "patient_name": "이수호",
        "phone": "010-9999-8888",
        "doctor_id": doctor.doctor_id,
        "treatment_id": treatment.treatment_id,
        "start_time": "2026-01-15T10:00:00"
    }

    # when
    response = client.post("/api/v1/patient/reservation", json=payload)

    # then
    assert response.status_code == 400
