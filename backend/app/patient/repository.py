from sqlalchemy.orm import Session
from datetime import datetime

from app.common.models import (
    Doctor,
    Appointment,
    AppointmentStatus,
    Patient,
    HospitalSlot,
    OperatingHour,
    Treatment
)

# 의사 조회
def find_doctors_by_department(db: Session, department: str | None = None):
    query = db.query(Doctor)
    if department:
        query = query.filter(Doctor.department == department)
    return query.all()


# 운영 시간 조회
def find_operating_hour(db: Session, weekday: int):
    return db.query(OperatingHour).filter(
        OperatingHour.day_of_week == weekday,
        OperatingHour.is_opened == True
    ).first()

# 의사 정보 확인
def exists_by_doctor_and_time(db: Session, doctor_id: int, start: datetime, end: datetime):
    exists = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status != AppointmentStatus.CANCELLED,
        Appointment.start_time < end,
        Appointment.end_time > start
    ).first()
    return exists is not None

# 병원 수용량
def check_hospital_capacity(db: Session, start_dt: datetime, end_dt: datetime):
    slots = db.query(HospitalSlot).filter(
        HospitalSlot.start_time <= start_dt.time(),
        HospitalSlot.end_time >= end_dt.time()
    ).all()

    if not slots:
        return False  # 슬롯이 없으면 예약 불가

    for slot in slots:
        slot_start_dt = datetime.combine(start_dt.date(), slot.start_time)
        slot_end_dt = datetime.combine(start_dt.date(), slot.end_time)

        count = db.query(Appointment).filter(
            Appointment.status != AppointmentStatus.CANCELLED,
            Appointment.start_time < slot_end_dt,
            Appointment.end_time > slot_start_dt
        ).count()

        if count >= slot.max_capacity:
            return False

    return True




# 예약 코드로 예약 조회
def find_by_reservation_code(
    db: Session,
    reservation_code: str,
):
    return (
        db.query(Appointment)
        .filter(
            Appointment.reservation_code == reservation_code,
            Appointment.status != AppointmentStatus.CANCELLED,
        )
        .first()
    )

# 시술 
def find_treatment_by_id(db: Session, treatment_id: int):
    return db.query(Treatment).filter(Treatment.treatment_id == treatment_id).first()

# 환자 정보
def find_patient_by_name_ane_phone(db: Session, patient_name: str, phone: str):
    return db.query(Patient).filter(Patient.patient_name == patient_name, Patient.phone == phone).first()

# 환자 정보 생성
def create_patient(db: Session, patient_name: str, phone: str):
    patient = db.query(Patient).filter(Patient.phone == phone).first()
    if patient:
        return patient
    
    patient = Patient(patient_name=patient_name, phone=phone)
    db.add(patient)
    db.flush() 
    return patient

# 예약 저장
def save_appointment(db: Session, appointment: Appointment):
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


# 내 예약 조회
def find_by_patient(db: Session, patient_name: str, phone: str):
    return (
        db.query(Appointment)
        .join(Patient)
        .filter(Patient.patient_name == patient_name, Patient.phone == phone, Appointment.status != AppointmentStatus.CANCELLED)
        .order_by(Appointment.start_time.desc())
        .all()
    )


# 예약 취소
def update_appointment_to_cancelled(db: Session, reservation_code: str):
    appointment = db.query(Appointment).filter(
        Appointment.reservation_code == reservation_code,
        Appointment.status != AppointmentStatus.CANCELLED
    ).first()

    if not appointment:
        return None
    
    appointment.status = AppointmentStatus.CANCELLED
    db.commit()
    db.refresh(appointment) # 변경된 상태(status)를 반영해서 가져옴
    return appointment


