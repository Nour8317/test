from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from app.schemas.stitching_material import StitchingMaterialCreate
from app.models.stitching_material import StitchingMaterial
from app.repositories.stitching_material_repository import StitchingMaterialRepository


class StitchingMaterialService:
    def __init__(self, db: Session):
        self.repo = StitchingMaterialRepository(db)

    def create(self, data: StitchingMaterialCreate) -> StitchingMaterial:
        row = StitchingMaterial(**data.dict())
        return self.repo.add(row)

    def get_all(self) -> List[StitchingMaterial]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> StitchingMaterial:
        row = self.repo.get_by_id(id)
        if not row:
            raise HTTPException(status_code=404, detail="Material not found")
        return row

    def update(self, id: int, data: StitchingMaterialCreate) -> StitchingMaterial:
        row = self.repo.get_by_id(id)
        if not row:
            raise HTTPException(status_code=404, detail="Material not found")
        for key, value in data.dict().items():
            setattr(row, key, value)
        self.repo.db.commit()
        self.repo.db.refresh(row)
        return row

    def delete(self, id: int) -> dict:
        row = self.repo.get_by_id(id)
        if not row:
            raise HTTPException(status_code=404, detail="Material not found")
        self.repo.db.delete(row)
        self.repo.db.commit()
        return {"detail": "Material deleted successfully"}
