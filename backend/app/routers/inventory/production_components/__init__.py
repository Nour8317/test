
from fastapi import APIRouter
from app.routers.inventory.production_components.Packaging import router as packaging_router
from app.routers.inventory.production_components.Adhesives_Glue import router as adhesives_glue_router
from app.routers.inventory.production_components.Inks_and_Solvents import router as inks_and_solvents_router
from app.routers.inventory.production_components.Chemicals import router as chemicals_router
from app.routers.inventory.production_components.stitching_material import router as stitching_material_router
from app.routers.inventory.production_components.production_component import router as production_component_router

production_components_router = APIRouter()



production_components_router.include_router(packaging_router, tags=["packaging"])
production_components_router.include_router(adhesives_glue_router, tags=["adhesive glue"])
production_components_router.include_router(inks_and_solvents_router, tags=["inks and solvents"])
production_components_router.include_router(chemicals_router, tags=["chemicals"])
production_components_router.include_router(stitching_material_router, tags=["stitching material"])
production_components_router.include_router(production_component_router, tags=["production component"])
