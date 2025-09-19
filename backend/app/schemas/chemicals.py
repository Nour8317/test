from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union
from typing import Literal

class ChemicalsBase(BaseModel):
    material_name: Optional[str]= None
    material_type: Optional[str]= None
    weight: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    supplier_name: str
    cost: Optional[float] = Field(default=None, ge=0)

class ChemicalsCreate(ChemicalsBase):
    pass

class ChemicalsOut(ChemicalsBase):
    id: int

    class Config:
        from_attributes = True

class ChemicalsUpdate(BaseModel):
    material_name: Optional[str] = None
    material_type: Optional[str] = None
    weight: Optional[float] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)
    supplier_name: Optional[str] = None
    cost: Optional[float] = Field(default=None, ge=0)

    class Config:
        from_attributes = True