from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.adhesives_glue import AdhesivesGlue
from app.repositories.base import BaseRepository

class AdhesivesGlueRepository(BaseRepository[AdhesivesGlue]):
    def __init__(self, db: Session):
        super().__init__(AdhesivesGlue, db)

    def get_by_supplier(self, supplier_name: str) -> List[AdhesivesGlue]:
        return self.db.query(AdhesivesGlue).filter(AdhesivesGlue.supplier_name == supplier_name).all()

    def get_by_type(self, material_type: str) -> List[AdhesivesGlue]:
        return self.db.query(AdhesivesGlue).filter(AdhesivesGlue.material_type == material_type).all()
