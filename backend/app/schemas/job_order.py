from pydantic import BaseModel
from typing import List, Literal, Optional

class JobOrderItemCreate(BaseModel):
    item_type: Literal["american_box", "rolls", "sheet_carton"]
    item_id: int
    number_of_outs: int
    quantity: int


class JobOrderCreate(BaseModel):
    client_ids: List[int]                 
    order_type: Literal["single", "double"]
    itemId_for_quantity: int
    items: List[JobOrderItemCreate]


class JobOrderItemOut(BaseModel):
    id: int
    job_order_id: int
    item_type: str
    item_id: int
    sheet_length: Optional[float]
    sheet_width: Optional[float]
    quantity: Optional[int]  
    number_of_outs: Optional[int]

    class Config:
        from_attributes = True  


class JobOrderOut(BaseModel):
    id: int
    order_type: str
    working_width: float
    meter_length: float
    items: List[JobOrderItemOut] 
    clients: List[int]  

    class Config:
        from_attributes = True


class JobOrderResponse(BaseModel):
    id: int
    order_type: str
    working_width: float
    meter_length: Optional[float]  
    calculated_weight: float
    items: List[JobOrderItemOut]
    clients: List[int]

    class Config:
        from_attributes = True


class FlutWeight(BaseModel):
    weight: float

class RollJobOrderCreate(BaseModel):
    client_ids: List[int]
    roll_id: int
    meter_length: float