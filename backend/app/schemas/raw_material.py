from pydantic import BaseModel, Field
from typing import Optional, Union, List
from datetime import datetime
from typing import Literal

class RawMaterialBase(BaseModel):
    category: str
    supplier_name: str
    degree: str
    quantity: int = Field(..., ge=0)
    paper_type: str
    roll_width: float = Field(..., ge=0)
    gsm: float = Field(..., ge=0)
    job_order_id: int
    status: Optional[str] = ["not priced", "priced"]

class RawMaterialCreate(RawMaterialBase):
    category: Literal["Imported", "Local"]
    weights: Optional[List[float]] = None   

class RawMaterialOut(RawMaterialBase):
    id: int
    received_at: datetime
    serial_number: Optional[str] = None

    class Config:
        from_attributes = True

class RawMaterialGeneralSummary(BaseModel):
    paper_type: str
    roll_width: float
    category: str
    degree: str
    gsm: float
    quantity: int

class Combination(BaseModel):
    gsm: Union[str, float, int]
    degree: str
    category: str
    quantity: float

class FilterSummaryOut(BaseModel):
    group_value: Union[str, float, int]
    combinations: List[Combination]
