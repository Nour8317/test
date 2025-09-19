from fastapi import FastAPI
from app.database import engine
from app.rate_limiting import limiter
from app import models
from app.routers.admin import paper_type
from app.routers.admin import gsm
from app.routers.inventory.production_components import (
    stitching_material,
    Chemicals,
    Packaging,
    Adhesives_Glue,
    Inks_and_Solvents,
    production_component,
)
from app.routers.inventory.rolls_inventory import (
    raw_material_router,
    paper_rolls_router
)
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.routers import employee 
from app.routers import department 
from app.routers.client_account import client_account
from app.routers.client_account import american_box
from app.routers.client_account import flut
from app.routers.client_account import sheet_carton
from app.routers.client_account import rolls
from app.routers import job_order
from app.routers import tape
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My App",
        version="1.0",
        description="API for employees and departments",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2Password": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/employees/login/swagger", 
                    "scopes": {}
                }
            }
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"OAuth2Password": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

Base.metadata.create_all(bind=engine)
app.openapi = custom_openapi

app.include_router(employee.router, prefix="/employees", tags=["employees"])
app.include_router(client_account.router, prefix="/client", tags=["client"])
app.include_router(american_box.router, prefix="/american_box", tags=["american box"])
app.include_router(sheet_carton.router, prefix="/sheet_carton", tags=["sheet carton"])
app.include_router(rolls.router, prefix="/rolls", tags=["rolls"])
app.include_router(flut.router, prefix="/flut", tags=["flut"])
app.include_router(department.router, prefix="/department", tags=["department"])
app.include_router(raw_material_router, prefix="/raw-materials", tags=["raw materials"])
app.include_router(paper_rolls_router, prefix="/paper-rolls", tags=["paper rolls"])
app.include_router(stitching_material.router, prefix="/stitching-material", tags=["stitching material"])
app.include_router(Chemicals.router, prefix="/chemicals", tags=["chemicals"])
app.include_router(Packaging.router, prefix="/packaging", tags=["packaging"])
app.include_router(Adhesives_Glue.router, prefix="/adhesive-glue", tags=["adhesive glue"])
app.include_router(Inks_and_Solvents.router, prefix = "/inks-and-solvents", tags =["inks and solvents"])
app.include_router(production_component.router, prefix="/production-component", tags=["production component"])
app.include_router(gsm.router, prefix="/gsm", tags=["gsm"])
app.include_router(paper_type.router, prefix="/paper-type", tags=["paper type"])
app.include_router(job_order.router, prefix="/job_orders", tags=["Job Orders"])
app.include_router(tape.router, prefix="/tapes", tags=["Tapes"])



