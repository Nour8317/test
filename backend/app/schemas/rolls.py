from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from app.schemas.flut import FlutOut

class RollsBase(BaseModel):
    client_id: Optional[int] = None
    roll_width: Optional[float] = None
    form: Optional[str] = None
    notes: Optional[str] = None
    polygon_type: Optional[str] = None
    polygon_category: Optional[str] = None
    total_weight: Optional[float] = None
    waste_weight: Optional[float] = None
    design: Optional[str] = None
    gsm : Optional[float] = None
    cost: Optional[float] = None
    currency: Optional[str] = None

class RollsCreate(RollsBase):
    pass

class RollsOut(RollsBase):
    id: int
    created_at: datetime
    updated_at: datetime
    flutes: List[FlutOut] = []
    class Config:
        orm_mode = True

class FlutCreate(BaseModel):
    layer_number: int
    paper_type: str
    supplier: Optional[str] = None
    weight: Optional[float] = None


class RollWithFlutesCreate(BaseModel):
    client_id: int
    roll_width: float
    form: Optional[str] = None
    notes: Optional[str] = None
    polygon_type: Optional[str] = None
    polygon_category: Optional[str] = None
    cost: Optional[float] = None
    currency: Optional[str] = None
    flutes: List[FlutCreate] = [] 