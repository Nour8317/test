from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from app.models import PaperRoll, RawMaterial
from app.schemas.paper_roll import PaperRollCreate, RollPriceRequest
from app.repositories.paper_roll_repository import PaperRollRepository


class PaperRollService:
    def __init__(self, db: Session):
        self.repo = PaperRollRepository(db)

    def list(self) -> List[PaperRoll]:
        return self.repo.get_all()

    def get(self, id: int) -> PaperRoll:
        roll = self.repo.get_by_id(id)
        if not roll:
            raise HTTPException(status_code=404, detail="Paper roll not found")
        return roll

    def get_by_raw_material(self, raw_material_id: int) -> List[PaperRoll]:
        rolls = self.repo.get_by_raw_material(raw_material_id)
        if not rolls:
            raise HTTPException(status_code=404, detail="Paper roll not found")
        return rolls

    def get_groups(self):
        results = self.repo.get_groups()
        return [
            {
                "gsm": gsm,
                "category": category,
                "degree": degree,
                "paper_type": paper_type,
                "raw_id": raw_id,
                "count": count,
            }
            for gsm, category, degree, paper_type, raw_id, count in results
        ]

    def price_roll(self, roll_id: int, data: RollPriceRequest) -> dict:
        roll = self.repo.get_by_id(roll_id)
        if not roll:
            raise HTTPException(status_code=404, detail="PaperRoll not found")

        roll.cost = data.cost
        roll.currency = data.currency

        raw = roll.raw_material
        all_priced = all(r.cost and r.currency for r in raw.paper_rolls)
        raw.status = "Priced" if all_priced else "Not priced"

        self.repo.db.commit()
        self.repo.db.refresh(raw)

        return {"detail": f"PaperRoll {roll.id} priced successfully. RawMaterial {raw.serial_number} status: {raw.status}"}

    def use_roll(self, serial_number: str) -> dict:
        roll = self.repo.get_by_serial(serial_number)
        if not roll:
            raise HTTPException(status_code=404, detail="PaperRoll not found")

        raw_material = self.repo.db.query(RawMaterial).filter_by(id=roll.raw_id).first()
        if not raw_material:
            raise HTTPException(status_code=404, detail="RawMaterial not found")

        if raw_material.quantity > 0:
            raw_material.quantity -= 1

        roll.status = "used"
        self.repo.db.commit()
        return {"detail": f"PaperRoll {serial_number} marked as used, quantity updated."}

    def create(self, data: PaperRollCreate, weight: Optional[float]) -> PaperRoll:
        roll_data = PaperRollCreate(**data.dict(), weight=weight)
        roll = PaperRoll(**roll_data.dict())
        return self.repo.add(roll)

    def update(self, id: int, data: PaperRollCreate) -> PaperRoll:
        roll = self.repo.get_by_id(id)
        if not roll:
            raise HTTPException(status_code=404, detail="Paper roll not found")

        for key, value in data.dict().items():
            setattr(roll, key, value)

        self.repo.db.commit()
        self.repo.db.refresh(roll)
        return roll

    def update_weight(self, roll_id: int, weight: Optional[float]) -> PaperRoll:
        roll = self.repo.get_by_id(roll_id)
        if not roll:
            raise HTTPException(status_code=404, detail="Paper roll not found")

        roll.weight = weight
        self.repo.db.commit()
        self.repo.db.refresh(roll)
        return roll

    def set_cost_currency(self, barcode: str, cost: float, currency: str) -> PaperRoll:
        roll = self.repo.get_by_serial(barcode)
        if not roll:
            raise HTTPException(status_code=404, detail="Paper roll not found")

        roll.cost = cost
        roll.currency = currency

        self.repo.db.commit()
        self.repo.db.refresh(roll)
        return roll

    def delete(self, id: int) -> dict:
        roll = self.repo.get_by_id(id)
        if not roll:
            raise HTTPException(status_code=404, detail="Paper roll not found")
        self.repo.db.delete(roll)
        self.repo.db.commit()
        return {"detail": "Deleted"}
