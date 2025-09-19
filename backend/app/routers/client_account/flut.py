from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.models.flut import Flut
from app.schemas.flut import FlutBatchCreate, FlutCreate, FlutOut
router = APIRouter()

@router.post("/", response_model=List[FlutOut])
def create_fluts(fluts: List[FlutCreate], db: Session = Depends(get_db)):
    created = []
    for flut_data in fluts:
        db_flut = models.Flut(**flut_data.dict())
        db.add(db_flut)
        created.append(db_flut)
    db.commit()
    return created


@router.post("/create_batch", status_code=201)
def create_flut_batch(payload: FlutBatchCreate, db: Session = Depends(get_db)):
    fluts = payload.fluts

    if not fluts:
        raise HTTPException(status_code=400, detail="No fluts provided.")

    first = fluts[0]

    product_type = None
    product_id = None
    polygon_type = None

    if first.american_box_id:
        product_type = "american_box_id"
        product_id = first.american_box_id
        product = db.query(models.AmericanBox).filter_by(id=product_id).first()
    elif first.sheet_carton_id:
        product_type = "sheet_carton_id"
        product_id = first.sheet_carton_id
        product = db.query(models.SheetCarton).filter_by(id=product_id).first()
    elif first.roll_id:
        product_type = "roll_id"
        product_id = first.roll_id
        product = db.query(models.Rolls).filter_by(id=product_id).first()
    else:
        raise HTTPException(status_code=400, detail="Each flut must be linked to exactly one product.")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    polygon_type = getattr(product, "polygon_type", None)
    if not polygon_type:
        raise HTTPException(status_code=400, detail="Product does not have a polygon_type.")

    for f in fluts:
        links = [f.american_box_id, f.sheet_carton_id, f.roll_id]
        non_null_links = [x for x in links if x is not None]
        if len(non_null_links) != 1:
            raise HTTPException(status_code=400, detail="Each flut must be linked to exactly one product (AmericanBox, SheetCarton, or Roll).")
        if getattr(f, product_type) != product_id:
            raise HTTPException(status_code=400, detail="All fluts must be linked to the same product.")

    n_fluts = len(fluts)
    expected_fluts = 3 if polygon_type == "single" else 4 if n_fluts == 4 else 5 if n_fluts == 5 else None
    if polygon_type == "single" and n_fluts != 3:
        raise HTTPException(status_code=400, detail="Single polygon type must have exactly 3 fluts.")
    if polygon_type == "double" and n_fluts not in [4, 5]:
        raise HTTPException(status_code=400, detail="Double polygon type must have 4 or 5 fluts.")

    gsm = 0
    if polygon_type == "single" and n_fluts == 3:
        gsm = fluts[0].weight + (fluts[1].weight * 1.4) + fluts[2].weight
    elif polygon_type == "double 4" and n_fluts == 4:
        gsm = fluts[0].weight + (fluts[1].weight * 1.4) + fluts[2].weight + (fluts[3].weight * 1.4)
    elif polygon_type == "double 5" and n_fluts == 5:
        gsm = fluts[0].weight + (fluts[1].weight * 1.4) + fluts[2].weight + (fluts[3].weight * 1.4) + fluts[4].weight
    else:
        raise HTTPException(status_code=400, detail="Invalid flut count for polygon type.")

    flut_objects = [
        Flut(
            layer_number=f.layer_number,
            paper_type=f.paper_type,
            supplier=f.supplier,
            weight=f.weight,
            american_box_id=f.american_box_id,
            sheet_carton_id=f.sheet_carton_id,
            roll_id=f.roll_id,
        )
        for f in fluts
    ]
    db.add_all(flut_objects)

    product.gsm = gsm
    db.commit()

    return {"message": f"{len(flut_objects)} flut(s) created successfully.", "gsm": gsm}