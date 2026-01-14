from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.common.database import get_db
from app.admin.statistics import schema, service
from datetime import datetime


router = APIRouter(
    tags=["Statistics"],
    prefix="/statistics"
)

# 상태별 예약 건수
@router.get(
    "/appointment/status",
    response_model=schema.statisticsAppointmentStatusResponse,
    summary="상태별 예약 건수"
)
def get_appointment_by_status(
    db: Session = Depends(get_db)
):
    return service.get_appointment_by_status(db)

# 일별/시간대별 예약 현황
@router.get(
    "/appointment/trend",
    response_model=schema.statisticsAppointmentResponse,
    summary="일별/시간대별 예약 현황"
)
def get_appointment_trend(
    trend_type: str = Query("day", enum=["day", "time"]),
    db: Session = Depends(get_db)
):
    return service.get_appointment_trend(db, trend_type)


# 초진/재진 비율
@router.get(
    "/visit",
    response_model=schema.statisticsVisitResponse,
    summary="초진/재진 비율"
)
def get_appointment_by_visit(
    db: Session = Depends(get_db)
):
    return service.get_appointment_by_visit(db)

