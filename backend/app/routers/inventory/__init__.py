from fastapi import APIRouter
from .rolls_inventory import rolls_inventory_router
from .production_components import production_components_router

inventory_router = APIRouter(prefix="/inventory", tags=["inventory"])
inventory_router.include_router(rolls_inventory_router)
inventory_router.include_router(production_components_router)
