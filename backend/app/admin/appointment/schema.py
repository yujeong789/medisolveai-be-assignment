from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class appointmentResponse(BaseModel):
    appointment_id: int
    reservation_code: str
    patient_id: str
    doctor_id: int
    treatment_id: int
    start_time: datetime
    end_time: datetime
    status: str
    is_first_visit: bool
    memo: Optional[str] = None
    created_at: datetime

class appointmentUpdateRequest(BaseModel):
    status: Optional[str] = None
    memo: Optional[str] = None

