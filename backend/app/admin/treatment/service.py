import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.admin.treatment import repository
from datetime import datetime, date, timedelta

def get_treatment_list(db: Session):
    return repository.find_treatments(db)

def create_treatment(db: Session, request):
    return repository.create_treatment(db, request)

def update_treatment(db: Session, treatment_id: int, request):
    treatment = repository.update_treatment(
        db,
        treatment_id,
        request.treatment_name,
        request.duration_minutes,
        request.price,
        request.description
    )
    if not treatment:
        raise HTTPException(404, "진료 항목이 존재하지 않습니다.")
    return treatment

def delete_treatment(db: Session, treatment_id: int):
    treatment = repository.delete_treatment(db, treatment_id)
    if not treatment:
        raise HTTPException(404, "진료 항목이 존재하지 않습니다.")
    return treatment

"""
treatment_id = Column(Integer, primary_key=True, autoincrement=True)
    treatment_name = Column(String(255), nullable=False) # 시술명
    duration_minutes = Column(Integer, nullable=False) # 소요시간 (30분 단위)
    price = Column(Integer, nullable=False) # 가격
    description
"""