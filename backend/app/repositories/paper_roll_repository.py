from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.models import PaperRoll, RawMaterial
from app.repositories.base import BaseRepository


class PaperRollRepository(BaseRepository[PaperRoll]):
    def __init__(self, db: Session):
        super().__init__(PaperRoll,db)

    def get_by_raw_material(self, raw_material_id: int) -> List[PaperRoll]:
        return (
            self.db.query(PaperRoll)
            .filter(PaperRoll.raw_id == raw_material_id, PaperRoll.status == "available")
            .all()
        )

    def get_groups(self):
        return (
            self.db.query(
                PaperRoll.gsm,
                RawMaterial.category,
                RawMaterial.degree,
                PaperRoll.paper_type,
                PaperRoll.raw_id,
                func.count(PaperRoll.id).label("count"),
            )
            .join(RawMaterial, PaperRoll.raw_id == RawMaterial.id)
            .group_by(
                PaperRoll.gsm,
                RawMaterial.category,
                RawMaterial.degree,
                PaperRoll.paper_type,
                PaperRoll.raw_id,
            )
            .having(func.count(PaperRoll.id) > 1)
            .all()
        )

    def get_by_serial(self, serial_number: str) -> Optional[PaperRoll]:
        return self.db.query(PaperRoll).filter(PaperRoll.serial_number == serial_number).first()
    
    
    def get_by_id(self, id: int) -> Optional[PaperRoll]:
        return self.db.query(PaperRoll).filter(PaperRoll.id == id).first()
