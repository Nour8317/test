from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.american_box import AmericanBox
from app.models.flut import Flut
from app.repositories.base import BaseRepository
from app.models.client import ClientAccount
from app.schemas.client import ClientOut

class AmericanBoxRepository(BaseRepository[AmericanBox]):
    def __init__(self, db: Session):
        super().__init__(AmericanBox, db)

    def add_flutes(self, box_id: int, flutes: List[dict]):
        for flute in flutes:
            new_flute = Flut(**flute, american_box_id=box_id)
            self.db.add(new_flute)
        self.db.commit()

    def update_waste(self, box_id: int, waste: float) -> Optional[AmericanBox]:
        box = self.db.query(AmericanBox).filter(AmericanBox.id == box_id).first()
        if not box:
            return None
        box.waste_weight = waste
        self.db.commit()
        self.db.refresh(box)
        return box
    
    def get_clients(self) -> list[ClientOut]:
        return (
            self.db.query(ClientAccount)
            .join(AmericanBox, ClientAccount.id == AmericanBox.client_id)
            .distinct()
            .all()
        )
    def get_by_client(self, client_id: int) -> List[AmericanBox]:
        return self.db.query(AmericanBox).filter(AmericanBox.client_id == client_id).all()
