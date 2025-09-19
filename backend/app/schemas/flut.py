from pydantic import BaseModel, Field, validator
from typing import Optional, List


class FlutBase(BaseModel):
    layer_number: int
    paper_type: str
    supplier: str
    weight: float= Field(ge=0)
    american_box_id: Optional[int] = None
    sheet_carton_id: Optional[int] = None
    roll_id: Optional[int] = None


class FlutCreate(FlutBase):
    @validator("american_box_id", "sheet_carton_id", "roll_id", pre=True, always=True)
    def zero_to_none(cls, v):
        return None if v == 0 else v


class FlutBatchCreate(BaseModel):
    fluts: List[FlutCreate]


class FlutOut(FlutBase):
    id: int

    class Config:
        orm_mode = True



