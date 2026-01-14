from sqlalchemy.orm import Session
from app.common.models import Doctor
from datetime import datetime

def get_doctors(db: Session, department: str | None = None):
    query = db.query(Doctor).filter(Doctor.is_active.is_(True))
    if department:
        query = query.filter(Doctor.department == department)
    return query.order_by(Doctor.doctor_id.asc()).all()

def create_doctor(db: Session, doctor_name: str, department: str):
    doctor = Doctor(
        doctor_name=doctor_name,
        department = department
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

def find_doctor_by_id(db: Session, doctor_id: int):
    return (
        db.query(Doctor).filter(Doctor.doctor_id==doctor_id, Doctor.is_active.is_(True)).first()
    )

def update_doctor(db: Session, doctor_id: int, doctor_name: str | None, department: str | None):
    doctor = find_doctor_by_id(db, doctor_id)

    if not doctor:
        return None
    
    if doctor_name is not None:
        doctor.doctor_name = doctor_name

    if department is not None:
        doctor.department = department

    db.commit()
    db.refresh(doctor)
    return doctor

def delete_doctor(db: Session, doctor_id: int):
    doctor = find_doctor_by_id(db, doctor_id)

    if not doctor:
        return None
    
    doctor.is_active = False
    doctor.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(doctor)

    return doctor