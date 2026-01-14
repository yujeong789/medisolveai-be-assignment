from pydantic import BaseModel
from typing import Optional
from datetime import time

class hospitalSlotResponse(BaseModel):
    hospitalslot_id: int
    start_time: time        
    end_time: time        
    max_capacity: int

class hospitalSlotInitRequest(BaseModel):
    start_time: time        
    end_time: time        
    interval_minutes: int = 30
    max_capacity: int

class hospitalSlotRequest(BaseModel):
    start_time: time        
    end_time: time        
    max_capacity: int

class hospitalSlotUpdateRequest(BaseModel):
    max_capacity: Optional[int] = None