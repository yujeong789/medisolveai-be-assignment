from pydantic import BaseModel

class appointmentStatusCount(BaseModel):
    status: str
    count: int

class statisticsAppointmentStatusResponse(BaseModel):
    data: list[appointmentStatusCount]

class appointmentTrendItem(BaseModel):
    key: str   # "2026-01-13" or "10"
    count: int

class statisticsAppointmentResponse(BaseModel):
    type: str  # "day" | "time"
    data: list[appointmentTrendItem]

class visitRatioItem(BaseModel):
    is_first_visit: bool
    count: int

class statisticsVisitResponse(BaseModel):
    data: list[visitRatioItem]
