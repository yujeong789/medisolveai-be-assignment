from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.database import get_db
from app.admin.hospital_slot import schema, service


router = APIRouter(
    tags=["Hospital Slot"]
)

# hospital slot 조회
@router.get(
    "/hospital-slot",
    response_model=list[schema.hospitalSlotResponse],
    summary="hospital slot 조회"
)
def get_hospital_slot_list(
    db: Session = Depends(get_db)
):
    return service.get_hospital_slot_list(db)

# hospital slot 생성 (일괄생성)
@router.post(
    "/hospital-slot/init",
    response_model=list[schema.hospitalSlotResponse],
    summary="hospital slot 일괄 생성"
)
def init_hospital_slot(
    request: schema.hospitalSlotInitRequest, 
    db: Session = Depends(get_db)
):
    return service.init_hospital_slot(db, request)

#hospital slot 생성 (하나씩)
@router.post(
    "/hospital-slot",
    response_model=schema.hospitalSlotResponse,
    summary="hospital slot 하나씩 생성"
)
def create_hospital_slot(
    request: schema.hospitalSlotRequest, 
    db: Session = Depends(get_db)
):
    return service.create_hospital_slot(db, request)

# hospital slot 수정 (선택)
@router.patch(
    "/hospital-slot/{hospitalslot_id}",
    response_model=schema.hospitalSlotResponse,
    summary="hospital slot 수정"
)
def update_hospital_slot(
    hospitalslot_id: int,
    request: schema.hospitalSlotUpdateRequest,
    db: Session = Depends(get_db)
):
    return service.update_hospital_slot(db, hospitalslot_id, request)

# hospital slot 삭제 (선택)
@router.delete(
    "/hospital-slot/{hospitalslot_id}",
    response_model=schema.hospitalSlotResponse,
    summary="hospital slot 삭제"
)
def delete_hospital_slot(
    hospitalslot_id: int,
    db: Session = Depends(get_db)
):
    return service.delete_hospital_slot(db, hospitalslot_id)
