from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth.jwt_handler import get_current_admin, get_current_user, get_admin_or_authorized_manager
from app.schemas.department import DepartmentCreate, DepartmentOut
from app.services.department_service import DepartmentService

router = APIRouter()

AVAILABLE_RESOURCES = [
   "raw materials", "paper rolls", "adhesive glue", "inks_and solvents",
   "chemicals", "packaging", "stitching material", "production component"
]

@router.post("/", response_model=DepartmentOut)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin),
):
    service = DepartmentService(db)
    return service.create_department(department)

@router.get("/", response_model=List[DepartmentOut])
def get_departments(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    service = DepartmentService(db)
    return service.get_departments()

@router.get("/{department_id}", response_model=DepartmentOut)
def get_department(department_id: int, db: Session = Depends(get_db), _: dict = Depends(get_admin_or_authorized_manager)):
    service = DepartmentService(db)
    return service.get_department(department_id)

@router.put("/{department_id}", response_model=DepartmentOut)
def update_department(department_id: int, updated: DepartmentCreate, db: Session = Depends(get_db), _: dict = Depends(get_admin_or_authorized_manager)):
    service = DepartmentService(db)
    return service.update_department(department_id, updated)

@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db), _: dict = Depends(get_current_admin)):
    service = DepartmentService(db)
    return service.delete_department(department_id)

@router.get("/available-resources", response_model=list[str])
def get_available_resources(_: dict = Depends(get_current_user)):
    return AVAILABLE_RESOURCES
