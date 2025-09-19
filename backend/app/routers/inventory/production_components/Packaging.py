from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.auth.jwt_handler import get_current_admin, check_resource_permission
from app.database import get_db
from app.schemas.packaging import PackagingOut, PackagingCreate
from app.repositories.packaging_repository import PackagingRepository

router = APIRouter()


@router.post("/", response_model=PackagingOut, dependencies=[Depends(check_resource_permission("packaging"))])
def create_packaging(packaging: PackagingCreate, db: Session = Depends(get_db)):
    repo = PackagingRepository(db)
    return repo.add(packaging.dict())

@router.get("/", response_model=List[PackagingOut], dependencies=[Depends(check_resource_permission("packaging"))])
def read_packaging(db: Session = Depends(get_db)):
    repo = PackagingRepository(db)
    return repo.get_all()

@router.get("/{packaging_id}", response_model=PackagingOut, dependencies=[Depends(check_resource_permission("packaging"))])
def read_packaging_item(packaging_id: int, db: Session = Depends(get_db)):
    repo = PackagingRepository(db)
    item = repo.get(packaging_id)
    if not item:
        raise HTTPException(status_code=404, detail="Packaging item not found")
    return item

@router.put("/{packaging_id}", response_model=PackagingOut, dependencies=[Depends(check_resource_permission("packaging"))])
def update_packaging(packaging_id: int, updated_data: PackagingCreate, db: Session = Depends(get_db)):
    repo = PackagingRepository(db)
    updated = repo.update(packaging_id, updated_data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Packaging item not found")
    return updated

@router.delete("/{packaging_id}", dependencies=[Depends(get_current_admin)])
def delete_packaging(packaging_id: int, db: Session = Depends(get_db)):
    repo = PackagingRepository(db)
    deleted = repo.delete(packaging_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Packaging item not found")
    return {"detail": "Packaging item deleted successfully"}