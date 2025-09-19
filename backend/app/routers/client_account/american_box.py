from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.american_box import AmericanBoxCreate, AmericanBoxOut
from app.services.american_box_service import AmericanBoxService
from app.auth.jwt_handler import get_current_admin
from app.schemas.client import ClientOut  

router = APIRouter(prefix="/american_box", tags=["american box"])

@router.post("/", response_model=AmericanBoxOut)
async def create_box(box: AmericanBoxCreate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return AmericanBoxService(db).create_box(box)

@router.get("/", response_model=List[AmericanBoxOut])
def get_all_boxes(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return AmericanBoxService(db).repo.get_all()

@router.get("/clients", response_model=List[ClientOut])
def get_clients(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return AmericanBoxService(db).get_clients()

@router.get("/by_client/{client_id}", response_model=List[AmericanBoxOut])
def get_boxes_by_client(client_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return AmericanBoxService(db).get_boxes_by_client(client_id)

@router.get("/{box_id}", response_model=AmericanBoxOut)
def get_box(box_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return AmericanBoxService(db).get_box(box_id)

@router.put("/{box_id}/waste", response_model=AmericanBoxOut)
def update_waste(box_id: int, waste: float, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return AmericanBoxService(db).update_waste(box_id, waste)

@router.put("/{box_id}", response_model=AmericanBoxOut)
async def update_box(
    box_id: int,
    client_id: int = Form(...),
    carton_length: float = Form(...),
    carton_width: float = Form(...),
    carton_height: float = Form(...),
    tounge_dimension: float = Form(...),
    glue_type: Optional[str] = Form(None),
    form: Optional[str] = Form(None),
    polygon_type: Optional[str] = Form(None),
    polygon_category: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    design: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return AmericanBoxService(db).update_box(
        box_id=box_id,
        client_id=client_id,
        carton_length=carton_length,
        carton_width=carton_width,
        carton_height=carton_height,
        tounge_dimension=tounge_dimension,
        glue_type=glue_type,
        form=form,
        polygon_type=polygon_type,
        polygon_category=polygon_category,
        notes=notes,
        design=design
    )

@router.delete("/{box_id}")
def delete_box(box_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return AmericanBoxService(db).delete_box(box_id)
