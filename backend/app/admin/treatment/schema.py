from pydantic import BaseModel
from typing import Optional

class treatmentResponse(BaseModel):
    treatment_id: int
    treatment_name: str
    duration_minutes: int
    price: int
    description: Optional[str]

    class Config:
        from_attributes = True


class treatmentCreateRequest(BaseModel):
    treatment_name: str
    duration_minutes: int
    price: int
    description: Optional[str] = None


class treatmentUpdateRequest(BaseModel):
    treatment_name: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[int] = None
    description: Optional[str] = None
