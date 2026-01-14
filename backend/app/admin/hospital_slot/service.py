import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.admin.hospital_slot import repository
from datetime import datetime, date, timedelta

# 전체 목록 조회
def get_hospital_slot_list(db: Session):
    return repository.find_hospital_slots(db)

# 전체 시간표 생성
def init_hospital_slot(db: Session, request):
    '''
    start_time: time        
    end_time: time        
    interval_minutes: int = 30
    max_capacity: int
    '''
    # 기존 슬롯 삭제
    repository.delete_all_slots(db)

    # 시간 분할
    start_dt = datetime.combine(date.today(), request.start_time)
    end_dt = datetime.combine(date.today(), request.end_time)

    if start_dt >= end_dt:
        raise HTTPException(400, "시작 시간은 종료 시간보다 빨라야 합니다.")
    
    slots = []

    current = start_dt
    while(current < end_dt):
        next_time = current + timedelta(minutes=request.interval_minutes)
        if next_time > end_dt:
            break
            
        slots.append({
            "start_time": current.time(),
            "end_time": next_time.time(),
            "max_capacity": request.max_capacity
        })

        current = next_time
    if not slots:
        raise HTTPException(400, "생성할 시간표가 없습니다.")
    
    return repository.init_create_hospital_slots(db, slots)

# 단일 시간표 생성
def create_hospital_slot(db: Session, request):
    return repository.create_hospital_slot(db, request)

# 단일 시간표 수정
def update_hospital_slot(db: Session, hospitalslot_id: int, request):
    slot = repository.update_slot(db, hospitalslot_id, request.max_capacity)
    if not slot:
        raise HTTPException(404, "시간표가 존재하지 않습니다.")
    return slot

# 단일 시간표 삭제
def delete_hospital_slot(db: Session, hospital_id: int):
    slot = repository.delete_hospital_slot(db, hospital_id)
    if not slot:
        raise HTTPException(404, "시간표가 존재하지 않습니다.")
    return slot

