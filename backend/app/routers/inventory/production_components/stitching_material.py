from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth.jwt_handler import check_resource_permission, get_current_admin
from app.schemas.stitching_material import StitchingMaterialOut, StitchingMaterialCreate
from app.services.stitching_material_service import StitchingMaterialService

router = APIRouter()


@router.post("/", response_model=StitchingMaterialOut, dependencies=[Depends(check_resource_permission("stitching material"))])
def create_stitching_material(data: StitchingMaterialCreate, db: Session = Depends(get_db)):
    return StitchingMaterialService(db).create(data)


@router.get("/", response_model=List[StitchingMaterialOut], dependencies=[Depends(check_resource_permission("stitching material"))])
def get_all_stitching_materials(db: Session = Depends(get_db)):
    return StitchingMaterialService(db).get_all()


@router.get("/{id}", response_model=StitchingMaterialOut, dependencies=[Depends(check_resource_permission("stitching material"))])
def get_stitching_material(id: int, db: Session = Depends(get_db)):
    return StitchingMaterialService(db).get_by_id(id)


@router.put("/{id}", response_model=StitchingMaterialOut, dependencies=[Depends(check_resource_permission("stitching material"))])
def update_stitching_material(id: int, data: StitchingMaterialCreate, db: Session = Depends(get_db)):
    return StitchingMaterialService(db).update(id, data)


@router.delete("/{id}", dependencies=[Depends(get_current_admin)])
def delete_stitching_material(id: int, db: Session = Depends(get_db)):
    return StitchingMaterialService(db).delete(id)
