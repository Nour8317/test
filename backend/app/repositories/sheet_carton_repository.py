from sqlalchemy.orm import Session
from app.models.sheet_carton import SheetCarton
from app.models.flut import Flut
from typing import List

from app.schemas.client import ClientOut
from app.models.client import ClientAccount

class SheetCartonRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, sheet_carton_data: dict) -> SheetCarton:
        sheet_carton = SheetCarton(**sheet_carton_data)
        self.db.add(sheet_carton)
        self.db.commit()
        self.db.refresh(sheet_carton)
        return sheet_carton

    def add_flutes(self, sheet_carton_id: int, flutes_data: List[dict]):
        for f in flutes_data:
            self.db.add(Flut(**f, sheet_carton_id=sheet_carton_id))
        self.db.commit()

    def get_all(self) -> List[SheetCarton]:
        return self.db.query(SheetCarton).all()

    def get_clients(self) -> List[ClientOut]:
        return (
            self.db.query(ClientAccount)
            .join(SheetCarton, ClientAccount.id == SheetCarton.client_id)
            .distinct()
            .all()
        )

    def get_by_id(self, sheet_id: int) -> SheetCarton | None:
        return self.db.query(SheetCarton).filter(SheetCarton.id == sheet_id).first()
    
    def get_by_client(self, client_id: int) -> List[SheetCarton]:
        return self.db.query(SheetCarton).filter(SheetCarton.client_id == client_id).all()

    def update(self, sheet: SheetCarton):
        self.db.commit()
        self.db.refresh(sheet)
        return sheet

    def delete(self, sheet: SheetCarton):
        self.db.delete(sheet)
        self.db.commit()
