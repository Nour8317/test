from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.jwt_handler import get_current_admin, check_resource_permission
from app.schemas.chemicals import ChemicalsCreate, ChemicalsUpdate, ChemicalsOut
from app.repositories.chemicals_repository import ChemicalsRepository

router = APIRouter(prefix="/chemicals", tags=["chemicals"])

@router.post("/", response_model=ChemicalsOut, dependencies=[Depends(check_resource_permission("chemicals"))])
def create_chemical(chemical: ChemicalsCreate, db: Session = Depends(get_db)):
    repo = ChemicalsRepository(db)
    return repo.create(chemical)

@router.get("/", response_model=list[ChemicalsOut], dependencies=[Depends(check_resource_permission("chemicals"))])
def read_chemicals(db: Session = Depends(get_db)):
    repo = ChemicalsRepository(db)
    return repo.get_all()

@router.get("/{chemical_id}", response_model=ChemicalsOut, dependencies=[Depends(check_resource_permission("chemicals"))])
def read_chemical(chemical_id: int, db: Session = Depends(get_db)):
    repo = ChemicalsRepository(db)
    chemical = repo.get_by_id(chemical_id)
    if not chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    return chemical

@router.put("/{chemical_id}", response_model=ChemicalsOut, dependencies=[Depends(check_resource_permission("chemicals"))])
def update_chemical(chemical_id: int, updated_data: ChemicalsUpdate, db: Session = Depends(get_db)):
    repo = ChemicalsRepository(db)
    chemical = repo.update(chemical_id, updated_data)
    if not chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    return chemical

@router.delete("/{chemical_id}", dependencies=[Depends(get_current_admin)])
def delete_chemical(chemical_id: int, db: Session = Depends(get_db)):
    repo = ChemicalsRepository(db)
    chemical = repo.delete(chemical_id)
    if not chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    return {"detail": "Chemical deleted successfully"}
