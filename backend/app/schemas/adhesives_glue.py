from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union
from typing import Literal


class AdhesivesGlueBase(BaseModel):
    material_name: Optional[str]= None
    material_type: Optional[str]= None
    weight: float  = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    supplier_name: str
    cost: Optional[float] = Field(default=0.0, ge=0)

class AdhesivesGlueCreate(AdhesivesGlueBase):
    pass

class AdhesivesGlueOut(AdhesivesGlueBase):
    id: int

    class Config:
        from_attributes = True
