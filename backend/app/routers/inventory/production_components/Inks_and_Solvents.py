from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.auth.jwt_handler import check_resource_permission, get_current_admin
from app.database import get_db
from app.schemas.ink_and_solvents import InksandSolventsOut, InksandSolventsCreate
from app.repositories.inks_and_solvents_repository import InksandSolventsRepository

router = APIRouter()



@router.post("/", response_model=InksandSolventsOut, dependencies=[Depends(check_resource_permission("inks_and_solvents"))])
def create_ink(data: InksandSolventsCreate, db: Session = Depends(get_db)):
    repo = InksandSolventsRepository(db)
    return repo.add(data.dict())

@router.get("/", response_model=List[InksandSolventsOut], dependencies=[Depends(check_resource_permission("inks_and_solvents"))])
def get_all_inks(db: Session = Depends(get_db)):
    repo = InksandSolventsRepository(db)
    return repo.get_all()

@router.get("/{ink_id}", response_model=InksandSolventsOut, dependencies=[Depends(check_resource_permission("inks_and_solvents"))])
def get_ink(ink_id: int, db: Session = Depends(get_db)):
    repo = InksandSolventsRepository(db)
    row = repo.get(ink_id)
    if not row:
        raise HTTPException(status_code=404, detail="Ink not found")
    return row

@router.put("/{ink_id}", response_model=InksandSolventsOut, dependencies=[Depends(check_resource_permission("inks_and_solvents"))])
def update_ink(ink_id: int, data: InksandSolventsCreate, db: Session = Depends(get_db)):
    repo = InksandSolventsRepository(db)
    updated = repo.update(ink_id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Ink not found")
    return updated

@router.delete("/{ink_id}", dependencies=[Depends(get_current_admin)])
def delete_ink(ink_id: int, db: Session = Depends(get_db)):
    repo = InksandSolventsRepository(db)
    deleted = repo.delete(ink_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ink not found")
    return {"detail": "Ink deleted"}