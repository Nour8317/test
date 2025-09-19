from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.job_order import JobOrderCreate, JobOrderOut, JobOrderResponse, RollJobOrderCreate
from app.schemas.job_order_flut_rolls import FlutAssociationCreate
from app.services.job_order_service import JobOrderService

router = APIRouter()

@router.post("/", response_model=JobOrderOut)
def create_job_order(data: JobOrderCreate, db: Session = Depends(get_db)):
    return JobOrderService(db).create_job_order(data)

@router.post("/roll_job_order", response_model=JobOrderOut)
def create_roll_job_order(data: RollJobOrderCreate, db: Session = Depends(get_db)):
    return JobOrderService(db).create_roll_job_order(data)

@router.post("/{job_order_id}/associate-flut")
def associate_flut_with_job_order(job_order_id: int, data: FlutAssociationCreate, db: Session = Depends(get_db)):
    return JobOrderService(db).associate_flut_with_job_order(job_order_id, data)

@router.get("/{order_id}", response_model=JobOrderResponse)
def get_job_order(order_id: int, db: Session = Depends(get_db)):
    return JobOrderService(db).get_job_order(order_id)
