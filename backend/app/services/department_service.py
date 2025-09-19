from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app.repositories.department_repository import DepartmentRepository
from app.schemas.department import DepartmentCreate, DepartmentOut

class DepartmentService:
    def __init__(self, db: Session):
        self.repo = DepartmentRepository(db)

    def create_department(self, data: DepartmentCreate) -> DepartmentOut:
        if self.repo.get_by_name(data.name):
            raise HTTPException(status_code=400, detail="Department already exists")
        department = self.repo.create(data.name, data.resource_names)
        return self._to_schema(department)

    def get_departments(self) -> List[DepartmentOut]:
        departments = self.repo.get_all()
        return [self._to_schema(dept) for dept in departments]

    def get_department(self, department_id: int) -> DepartmentOut:
        department = self.repo.get_by_id(department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        return self._to_schema(department)

    def update_department(self, department_id: int, data: DepartmentCreate) -> DepartmentOut:
        department = self.repo.get_by_id(department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        department = self.repo.update(department, data.name, data.resource_names)
        return self._to_schema(department)

    def delete_department(self, department_id: int):
        department = self.repo.get_by_id(department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        self.repo.delete(department)
        return {"detail": "Department deleted"}

    def _to_schema(self, dept) -> DepartmentOut:
        resource_names = [ra.resource_name for ra in dept.router_accesses]
        manager_names = [
            link.employee.name
            for link in dept.employees
            if link.employee.role == "manager"
        ]
        return DepartmentOut(
            id=dept.id,
            name=dept.name,
            resource_names=resource_names,
            no_of_managers=dept.no_of_managers or 0,
            manager_names=manager_names
        )
