from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.paper_type import PaperTypeCreate, PaperTypeOut
from app.database import get_db
from app.auth.jwt_handler import get_current_admin
from app.repositories.paper_type_repository import PaperTypeRepository

router = APIRouter()


@router.post("/", response_model=PaperTypeOut, dependencies=[Depends(get_current_admin)])
def create_paper_type(paper_type: PaperTypeCreate, db: Session = Depends(get_db)):
    repo = PaperTypeRepository(db) 
    return repo.create(paper_type.dict())

@router.get("/", response_model=List[PaperTypeOut], dependencies=[Depends(get_current_admin)])
def read_paper_types(db: Session = Depends(get_db)):
    repo = PaperTypeRepository(db) 
    return repo.get_all()

@router.get("/{paper_type_id}", response_model=PaperTypeOut, dependencies=[Depends(get_current_admin)])
def read_paper_type(paper_type_id: int, db: Session = Depends(get_db)):
    repo = PaperTypeRepository(db)
    paper_type = repo.get(paper_type_id)
    if not paper_type:
        raise HTTPException(status_code=404, detail="Paper type not found")
    return paper_type

@router.put("/{paper_type_id}", response_model=PaperTypeOut, dependencies=[Depends(get_current_admin)])
def update_paper_type(paper_type_id: int, paper_type_update: PaperTypeCreate, db: Session = Depends(get_db)):
    repo = PaperTypeRepository(db)
    updated = repo.update(paper_type_id, paper_type_update.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Paper type not found")
    return updated

@router.delete("/{paper_type_id}", dependencies=[Depends(get_current_admin)])
def delete_paper_type(paper_type_id: int, db: Session = Depends(get_db)):
    repo = PaperTypeRepository(db)
    deleted = repo.delete(paper_type_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Paper type not found")
    return {"detail": "Paper type deleted"}