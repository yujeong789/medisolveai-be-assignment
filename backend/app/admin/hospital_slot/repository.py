from sqlalchemy.orm import Session
from app.common.models import HospitalSlot

# 전체 조회
def find_hospital_slots(db: Session):
    return (
        db.query(HospitalSlot)
        .order_by(HospitalSlot.start_time)
        .all()
    )

# 전체 삭제 (init 위함)
def delete_all_slots(db: Session):
    db.query(HospitalSlot).delete()
    db.commit()

# init용 
def init_create_hospital_slots(db: Session, slots: list[dict]):
    objects = [HospitalSlot(**slot) for slot in slots]
    db.add_all(objects)
    db.commit()
    return objects

# 단일 생성
def create_hospital_slot(db: Session, request):
    slot = HospitalSlot(
        start_time=request.start_time,
        end_time=request.end_time,
        max_capacity=request.max_capacity
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot

# 단일 수정
def update_slot(db: Session, hospitalslot_id: int, max_capacity: int | None):
    slot = (
        db.query(HospitalSlot)
        .filter(HospitalSlot.hospitalslot_id == hospitalslot_id)
        .first()
    )

    if not slot:
        return None

    if max_capacity is not None:
        slot.max_capacity = max_capacity

    db.commit()
    db.refresh(slot)
    return slot

# 단일 삭제
def delete_hospital_slot(db: Session, hospitalslot_id: int):
    slot = (
        db.query(HospitalSlot)
        .filter(HospitalSlot.hospitalslot_id == hospitalslot_id)
        .first()
    )

    if not slot:
        return None

    db.delete(slot)
    db.commit()
    return slot
