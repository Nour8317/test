from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union
from typing import Literal

class InksandSolventsBase(BaseModel):
    material_name: Optional[str] = None
    material_type: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[float] = 0.0
    quantity: Optional[int] = 0
    supplier_name: Optional[str] = None
    color_code: Optional[str] = None
    cost: Optional[float] = 0.0
    received_at: Optional[datetime]

class InksandSolventsCreate(InksandSolventsBase):
    pass

class InksandSolventsOut(InksandSolventsBase):
    id: int

    class Config:
        from_attributes = True