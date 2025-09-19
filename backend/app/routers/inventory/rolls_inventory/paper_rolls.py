from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.auth.jwt_handler import check_resource_permission, get_current_admin
from app.schemas import PaperRollOut, PaperRollCreate, RollPriceRequest
from app.services.paper_roll_service import PaperRollService

router = APIRouter()


@router.get("/", response_model=List[PaperRollOut], dependencies=[Depends(check_resource_permission("paper rolls"))])
def list_paper_rolls(db: Session = Depends(get_db)):
    return PaperRollService(db).list()


@router.get("/{paper_roll_id}", response_model=PaperRollOut, dependencies=[Depends(check_resource_permission("paper rolls"))])
def get_paper_roll(paper_roll_id: int, db: Session = Depends(get_db)):
    return PaperRollService(db).get(paper_roll_id)


@router.get("/by-raw-material/{raw_material_id}", response_model=List[PaperRollOut], dependencies=[Depends(check_resource_permission("paper rolls"))])
def get_paper_rolls_by_raw_material(raw_material_id: int, db: Session = Depends(get_db)):
    return PaperRollService(db).get_by_raw_material(raw_material_id)


@router.get("/groups", dependencies=[Depends(check_resource_permission("paper rolls"))])
def get_duplicate_paper_roll_groups(db: Session = Depends(get_db)):
    return PaperRollService(db).get_groups()


@router.put("/rolls/{roll_id}/price", dependencies=[Depends(get_current_admin)])
def price_paper_roll(roll_id: int, data: RollPriceRequest, db: Session = Depends(get_db)):
    return PaperRollService(db).price_roll(roll_id, data)


@router.put("/{serial_number}", dependencies=[Depends(check_resource_permission("paper rolls"))])
def use_paper_roll(serial_number: str, db: Session = Depends(get_db)):
    return PaperRollService(db).use_roll(serial_number)


@router.post("/", response_model=PaperRollOut, dependencies=[Depends(check_resource_permission("paper rolls"))])
def create_paper_roll(data: PaperRollCreate, db: Session = Depends(get_db), weight: Optional[float] = Form(None)):
    return PaperRollService(db).create(data, weight)


@router.put("/{paper_roll_id}", response_model=PaperRollOut, dependencies=[Depends(check_resource_permission("paper rolls"))])
def update_paper_roll(paper_roll_id: int, data: PaperRollCreate, db: Session = Depends(get_db)):
    return PaperRollService(db).update(paper_roll_id, data)


@router.put("/set-cost-currency/{barcode}", response_model=PaperRollOut, dependencies=[Depends(get_current_admin)])
def set_paper_roll_cost_currency_by_barcode(barcode: str, cost: float = Form(...), currency: str = Form(...), db: Session = Depends(get_db)):
    return PaperRollService(db).set_cost_currency(barcode, cost, currency)


@router.put("/update-weight/{roll_id}", response_model=PaperRollOut, dependencies=[Depends(check_resource_permission("paper rolls"))])
def update_paper_roll_weight(roll_id: int, weight: Optional[float] = Form(None), db: Session = Depends(get_db)):
    return PaperRollService(db).update_weight(roll_id, weight)


@router.delete("/{paper_roll_id}", dependencies=[Depends(get_current_admin)])
def delete_paper_roll(paper_roll_id: int, db: Session = Depends(get_db)):
    return PaperRollService(db).delete(paper_roll_id)
