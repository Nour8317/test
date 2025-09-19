from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TapeBase(BaseModel):
    item: Optional[str]
    size_raw: Optional[str]
    width: Optional[float]
    thickness: Optional[str]
    length: Optional[float]
    gross_weight: Optional[float]
    roll_number: Optional[str]
    made_in: Optional[str]

class TapeCreate(TapeBase):
    pass

class TapeUpdate(TapeBase):
    pass

class TapeResponse(TapeBase):
    id: int

    class Config:
        orm_mode = True
