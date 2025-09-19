from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models.tape import Tape
from app.schemas.tape import TapeCreate, TapeUpdate, TapeResponse

router = APIRouter()

@router.post("/", response_model=TapeResponse)
async def create_tape(tape: TapeCreate, db: Session = Depends(get_db)):
    new_tape = Tape(**tape.dict())
    db.add(new_tape)
    db.commit()
    db.refresh(new_tape)
    return new_tape

@router.get("/", response_model=List[TapeResponse])
async def read_tapes(db: Session = Depends(get_db)):
    tapes = db.query(Tape).all()
    return tapes

@router.get("/{tape_id}", response_model=TapeResponse)
async def read_tape(tape_id: int, db: Session = Depends(get_db)):
    tape = db.query(Tape).filter(Tape.id == tape_id).first()
    if not tape:
        raise HTTPException(status_code=404, detail="Tape not found")
    return tape

@router.put("/{tape_id}", response_model=TapeResponse)
async def update_tape(tape_id: int, tape_update: TapeUpdate, db: Session = Depends(get_db)):
    tape = db.query(Tape).filter(Tape.id == tape_id).first()
    if not tape:
        raise HTTPException(status_code=404, detail="Tape not found")
    for key, value in tape_update.dict(exclude_unset=True).items():
        setattr(tape, key, value)
    db.add(tape)
    db.commit()
    db.refresh(tape)
    return tape