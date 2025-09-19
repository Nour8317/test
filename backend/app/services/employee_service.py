from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.employee import Employee
from app.models.department import Department
from app.models.employee_department import EmployeeDepartment
from app.repositories.employee_repository import EmployeeRepository
from app.auth.jwt_handler import get_password_hash, verify_password, create_access_token
from app.schemas.employee import EmployeeCreate, ManagerCreate
from app.schemas.auth import TokenResponse

class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = EmployeeRepository(db)

    def register_admin(self, data: EmployeeCreate) -> TokenResponse:
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        admin = self.repo.create({
            "name": data.name,
            "email": data.email,
            "password": get_password_hash(data.password),
            "role": "admin"
        })
        token = create_access_token({"sub": admin.id})
        return TokenResponse(access_token=token, token_type="bearer", employee=admin)

    def register_manager(self, data: ManagerCreate, current_admin: Employee) -> TokenResponse:
        if current_admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admins can register managers")

        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        manager = self.repo.create({
            "name": data.name,
            "email": data.email,
            "password": get_password_hash(data.password),
            "role": "manager"
        })

        for dept_id in data.department_ids:
            dept = self.db.query(Department).filter(Department.id == dept_id).first()
            if not dept:
                raise HTTPException(status_code=404, detail=f"Department {dept_id} not found")
            self.db.add(EmployeeDepartment(employee_id=manager.id, department_id=dept_id))
            dept.no_of_managers = (dept.no_of_managers or 0) + 1

        self.db.commit()
        self.db.refresh(manager)

        token = create_access_token({"sub": manager.id})
        return TokenResponse(access_token=token, token_type="bearer", employee=manager)

    def login(self, email: str, password: str) -> TokenResponse:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.id})
        return TokenResponse(access_token=token, token_type="bearer", employee=user)
    

    def login_form(self, username: str, password: str) -> dict:
        token_response = self.login(username, password)
        return {
            "access_token": token_response.access_token,
            "token_type": token_response.token_type
        }
    
    def get_all_employees(self, current_admin: Employee):
        if current_admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admins can get employees")
        return self.db.query(Employee).all()

