from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union
from typing import Literal



class ProductionComponentBase(BaseModel):
    component: str
    material_name: Optional[str]= None
    material_type: str
    color: Optional[str]= None
    weight: float= Field(..., ge=0)
    quantity: int= Field(..., ge=0)
    color_code: Optional[str]= None
    dimensions: Optional[float] = Field(default=None, ge=0)

class ProductionComponentCreate(ProductionComponentBase):
    pass

class ProductionComponentOut(ProductionComponentBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True

class DeductRequest(BaseModel):
    material_id: int = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class DeductByComponentRequest(BaseModel):
    component: str
    material_name: str
    material_type: str
    quantity_to_deduct: int
    weight_to_deduct: float
    color: Optional[str] = None
    color_code: Optional[str] = None
    dimensions: Optional[float] = None