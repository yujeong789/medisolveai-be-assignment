import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.admin.doctor import repository

def get_doctors(db: Session, department: str | None = None):
    return repository.get_doctors(db, department)

def creat_doctor(db:Session, request):
    return repository.create_doctor(db, request.doctor_name, request.department)
    
def update_doctor(db:Session, doctor_id: int, doctor_name: str | None, department: str | None):
    doctor = repository.update_doctor(db, doctor_id, doctor_name, department)
    if not doctor:
        raise HTTPException(404, "해당 의사가 존재하지 않습니다.")
    return doctor

def delete_doctor(db:Session, doctor_id: int):
    doctor = repository.delete_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(404, "해당 의사가 존재하지 않습니다.")
    return doctor