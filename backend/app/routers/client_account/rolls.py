from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.jwt_handler import get_current_admin
from app.services.rolls_service import RollsService
from app.schemas.rolls import RollWithFlutesCreate, RollsOut
from app.schemas.client import ClientOut

router = APIRouter(prefix="/rolls", tags=["rolls"])

@router.post("/", response_model=RollsOut)
async def create_roll_with_flutes(
    roll_data: RollWithFlutesCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    service = RollsService(db)
    return service.create_with_flutes(roll_data)

@router.get("/", response_model=list[RollsOut])
def get_all_rolls(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    service = RollsService(db)
    return service.get_all()

@router.get("/clients", response_model=list[ClientOut])
def get_clients(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    service = RollsService(db)
    return service.get_clients() 

@router.get("/{id}", response_model=RollsOut)
def get_roll(id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    service = RollsService(db)
    return service.get_by_id(id)


@router.get("/by_client/{client_id}", response_model=list[RollsOut])
def get_rolls_by_client(client_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    service = RollsService(db)
    return service.get_by_client_id(client_id)

@router.delete("/{id}")
def delete_roll(id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    service = RollsService(db)
    return service.delete(id)

@router.put("/{roll_id}/waste", response_model=RollsOut)
def update_waste(roll_id: int, waste: float, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    service = RollsService(db)
    return service.update_waste(roll_id, waste)
