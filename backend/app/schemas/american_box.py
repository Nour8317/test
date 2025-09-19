from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.schemas.flut import FlutOut

class AmericanBoxBase(BaseModel):
    client_id: Optional[int] = None
    carton_length: float
    carton_width: float
    carton_height: float
    tounge_dimension: Optional[float] = None
    gsm : Optional[float] = None
    glue_type: Optional[str] = None
    design: Optional[str] = None
    form: Optional[str] = None
    polygon_type: Optional[str] = None
    polygon_category: Optional[str] = None
    notes: Optional[str] = None
    sheet_length: Optional[float] = None
    sheet_width: Optional[float] = None
    flap_dimension: Optional[float] = None
    piece_weight: Optional[float] = None
    total_weight: Optional[float] = None
    total_length: Optional[float] = None
    rolls_weight: Optional[float] = None
    waste_weight: Optional[float] = None
    cost: Optional[float] = None
    currency: Optional[str] = None

class FlutCreate(BaseModel):
    layer_number: int
    paper_type: str
    supplier: Optional[str] = None
    weight: Optional[float] = None
    
class AmericanBoxCreate(AmericanBoxBase):
    flutes: List[FlutCreate] = []

class AmericanBoxOut(AmericanBoxBase):
    id: int
    created_at: datetime
    updated_at: datetime
    flutes: List[FlutOut] = []

    class Config:
        orm_mode = True
