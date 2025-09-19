from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.employee import Employee
from app.models.employee_department import EmployeeDepartment

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.email == email).first()

    def get_managers(self) -> List[Employee]:
        return self.db.query(Employee).filter(Employee.role == "manager").all()

    def get_admins(self) -> List[Employee]:
        return self.db.query(Employee).filter(Employee.role == "admin").all()

    def get_employee_departments(self, employee_id: int) -> List[EmployeeDepartment]:
        return self.db.query(EmployeeDepartment).filter(EmployeeDepartment.employee_id == employee_id).all()

    def create(self, data: dict) -> Employee:
        emp = Employee(**data)
        self.db.add(emp)
        self.db.commit()
        self.db.refresh(emp)
        return emp

    def delete(self, employee: Employee):
        self.db.delete(employee)
        self.db.commit()
