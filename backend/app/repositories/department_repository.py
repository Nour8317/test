from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.department import Department
from app.models.router_access import RouterAccess
from app.repositories.base import BaseRepository

class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, db: Session):
        super().__init__(Department, db)


    def get_by_id(self, id: int) -> Optional[Department]:
        return self.db.query(Department).filter(Department.id == id).first()

    def create_with_resources(self, name: str, resources: List[str]) -> Department:
        department = super().create({"name": name})
        for resource in resources:
            access = RouterAccess(department_id=department.id, resource_name=resource)
            self.db.add(access)
        self.db.commit()
        self.db.refresh(department)
        return department

    def update_with_resources(self, department: Department, name: str, resources: List[str]) -> Department:
        department = super().update(department, {"name": name})
        self.db.query(RouterAccess).filter(RouterAccess.department_id == department.id).delete()
        for resource in resources:
            self.db.add(RouterAccess(department_id=department.id, resource_name=resource))
        self.db.commit()
        self.db.refresh(department)
        return department
