from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.database import get_db
from app.admin.treatment import schema, service

router = APIRouter(
    tags=["Treatment"]
)

# 진료 항목 조회
@router.get(
    "/treatment",
    response_model=list[schema.treatmentResponse],
    summary="진료 항목 조회"
)
def get_treatment_list(
    db: Session = Depends(get_db)
):
    return service.get_treatment_list(db)

# 진료 항목 생성
@router.post(
    "/treatment",
    response_model=schema.treatmentResponse,
    summary="진료 항목 생성"
)
def create_treatment(
    request: schema.treatmentCreateRequest,
    db: Session = Depends(get_db)
):
    return service.create_treatment(db, request)

# 진료 항목 수정
@router.patch(
    "/treatment/{treatment_id}",
    response_model=schema.treatmentResponse,
    summary="진료 항목 수정"
)
def update_treatment(
    treatment_id: int,
    request: schema.treatmentUpdateRequest,
    db: Session = Depends(get_db)
):
    return service.update_treatment(db, treatment_id, request)

# 진료 항목 삭제
@router.delete(
    "/treatment/{treatment_id}",
    response_model=schema.treatmentResponse,
    summary="진료 항목 삭제"
)
def delete_treatment(
    treatment_id: int,
    db: Session=Depends(get_db)
):
    return service.delete_treatment(db, treatment_id)


