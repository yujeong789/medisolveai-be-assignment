from sqlalchemy.orm import Session
from app.common.models import Treatment

def find_treatments(db: Session):
    return (
        db.query(Treatment)
        .order_by(Treatment.treatment_id)
        .all()
    )

def create_treatment(db: Session, request):
    treatment = Treatment(
        treatment_name=request.treatment_name,
        duration_minutes=request.duration_minutes,
        price=request.price,
        description=request.description
    )
    db.add(treatment)
    db.commit()
    db.refresh(treatment)
    return treatment

def update_treatment(
    db: Session,
    treatment_id: int,
    treatment_name: str | None,
    duration_minutes: int | None,
    price: int | None,
    description: str | None,
):
    treatment = (
        db.query(Treatment)
        .filter(Treatment.treatment_id == treatment_id)
        .first()
    )

    if not treatment:
        return None

    if treatment_name is not None:
        treatment.treatment_name = treatment_name
    if duration_minutes is not None:
        treatment.duration_minutes = duration_minutes
    if price is not None:
        treatment.price = price
    if description is not None:
        treatment.description = description

    db.commit()
    db.refresh(treatment)
    return treatment

def delete_treatment(db: Session, treatment_id: int):
    treatment = (
        db.query(Treatment)
        .filter(Treatment.treatment_id == treatment_id)
        .first()
    )

    if not treatment:
        return None

    db.delete(treatment)
    db.commit()
    return treatment
"""
treatment_id = Column(Integer, primary_key=True, autoincrement=True)
    treatment_name = Column(String(255), nullable=False) # 시술명
    duration_minutes = Column(Integer, nullable=False) # 소요시간 (30분 단위)
    price = Column(Integer, nullable=False) # 가격
    description
"""