from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.auth.jwt_handler import check_resource_permission
from app.database import get_db
from app.schemas.production_components import ProductionComponentOut, DeductByComponentRequest
from app.services.production_component_service import ProductionComponentService

router = APIRouter()

def get_service(db: Session = Depends(get_db)):
    return ProductionComponentService(db)

@router.get(
    "/", 
    response_model=List[ProductionComponentOut],
    dependencies=[Depends(check_resource_permission("production component"))]
)
def get_production_components(service: ProductionComponentService = Depends(get_service)):
    return service.get_all()

@router.get(
    "/get-by-component", 
    response_model=List[ProductionComponentOut],
    dependencies=[Depends(check_resource_permission("production component"))]
)
def get_by_component(component: str, service: ProductionComponentService = Depends(get_service)):
    return service.get_by_component(component)

@router.post(
    "/deduct-by-component",
    response_model=ProductionComponentOut,
    dependencies=[Depends(check_resource_permission("production component"))]
)
def deduct_by_component(data: DeductByComponentRequest, service: ProductionComponentService = Depends(get_service)):
    return service.deduct_by_component(data)
