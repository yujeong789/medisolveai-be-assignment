import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Time, Enum, Text, Index, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.common.database import Base

class AppointmentStatus(str, enum.Enum):
    PENDING = "예약대기"
    CONFIRMED = "확정"
    COMPLETED = "완료"
    CANCELLED = "취소"

# 의사 정보 : 병원에 근무하는 의사의 기본 정보
class Doctor(Base):
    __tablename__ = "doctors"
    doctor_id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_name = Column(String(20), nullable=False) # 이름
    department = Column(String(50), nullable=False) # 진료과
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

# 진료 항목 : 병원에서 제공하는 진료/시술 메뉴
class Treatment(Base):
    __tablename__="treatments"
    treatment_id = Column(Integer, primary_key=True, autoincrement=True)
    treatment_name = Column(String(255), nullable=False) # 시술명
    duration_minutes = Column(Integer, nullable=False) # 소요시간 (30분 단위)
    price = Column(Integer, nullable=False) # 가격
    description = Column(String(255)) # 설명

# 병원 시간대별 인원 설정 : 병원 전체의 시간대별 동시 수용 가능 인원. 모든 날짜에 동일하게 적용된다.
class HospitalSlot(Base):
    __tablename__ = "hospital_slots"
    hospitalslot_id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(Time, nullable=False) # 시간대_시작
    end_time = Column(Time, nullable=False) # 시간대_종료(30분 단위)
    max_capacity = Column(Integer, nullable=False) # 최대_인원수

    # 중복 예약 방지용 인덱스
    __table_args__ = (
        Index("idx_slot_time", "start_time", "end_time", unique=True),
    )

# 환자 정보 : 예약을 진행하는 환자의 기본 정보
class Patient(Base):
    __tablename__="patients"
    patient_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_name = Column(String(20), nullable=False) # 이름
    phone = Column(String(13), unique=True, nullable=False) # 연락처

    __table_args__ = (
        UniqueConstraint('patient_name', 'phone', name='_name_phone_uc'),
        )

# 예약 정보
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

# 병원 운영 시간
class OperatingHour(Base):
    __tablename__ = "operating_hours"
    operating_hour_id = Column(Integer, primary_key=True, autoincrement=True)
    day_of_week = Column(Integer, nullable=False) # 요일(0월 1화 2수 3목 4금 5토 6일)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    break_start_time = Column(Time)
    break_end_time = Column(Time)
    is_opened = Column(Boolean, default=True)

    __table_args__ = (
        Index("idx_day_of_week", "day_of_week", unique=True),
    )


# revision 생성 
# docker-compose run --rm gateway uv run alembic revision --autogenerate -m "create clinic tables"

# DB에 반영
# docker-compose run --rm gateway uv run alembic upgrade head
