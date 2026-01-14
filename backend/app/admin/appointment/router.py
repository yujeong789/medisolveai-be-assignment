from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.database import get_db
from app.admin.appointment import schema, service
from datetime import datetime

router = APIRouter(
    tags=["Appointment"]
)

# 전체 예약 조회
@router.get(
    "/appointment",
    response_model=list[schema.appointmentResponse],
    summary="예약 조회"
)
def get_appointment_list(
    created_at: datetime | None = None,
    start_time: datetime | None = None,
    doctor_id: int | None = None,
    treatment_id: int | None = None,
    status: str | None = None,
    is_first_visit: bool | None = None,
    db: Session = Depends(get_db)
):
    return service.get_appointment_list(
        db,
        created_at,
        start_time,
        doctor_id,
        treatment_id,
        status,
        is_first_visit
    )


# 예약 상태 수정
@router.patch(
    "/appointment/{appointment_id}",
    response_model=schema.appointmentResponse,
    summary="예약 상태 수정"
)
def update_apponintment(
    appointment_id: int,
    request: schema.appointmentUpdateRequest,
    db: Session = Depends(get_db)
):
    return service.update_appointment(db, appointment_id, request)


'''
class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_code = Column(String(6), unique=True, index=True)

    patient_id = Column(String(36), ForeignKey("patients.patient_id"), nullable=False) # 환자
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"), nullable=False)
    treatment_id = Column(Integer, ForeignKey("treatments.treatment_id"), nullable=False)

    start_time = Column(DateTime, nullable=False) # 예약_시작일시
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING) # 예약대기
    is_first_visit = Column(Boolean, default=True) # 초진/재진 구분
    memo = Column(Text) # 메모
    created_at = Column(DateTime, default=datetime.utcnow)

    # 중복 예약 방지용 인덱스
    __table_args__ = (
        Index("idx_doctor_time", "doctor_id", "start_time"),
    )
    # FK 설정
    patient = relationship("Patient", lazy="joined")
    doctor = relationship("Doctor", lazy="joined")
    treatment = relationship("Treatment", lazy="joined")    
'''