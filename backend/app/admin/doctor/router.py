from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.database import get_db
from app.admin.doctor import schema, service


router = APIRouter(
    tags=["Doctor"]
)

'''
1. 의사 정보 crud
'''
# 의사 정보 조회
@router.get(
        "/doctor",
        response_model=list[schema.DoctorResponse],
        summary="의사 정보 조회"
        )
def get_doctors_list(
    department: str | None = None,
    db: Session = Depends(get_db)
):
    """
    옵션: 진료과로 필터링 가능
    """
    return service.get_doctors(db, department)
    
# 의사 정보 생성
@router.post(
        "/doctor",
        response_model=schema.DoctorResponse,
        summary="의사 정보 생성"
)
def create_doctor(
    request: schema.DoctorCreateRequest,
    db: Session = Depends(get_db)
):
    return service.creat_doctor(db, request)

# 의사 정보 수정
@router.patch(
        "/doctor/{doctor_id}",
        response_model=schema.DoctorResponse,
        summary="의사 정보 수정"
)
def update_doctor(
    doctor_id: int,
    request: schema.DoctorUpdateRequest,
    db: Session = Depends(get_db)
):
    return service.update_doctor(db, doctor_id, request.doctor_name, request.department)

# 의사 정보 삭제
@router.delete(
        "/doctor/{doctor_id}",
        response_model=schema.DoctorResponse,
        summary="의사 정보 삭제"
)
def delete_doctor(
    doctor_id: int,
    db: Session=Depends(get_db)
):
    return service.delete_doctor(db, doctor_id)
