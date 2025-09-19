from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.american_box import AmericanBoxOut
from app.schemas.sheet_carton import SheetCartonOut
from app.schemas.rolls import RollsOut
class ClientBase(BaseModel):
    name: str
    email: str
    contact: str

class ClientCreate(ClientBase):
    pass


class ClientWithOrdersResponse(BaseModel):
    id: int
    name: str
    email: str
    contact: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    american_boxes: List[AmericanBoxOut] = []
    sheet_cartons: List[SheetCartonOut] = []
    rolls: List[RollsOut] = []

class ClientOut(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
