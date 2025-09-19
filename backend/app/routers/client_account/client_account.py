from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.client import ClientCreate, ClientOut, ClientWithOrdersResponse
from app.services.client_service import ClientService
from app.auth.jwt_handler import get_current_admin

router = APIRouter()

@router.post("/", response_model=ClientOut, dependencies=[Depends(get_current_admin)])
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return ClientService(db).create_client(client)

@router.get("/", response_model=List[ClientOut], dependencies=[Depends(get_current_admin)])
def get_all_clients(db: Session = Depends(get_db)):
    return ClientService(db).get_all_clients()

@router.get("/{client_id}", response_model=ClientOut, dependencies=[Depends(get_current_admin)])
def get_client(client_id: int, db: Session = Depends(get_db)):
    return ClientService(db).get_client(client_id)

@router.get("/client/{client_id}", response_model=ClientWithOrdersResponse, dependencies=[Depends(get_current_admin)])
def get_client_with_orders(client_id: int, db: Session = Depends(get_db)):
    return ClientService(db).get_client_with_orders(client_id)

@router.get("/clients/summary", dependencies=[Depends(get_current_admin)])
def get_clients_summary(db: Session = Depends(get_db)):
    return ClientService(db).get_summary()

@router.put("/{client_id}", response_model=ClientOut, dependencies=[Depends(get_current_admin)])
def update_client(client_id: int, update: ClientCreate, db: Session = Depends(get_db)):
    return ClientService(db).update_client(client_id, update)

@router.delete("/{client_id}", response_model=ClientOut, dependencies=[Depends(get_current_admin)])
def delete_client(client_id: int, db: Session = Depends(get_db)):
    return ClientService(db).delete_client(client_id)
