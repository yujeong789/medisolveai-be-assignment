from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.database import get_db
from datetime import date
from app.patient import schema, service
from app.patient.service import (
    get_available_reservations,
    create_reservation,
    read_my_reservation,
    cancel_reservation
)

router = APIRouter(
    tags=["Patient"]
)

# 의사 목록 조회
@router.get(
        "/doctors", 
        response_model=list[schema.DoctorResponse],
        summary="의사 목록 조회",
        description="병원의 전체 의사 목록을 조회합니다."
        )
def get_doctors(
    department: str | None = None,
    db: Session = Depends(get_db)
):
    """
    옵션: 진료과로 필터링 가능
    """
    return service.get_doctors(department, db)


# 예약 가능 시간 조회
@router.get(
        "/reservation/available", 
        response_model=list[schema.AvailableTimeResponse],
        summary="예약 가능 시간 조회",
        description="특정 의사의 예약 가능한 시간대를 조회합니다.")
def get_available_reservations(
    date: date,
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """
    요구사항:
    - 병원 운영 시간 내의 예약 가능 시간대만 노출
    - 선택한 날짜 기준으로 15분 간격 시간대 제공
    - 이미 예약된 시간, 병원 수용 인원 초과 시간은 제외
    """
    return service.get_available_reservations(date, doctor_id, db)


# 예약 생성
@router.post(
        "/reservation", 
        response_model=schema.ReservationResponse,
        summary="예약 생성",
        description="새로운 예약을 생성합니다.")
def create_reservation(
    request: schema.ReservationCreateRequest,
    db: Session = Depends(get_db)
):
    """
    요구사항:
    - 중복 예약 방지 로직 구현 (동일 의사에게 동일 시간대 중복 불가)
    - 병원 시간대별 최대 인원수 제한 검증
    - 초진/재진 자동 판단 및 저장

    시간대 검증 규칙:
    - 예약 시작 시간부터 종료 시간까지 걸치는 모든 30분 슬롯을 확인
    - 모든 해당 슬롯에 수용 인원 여유가 있어야 예약 가능
    - 예시: 10:15~10:45 예약(30분)은 10:00~10:30, 10:30~11:00 슬롯 모두 확인 필요
    """
    return service.create_reservation(request, db)


# 내 예약 조회
@router.post(
        "/my", 
        response_model=list[schema.ReservationResponse],
        summary="내 예약 조회",
        description="환자 본인의 예약 목록을 조회합니다.")
def read_reservation(
    request: schema.MyReservationRequest,
    db: Session = Depends(get_db)
):
    """
    요구사항: 본인의 예약만 조회 가능
    """
    return service.read_my_reservation(request, db)


# 내 예약 취소
@router.delete(
        "/reservation/{reservation_code}", 
        response_model=schema.ReservationResponse,
        summary="내 예약 취소",
        description="예약을 취소 상태로 변경합니다."
        )
def cancel_reservation(
    reservation_code: str, 
    db: Session = Depends(get_db)
):
    return service.cancel_reservation(reservation_code, db)
