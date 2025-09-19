from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.repositories.client_repository import ClientRepository
from app.models.client import ClientAccount
from app.schemas.client import ClientCreate

class ClientService:
    def __init__(self, db: Session):
        self.repo = ClientRepository(db)

    def create_client(self, data: ClientCreate):
        existing = self.repo.get_by_name(data.name)
        if existing:
            raise HTTPException(status_code=400, detail="Client with the same name already exists!")
        client = ClientAccount(
            name=data.name,
            email=data.email,
            contact=data.contact,
        )
        return self.repo.create(client)

    def get_all_clients(self):
        return self.repo.get_all()

    def get_client(self, client_id: int):
        client = self.repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    def get_client_with_orders(self, client_id: int):
        client = self.repo.get_with_orders(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    def update_client(self, client_id: int, data: ClientCreate):
        client = self.repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        client.name = data.name
        client.email = data.email
        client.contact = data.contact
        client.updated_at = datetime.now()

        return self.repo.update(client)

    def delete_client(self, client_id: int):
        client = self.repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        self.repo.delete(client)
        return client

    def get_summary(self):
        return self.repo.get_summary()
