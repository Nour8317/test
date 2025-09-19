from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union
from typing import Literal



class PackagingBase(BaseModel):
    material_name: Optional[str]= None
    material_type: Optional[str]= None
    weight: float = Field(..., ge=0)
    dimensions: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    supplier_name: str
    cost: Optional[float]= Field(default=0.0, ge=0)

class PackagingCreate(PackagingBase):
    pass

class PackagingOut(PackagingBase):
    id: int
    cost: Optional[float] = None  # allows 0.0 in DB

    class Config:
        from_attributes = True
