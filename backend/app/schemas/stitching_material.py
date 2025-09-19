from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union
from typing import Literal

class StitchingMaterialBase(BaseModel):
    material_name: Optional[str]= None
    material_type: Optional[str]= None
    weight: float= Field(..., ge=0)
    quantity: int= Field(..., ge=0)
    supplier_name: str
    cost: Optional[float] = Field(default=None, ge=0)

class StitchingMaterialCreate(StitchingMaterialBase):
    pass

class StitchingMaterialOut(StitchingMaterialBase):
    id: int

    class Config:
        from_attributes = True
