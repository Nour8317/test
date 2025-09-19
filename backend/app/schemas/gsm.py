from pydantic import BaseModel, Field, validator
from typing import Optional, List


class Gsm_Base(BaseModel):
    value: float
    
class GsmCreate(Gsm_Base):
    pass
    

class GsmOut(Gsm_Base):
    id: int

    class Config:
        orm_mode = True



