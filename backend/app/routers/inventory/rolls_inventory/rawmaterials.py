from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.raw_materials_services import RawMaterialService
from app.schemas.raw_material import RawMaterialCreate, RawMaterialOut

router = APIRouter(prefix="/raw-materials", tags=["raw materials"])

@router.post("/", response_model=RawMaterialOut)
def create_raw_material(data: RawMaterialCreate, db: Session = Depends(get_db)):
    service = RawMaterialService(db)
    try:
        return service.create_raw_material(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[RawMaterialOut])
def get_raw_materials(db: Session = Depends(get_db)):
    service = RawMaterialService(db)
    return service.get_raw_materials()

@router.get("/{id}", response_model=RawMaterialOut)
def get_raw_material(id: int, db: Session = Depends(get_db)):
    service = RawMaterialService(db)
    raw = service.get_by_id(id)
    if not raw:
        raise HTTPException(status_code=404, detail="Not found")
    return raw

@router.delete("/{id}")
def delete_raw_material(id: int, db: Session = Depends(get_db)):
    service = RawMaterialService(db)
    if not service.delete_raw_material(id):
        raise HTTPException(status_code=404, detail="Not found")
    return {"detail": "Deleted successfully"}
