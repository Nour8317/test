from sqlalchemy.orm import Session
from app.repositories.raw_material_repository import RawMaterialRepository
from app.schemas.raw_material import RawMaterialCreate
from app.models.raw_materials import RawMaterial
from datetime import datetime

CATEGORY_MAP = {"Imported": "I", "Local": "L"}

class RawMaterialService:
    def __init__(self, db: Session):
        self.repo = RawMaterialRepository(db)

    def create_raw_material(self, data: RawMaterialCreate):
        if data.category not in CATEGORY_MAP:
            raise ValueError("Invalid category")

        raw = RawMaterial(**data.dict(exclude={"weights"}))
        raw.received_at = datetime.utcnow()
        created = self.repo.create(raw)

        # Generate serial number
        date_str = raw.received_at.strftime("%Y%m%d")
        paper_type_abbr = "".join(word[0] for word in raw.paper_type.split()).upper()
        raw.serial_number = f"{CATEGORY_MAP[raw.category]}-{paper_type_abbr}-{date_str}-{raw.id}".upper()

        return self.repo.update(raw)

    def get_raw_materials(self):
        return self.repo.get_all()

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_by_supplier(self, supplier_name: str):
        return self.repo.get_by_supplier(supplier_name)

    def get_unpriced(self):
        return self.repo.get_unpriced()

    def update_raw_material(self, id: int, data: RawMaterialCreate):
        raw = self.repo.get_by_id(id)
        if not raw:
            return None
        for key, value in data.dict().items():
            setattr(raw, key, value)
        return self.repo.update(raw)

    def delete_raw_material(self, id: int):
        raw = self.repo.get_by_id(id)
        if raw:
            self.repo.delete(raw)
            return True
        return False
