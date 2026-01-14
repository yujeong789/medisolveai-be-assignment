import random
import string
import logging
from datetime import datetime, timedelta, date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.patient import repository

from app.common.models import (
    Patient,
    Doctor,
    Treatment,
    Appointment,
    AppointmentStatus,
)

# 로깅 설정
logger = logging.getLogger("uvicorn.error")
 
# 의사 목록 조회
def get_doctors(department: str | None, db: Session):
    return repository.find_doctors_by_department(db, department)


# 예약 가능 시간 조회
def get_available_reservations(target_date: date, doctor_id: int, db: Session):
    logger.info(f"🔥🔥 API 호출됨 - 날짜: {target_date}, 의사ID: {doctor_id}")
    
    doctor_exists = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor_exists:
        logger.warning(f"⚠️ 존재하지 않는 의사 ID 조회: {doctor_id}")
        return []
    
    now = datetime.now()
    today = now.date()
    weekday = target_date.weekday()
    operating = repository.find_operating_hour(db, weekday)
    if not operating:
        return []

    logger.info(f"🔥🔥 [통과] 운영시간 확인: {operating.open_time} ~ {operating.close_time}")   

    # 운영 시간
    open_dt = datetime.combine(target_date, operating.open_time)
    close_dt = datetime.combine(target_date, operating.close_time)
    break_start = datetime.combine(target_date, operating.break_start_time) if operating.break_start_time else None
    break_end = datetime.combine(target_date, operating.break_end_time) if operating.break_end_time else None

    if target_date == today:
        current = max(open_dt, now)
        minutes_to_add = (15 - (current.minute % 15)) % 15
        current = current.replace(second=0, microsecond=0) + timedelta(minutes=minutes_to_add)
    else:
        current = open_dt

    # 모든 시술 정보
    available = []

    while current + timedelta(minutes=15) <= close_dt:
        
        # 1. 점심시간 제외
        if break_start and break_start <= current < break_end:
            current += timedelta(minutes=15)
            continue

        # 2. 15분 단위의 슬롯 설정
        slot_end = current + timedelta(minutes=15)

        # 3. 의사 중복 여부 체크
        if repository.exists_by_doctor_and_time(db, doctor_id, current, slot_end):
            current += timedelta(minutes=15)
            continue

        # 4. 병원 전체 수용 인원 체크
        if not repository.check_hospital_capacity(db, current, slot_end):
            current += timedelta(minutes=15)
            continue

        # 5. 모든 조건을 통과하면 15분 슬롯 추가
        available.append({
            "start_time": current,
            "end_time": slot_end,
        })

        # 다음 15분으로 이동
        current += timedelta(minutes=15)

    return available


# 예약 코드 생성
def generate_reservation_code(size: int = 6) -> str:
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choices(characters, k=size))

def generate_unique_reservation_code(db: Session) -> str:
    while True:
        code = generate_reservation_code()
        if not repository.find_by_reservation_code(db, code):
            return code

# 예약 생성
def create_reservation(request, db: Session):
    treatment = repository.find_treatment_by_id(db, request.treatment_id)
    if not treatment:
        raise HTTPException(404, "시술 정보가 없습니다.")

    end_time = request.start_time + timedelta(minutes=treatment.duration_minutes)

    # 중복 예약 방지
    if repository.exists_by_doctor_and_time(db, request.doctor_id, request.start_time, end_time):
        raise HTTPException(400, "이미 예약된 시간입니다.")
    # 병원 슬롯 수용 인원 체크
    if not repository.check_hospital_capacity(db, request.start_time, end_time):
        raise HTTPException(400, "해당 시간대에 병원 수용량이 가득 찼습니다.")

    # 환자 조회 or 생성
    patient = repository.find_patient_by_name_ane_phone(db, request.patient_name, request.phone)
    is_first = False
    if not patient:
        patient = repository.create_patient(db, request.patient_name, request.phone)
        is_first = True

    reservation_code = generate_unique_reservation_code(db)

    # 예약 객체 생성 및 저장
    appointment = Appointment(
        reservation_code=generate_unique_reservation_code(db),
        patient_id=patient.patient_id,
        doctor_id=request.doctor_id,
        treatment_id=request.treatment_id,
        start_time=request.start_time,
        end_time=end_time,
        is_first_visit=is_first,
    )

    saved = repository.save_appointment(db, appointment)

    return {
        "reservation_code": saved.reservation_code,
        "doctor_name": saved.doctor.doctor_name,
        "treatment_name": saved.treatment.treatment_name,
        "start_time": saved.start_time,
        "end_time": saved.end_time,
        "status": saved.status,
    }


# 내 예약 조회
def read_my_reservation(request, db: Session):
    appointments = repository.find_by_patient(db, request.patient_name, request.phone)
    return [{
        "reservation_code": a.reservation_code,
        "doctor_name": a.doctor.doctor_name,
        "treatment_name": a.treatment.treatment_name,
        "start_time": a.start_time,
        "end_time": a.end_time,
        "status": a.status,
    } for a in appointments]


# 예약 취소
def cancel_reservation(reservation_code: str, db: Session):
    appointment = repository.update_appointment_to_cancelled(db, reservation_code)
    if not appointment:
        raise HTTPException(404, "예약이 존재하지 않습니다.")
    
    return {
        "reservation_code": appointment.reservation_code,
        "doctor_name": appointment.doctor.doctor_name,
        "treatment_name": appointment.treatment.treatment_name,
        "start_time": appointment.start_time,
        "end_time": appointment.end_time,
        "status": appointment.status,
    }
    
        

