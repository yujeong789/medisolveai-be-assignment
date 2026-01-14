import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.admin.statistics import repository

# service.py
def get_appointment_by_status(db: Session):
    appointments = repository.count_appointments_by_status(db)
    return {
        "data": [
            {"status": appointment[0], "count": appointment[1]} for appointment in appointments]
        }

def get_appointment_trend(db: Session, trend_type: str):
    if trend_type == "day":
        appointments = repository.count_appointments_by_day(db)
    elif trend_type == "time":
        appointments = repository.count_appointments_by_time(db)
    else:
        raise HTTPException(400, "trend_type는 day 또는 time 이어야 합니다.")
    
    return {
        "type": trend_type, 
        "data": [
            {"key": str(appointment[0]), "count": appointment[1]} for appointment in appointments
            ]
        }

def get_appointment_by_visit(db: Session):
    appointments = repository.count_visit_ratio(db)
    return {
        "data": [
            {"is_first_visit": appointment[0], "count": appointment[1]} for appointment in appointments
            ]
        }
