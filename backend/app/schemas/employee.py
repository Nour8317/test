from pydantic import BaseModel
from typing import List

class EmployeeCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class EmployeeOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class ManagerCreate(BaseModel):
    name: str
    email: str
    password: str
    department_ids: List[int]