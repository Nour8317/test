from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from app.schemas.flut import FlutOut

class SheetCartonBase(BaseModel):
    client_id: Optional[int] = None
    polygon_type: Optional[str] = None
    polygon_category: Optional[str] = None
    form: Optional[str] = None
    design: Optional[str] = None
    notes: Optional[str] = None
    sheet_length: Optional[float] = None
    sheet_width: Optional[float] = None
    total_weight: Optional[float] = None
    rolls_weight: Optional[float] = None
    waste_weight: Optional[float] = None
    cost: Optional[float] = None
    gsm : Optional[float] = None
    currency: Optional[str] = None

class FlutCreate(BaseModel):
    layer_number: int
    paper_type: str
    supplier: Optional[str] = None
    weight: Optional[float] = None

class SheetCartonCreate(SheetCartonBase):
    flutes: List[FlutCreate] = []

class SheetCartonOut(SheetCartonBase):
    id: int
    flutes: List[FlutOut] = []

    


    
