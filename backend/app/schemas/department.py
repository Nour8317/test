from pydantic import BaseModel, validator
from typing import List


AVAILABLE_RESOURCES = [
    "raw materials",
    "paper rolls",
    "adhesive glue",
    "inks_and solvents",
    "chemicals",
    "packaging",
    "stitching material",
    "production component",
]


class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    resource_names: List[str]

    @validator("resource_names", each_item=True)
    def validate_resource(cls, v):
        if v not in AVAILABLE_RESOURCES:
            raise ValueError(f"Invalid resource: {v}")
        return v

class DepartmentOut(BaseModel):
    id: int
    name: str
    resource_names: List[str] = []
    no_of_managers: int | None = 0
    manager_names: List[str] = []

    class Config:
        from_attributes = True
