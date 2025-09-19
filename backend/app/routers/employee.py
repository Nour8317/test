from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.jwt_handler import get_current_admin
from app.services.employee_service import EmployeeService
from app.schemas.employee import EmployeeCreate, ManagerCreate, EmployeeOut
from app.schemas.auth import LoginRequest, TokenResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.get("/get-all-employees")
def get_all(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return EmployeeService(db).get_all_employees(current_admin)


@router.post("/register-admin", response_model=TokenResponse)
def register_admin(data: EmployeeCreate, db: Session = Depends(get_db)):
    return EmployeeService(db).register_admin(data)


@router.post("/register-manager", response_model=TokenResponse)
def register_manager(
    data: ManagerCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return EmployeeService(db).register_manager(data, current_admin)

@router.put("/update-manager/{manager_id}", response_model=EmployeeOut)
def update_manager(manager_id: int, data: ManagerCreate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return EmployeeService(db).update_manager(manager_id, data, current_admin)


@router.post("/login/swagger")
def login_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return EmployeeService(db).login_form(form_data.username, form_data.password)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return EmployeeService(db).login(data.email, data.password)


@router.delete("/delete/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return EmployeeService(db).delete_employee(employee_id, current_admin)
