from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.gsm import GsmCreate, GsmOut
from app.database import get_db
from app.auth.jwt_handler import get_current_admin
from app.repositories.gsm_repository import GsmRepository

router = APIRouter()



@router.post("/", response_model=GsmOut, dependencies=[Depends(get_current_admin)])
def create_gsm(gsm: GsmCreate, db: Session = Depends(get_db)):
    repo = GsmRepository(db)
    return repo.create(gsm.dict())

@router.get("/", response_model=List[GsmOut], dependencies=[Depends(get_current_admin)])
def read_gsms(db: Session = Depends(get_db)):
    repo = GsmRepository(db)
    return repo.get_all()

@router.get("/{gsm_id}", response_model=GsmOut, dependencies=[Depends(get_current_admin)])
def read_gsm(gsm_id: int, db: Session = Depends(get_db)):
    repo = GsmRepository(db)
    gsm = repo.get(gsm_id)
    if not gsm:
        raise HTTPException(status_code=404, detail="GSM not found")
    return gsm

@router.put("/{gsm_id}", response_model=GsmOut, dependencies=[Depends(get_current_admin)])
def update_gsm(gsm_id: int, gsm_update: GsmCreate, db: Session = Depends(get_db)):
    repo = GsmRepository(db)
    updated = repo.update(gsm_id, gsm_update.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="GSM not found")
    return updated

@router.delete("/{gsm_id}", dependencies=[Depends(get_current_admin)])
def delete_gsm(gsm_id: int, db: Session = Depends(get_db)):
    repo = GsmRepository(db)
    deleted = repo.delete(gsm_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="GSM not found")
    return {"detail": "GSM deleted"}