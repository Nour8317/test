from fastapi import APIRouter
from app.routers.inventory.rolls_inventory.paper_rolls import router as paper_rolls_router
from app.routers.inventory.rolls_inventory.rawmaterials import router as raw_material_router

router = APIRouter()
router.include_router(paper_rolls_router)
router.include_router(raw_material_router)

rolls_inventory_router = router
