from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.stitching_material import StitchingMaterial
from app.repositories.base import BaseRepository


class StitchingMaterialRepository(BaseRepository[StitchingMaterial]):
    def __init__(self, db: Session):
        super().__init__(StitchingMaterial,db)

    def get_all(self) -> List[StitchingMaterial]:
        return self.db.query(StitchingMaterial).all()

    def get_by_id(self, id: int) -> Optional[StitchingMaterial]:
        return self.db.query(StitchingMaterial).filter(StitchingMaterial.id == id).first()
