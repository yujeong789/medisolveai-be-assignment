from sqlalchemy.orm import Session
from app.common.models import Appointment, AppointmentStatus

from sqlalchemy.orm import Session
from app.common.models import Appointment, AppointmentStatus
from datetime import datetime

def find_appointments(
    db: Session,
    created_at: datetime | None = None,
    start_time: datetime | None = None,
    doctor_id: int | None = None,
    treatment_id: int | None = None,
    status: str | None = None,
    is_first_visit: bool | None = None,
):
    query = db.query(Appointment)

    if created_at:
        query = query.filter(Appointment.created_at >= created_at)

    if start_time:
        query = query.filter(Appointment.start_time >= start_time)

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)

    if treatment_id:
        query = query.filter(Appointment.treatment_id == treatment_id)

    if status:
        query = query.filter(Appointment.status == AppointmentStatus(status))

    if is_first_visit is not None:
        query = query.filter(Appointment.is_first_visit == is_first_visit)

    return query.order_by(Appointment.start_time).all()


def update_appointment(
    db: Session,
    appointment_id: int,
    status: str | None,
    memo: str | None,
):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.appointment_id == appointment_id)
        .first()
    )

    if not appointment:
        return None

    if status:
        appointment.status = AppointmentStatus(status)

    if memo is not None:
        appointment.memo = memo

    db.commit()
    db.refresh(appointment)
    return appointment




