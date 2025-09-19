from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union
from typing import Literal

class PaperRollBase(BaseModel):
    raw_id: int
    roll_id: int
    paper_type: str
    gsm: float = Field(..., ge=0)
    roll_width: float = Field(..., ge=0)
    job_order_id: Optional[int] = None
    serial_number: str
    status: Optional[str] = "available"
    weight: Optional[float] = None
    cost: Optional[float] = None   
    currency: Optional[str] = None 
    
class RollPriceRequest(BaseModel):
    cost: float
    currency: str



class PaperRollCreate(PaperRollBase):
    pass

class PaperRollOut(PaperRollBase):
    id: int

    class Config:
        orm_mode = True
