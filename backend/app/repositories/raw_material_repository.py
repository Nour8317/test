from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.raw_materials import RawMaterial
from app.repositories.base import BaseRepository

class RawMaterialRepository(BaseRepository[RawMaterial]):
    def __init__(self, db: Session):
        super().__init__(RawMaterial, db)

    def get_by_serial_number(self, serial_number: str) -> Optional[RawMaterial]:
        return self.db.query(self.model).filter(self.model.serial_number == serial_number).first()

    def get_by_category(self, category: str) -> List[RawMaterial]:
        return self.db.query(self.model).filter(self.model.category == category).all()
    
    def get_by_name(self, name: str) -> Optional[RawMaterial]:
        return self.db.query(RawMaterial).filter(RawMaterial.name == name).first()

    def get_by_category(self, category: str) -> List[RawMaterial]:
        return self.db.query(RawMaterial).filter(RawMaterial.category == category).all()

    def decrease_stock(self, material_id: int, amount: float) -> Optional[RawMaterial]:
        """Decrease stock by `amount` and return updated object"""
        raw_material = self.get(material_id)
        if not raw_material:
            return None
        if raw_material.stock < amount:
            raise ValueError("Not enough stock available")
        raw_material.stock -= amount
        self.db.commit()
        self.db.refresh(raw_material)
        return raw_material