import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.admin.appointment import repository
from datetime import datetime

def get_appointment_list(
    db: Session,
    created_at: datetime | None = None,
    start_time: datetime | None = None,
    doctor_id: int | None = None,
    treatment_id: int | None = None,
    status: str | None = None,
    is_first_visit: bool | None = None,
):
    return repository.find_appointments(
        db,
        created_at,
        start_time,
        doctor_id,
        treatment_id,
        status,
        is_first_visit
    )


def update_appointment(db: Session, appointment_id: int, request):
    appointment = repository.update_appointment(
        db,
        appointment_id,
        request.status,
        request.memo
    )
    if not appointment:
        raise HTTPException(404, "해당 예약이 존재하지 않습니다.")
    return appointment
