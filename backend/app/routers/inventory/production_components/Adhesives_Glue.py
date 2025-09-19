from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth.jwt_handler import check_resource_permission, get_current_admin
from app.schemas.adhesives_glue import AdhesivesGlueCreate, AdhesivesGlueOut
from app.repositories.adhesives_glue_repository import AdhesivesGlueRepository
from app.services.adhesives_glue_service import AdhesivesGlueService

router = APIRouter()

def get_service(db: Session = Depends(get_db)):
    repo = AdhesivesGlueRepository(db)
    return AdhesivesGlueService(repo)

@router.post("/", response_model=AdhesivesGlueOut, dependencies=[Depends(check_resource_permission("adhesive glue"))])
def create_glue_material(data: AdhesivesGlueCreate, service: AdhesivesGlueService = Depends(get_service)):
    return service.create(data)

@router.get("/", response_model=List[AdhesivesGlueOut], dependencies=[Depends(check_resource_permission("adhesive glue"))])
def get_all_glue_materials(service: AdhesivesGlueService = Depends(get_service)):
    return service.get_all()

@router.get("/{material_id}", response_model=AdhesivesGlueOut, dependencies=[Depends(check_resource_permission("adhesive glue"))])
def get_glue_material(material_id: int, service: AdhesivesGlueService = Depends(get_service)):
    return service.get_one(material_id)

@router.put("/{material_id}", response_model=AdhesivesGlueOut, dependencies=[Depends(check_resource_permission("adhesive glue"))])
def update_glue_material(material_id: int, data: AdhesivesGlueCreate, service: AdhesivesGlueService = Depends(get_service)):
    return service.update(material_id, data)

@router.delete("/{material_id}", dependencies=[Depends(get_current_admin)])
def delete_glue_material(material_id: int, service: AdhesivesGlueService = Depends(get_service)):
    service.delete(material_id)
    return {"detail": "Glue material deleted"}
