from typing import List
from sqlalchemy.orm import Session
from app.models.rolls import Rolls
from app.models.flut import Flut
from app.schemas.rolls import RollWithFlutesCreate
from app.models.client import ClientAccount
from app.schemas.client import ClientOut

class RollsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_with_flutes(self, roll_data: RollWithFlutesCreate):
        db_roll = Rolls(
            client_id=roll_data.client_id,
            roll_width=roll_data.roll_width,
            form=roll_data.form,
            notes=roll_data.notes,
            polygon_type=roll_data.polygon_type,
            polygon_category=roll_data.polygon_category,
            cost=roll_data.cost,
            currency=roll_data.currency,
        )
        self.db.add(db_roll)
        self.db.commit()
        self.db.refresh(db_roll)

        for f in roll_data.flutes:
            db_flut = Flut(**f.dict(), roll_id=db_roll.id)
            self.db.add(db_flut)

        self.db.commit()
        self.db.refresh(db_roll)
        return db_roll

    def get_all(self):
        return self.db.query(Rolls).all()

    def get_by_id(self, roll_id: int):
        return self.db.query(Rolls).filter(Rolls.id == roll_id).first()
    
    def get_by_client_id(self, client_id: int):
        return self.db.query(Rolls).filter(Rolls.client_id == client_id).all()

    def get_clients(self) -> List[ClientOut]:
        return (
            self.db.query(ClientAccount)
            .join(Rolls, ClientAccount.id == Rolls.client_id)
            .distinct()
            .all()
        )
    def delete(self, roll: Rolls):
        self.db.delete(roll)
        self.db.commit()

    def update_waste(self, roll: Rolls, waste: float):
        roll.waste_weight = waste
        self.db.commit()
        self.db.refresh(roll)
        return roll
