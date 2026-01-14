from pydantic import BaseModel
from typing import Optional

# 의사 목록 응답
class DoctorResponse(BaseModel):
    doctor_id: int
    doctor_name: str
    department: str

# 의사 생성
class DoctorCreateRequest(BaseModel):
    doctor_name: str
    department: str

class DoctorUpdateRequest(BaseModel):
    doctor_name: Optional[str] = None
    department: Optional[str] = None