from pydantic import BaseModel
from datetime import datetime

# 의사 목록 응답
class DoctorResponse(BaseModel):
    doctor_id: int
    doctor_name: str
    department: str

    class Config:
        from_attributes = True

# 예약 가능 시간 응답
class AvailableTimeResponse(BaseModel):
    start_time: datetime
    end_time: datetime

# 예약할 때, 요청값
class ReservationCreateRequest(BaseModel):
    patient_name: str
    phone: str
    doctor_id: int
    treatment_id: int
    start_time: datetime

# 예약할 때, 응답값
class ReservationResponse(BaseModel):
    reservation_code: str
    doctor_name: str
    treatment_name: str
    start_time: datetime
    end_time: datetime
    status: str

class MyReservationRequest(BaseModel):
    patient_name: str
    phone: str
