from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.auth.jwt_handler import get_current_admin  
from app.schemas.sheet_carton import SheetCartonCreate, SheetCartonOut
from app.repositories.sheet_carton_repository import SheetCartonRepository
from app.services.sheet_carton_service import SheetCartonService
from app.schemas.client import ClientOut

router = APIRouter()

def get_service(db: Session = Depends(get_db)):
    repo = SheetCartonRepository(db)
    service = SheetCartonService(repo)
    return service

@router.post("/", response_model=SheetCartonOut)
async def create_sheet_carton(carton: SheetCartonCreate, service: SheetCartonService = Depends(get_service), current_admin=Depends(get_current_admin)):
    return service.create_sheet_carton(carton)

@router.get("/", response_model=List[SheetCartonOut])
def get_all_sheet_cartons(service: SheetCartonService = Depends(get_service), current_admin=Depends(get_current_admin)):
    return service.get_all_sheet_cartons()

@router.get("/clients", response_model=List[ClientOut])
def get_clients(service: SheetCartonService = Depends(get_service), current_admin=Depends(get_current_admin)):
    return service.get_clients()

@router.get("/{sheet_id}", response_model=SheetCartonOut)
def get_sheet_carton(sheet_id: int, service: SheetCartonService = Depends(get_service), current_admin=Depends(get_current_admin)):
    return service.get_sheet_carton(sheet_id)

@router.get("/by_client/{client_id}", response_model=List[SheetCartonOut])
def get_sheet_cartons_by_client(client_id: int, service: SheetCartonService = Depends(get_service), current_admin=Depends(get_current_admin)):
    return service.get_by_client(client_id)

@router.put("/{sheet_id}")
def update_waste(sheet_id: int, waste: float, service: SheetCartonService = Depends(get_service), current_admin=Depends(get_current_admin)):
    return service.update_waste(sheet_id, waste)

@router.delete("/{sheet_id}")
def delete_sheet_carton(sheet_id: int, service: SheetCartonService = Depends(get_service), current_admin=Depends(get_current_admin)):
    service.delete_sheet_carton(sheet_id)
    return {"detail": "Deleted successfully"}

@router.put("/update/{sheet_id}")
async def update_sheet_carton(
    sheet_id: int,
    client_id: int = Form(...),
    polygon_type: Optional[str] = Form(None),
    polygon_category: Optional[str] = Form(None),
    form: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    cost: Optional[float] = Form(None),
    currency: Optional[float] = Form(None),
    sheet_length: Optional[float] = Form(None),
    sheet_width: Optional[float] = Form(None),
    design: Optional[UploadFile] = File(None),
    service: SheetCartonService = Depends(get_service),
    current_admin=Depends(get_current_admin)
):
    return service.update_sheet_carton(
        sheet_id, client_id, polygon_type, polygon_category, form, notes, cost, currency, sheet_length, sheet_width, design
    )
