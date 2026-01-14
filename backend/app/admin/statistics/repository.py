from sqlalchemy import func
from sqlalchemy.orm import Session
from app.common.models import Appointment

def count_appointments_by_status(db: Session):
    return (
        db.query(
            Appointment.status,
            func.count(Appointment.appointment_id)
        )
        .group_by(Appointment.status)
        .all()
    )

def count_appointments_by_day(db: Session):
    # MySQL의 경우 func.date()가 정확히 작동하며 'YYYY-MM-DD' 형식을 반환합니다.
    return (
        db.query(
            func.date(Appointment.start_time),
            func.count(Appointment.appointment_id)
        )
        .group_by(func.date(Appointment.start_time))
        .order_by(func.date(Appointment.start_time))
        .all()
    )

def count_appointments_by_time(db: Session):
    return (
        db.query(
            func.hour(Appointment.start_time).label("hour"),
            func.count(Appointment.appointment_id).label("count")
        )
        .group_by(func.hour(Appointment.start_time))
        .order_by(func.hour(Appointment.start_time))
        .all()
    )

def count_visit_ratio(db: Session):
    return (
        db.query(
            Appointment.is_first_visit,
            func.count(Appointment.appointment_id).label("count")
        )
        .group_by(Appointment.is_first_visit)
        .all()
    )

