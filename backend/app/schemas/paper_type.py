from pydantic import BaseModel, Field, validator
from typing import Optional, List


class PaperType_Base(BaseModel):
    type: str
    
class PaperTypeCreate(PaperType_Base):
    pass
    

class PaperTypeOut(PaperType_Base):
    id: int

    class Config:
        orm_mode = True



