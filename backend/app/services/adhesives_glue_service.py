from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.adhesives_glue_repository import AdhesivesGlueRepository
from app.schemas.adhesives_glue import AdhesivesGlueCreate
from app.models.adhesives_glue import AdhesivesGlue

class AdhesivesGlueService:
    def __init__(self, repo: AdhesivesGlueRepository):
        self.repo = repo

    def create(self, data: AdhesivesGlueCreate) -> AdhesivesGlue:
        return self.repo.create(data.dict())

    def get_all(self) -> list[AdhesivesGlue]:
        return self.repo.get_all()

    def get_one(self, material_id: int) -> AdhesivesGlue:
        row = self.repo.get(material_id)
        if not row:
            raise HTTPException(status_code=404, detail="Glue material not found")
        return row

    def update(self, material_id: int, data: AdhesivesGlueCreate) -> AdhesivesGlue:
        row = self.repo.update(material_id, data.dict())
        if not row:
            raise HTTPException(status_code=404, detail="Glue material not found")
        return row

    def delete(self, material_id: int) -> dict:
        success = self.repo.delete(material_id)
        if not success:
            raise HTTPException(status_code=404, detail="Glue material not found")
        return {"detail": "Glue material deleted"}
