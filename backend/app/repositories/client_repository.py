from sqlalchemy.orm import Session, joinedload
from app.models.client import ClientAccount
from app.models.american_box import AmericanBox
from app.models.sheet_carton import SheetCarton
from app.models.rolls import Rolls
from typing import Optional

class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, client_id: int) -> Optional[ClientAccount]:
        return self.db.query(ClientAccount).filter(ClientAccount.id == client_id).first()

    def get_by_name(self, name: str) -> Optional[ClientAccount]:
        return self.db.query(ClientAccount).filter(ClientAccount.name == name).first()

    def get_all(self):
        return self.db.query(ClientAccount).all()

    def get_with_orders(self, client_id: int):
        return self.db.query(ClientAccount).options(
            joinedload(ClientAccount.american_boxes).joinedload(AmericanBox.flutes),
            joinedload(ClientAccount.sheet_cartons).joinedload(SheetCarton.flutes),
            joinedload(ClientAccount.rolls).joinedload(Rolls.flutes),
        ).filter(ClientAccount.id == client_id).first()

    def create(self, client: ClientAccount):
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def update(self, client: ClientAccount):
        self.db.commit()
        self.db.refresh(client)
        return client

    def delete(self, client: ClientAccount):
        self.db.delete(client)
        self.db.commit()

    def get_summary(self):
        total_clients = self.db.query(ClientAccount).count()
        total_american_boxes = self.db.query(AmericanBox).count()
        total_sheet_cartons = self.db.query(SheetCarton).count()
        total_rolls = self.db.query(Rolls).count()
        return {
            "total_clients": total_clients,
            "total_orders": total_american_boxes + total_sheet_cartons + total_rolls,
            "breakdown": {
                "american_boxes": total_american_boxes,
                "sheet_cartons": total_sheet_cartons,
                "rolls": total_rolls,
            },
        }
