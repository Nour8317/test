from pydantic import BaseModel

class FlutAssociationCreate(BaseModel):
    item_type: str
    item_ids: list[int]
    layer_number: int
    paper_roll_serial: str  

