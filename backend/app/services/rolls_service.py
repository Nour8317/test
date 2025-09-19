from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.rolls_repository import RollsRepository
from app.schemas.rolls import RollWithFlutesCreate

class RollsService:
    def __init__(self, db: Session):
        self.repo = RollsRepository(db)

    def create_with_flutes(self, roll_data: RollWithFlutesCreate):
        return self.repo.create_with_flutes(roll_data)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, roll_id: int):
        roll = self.repo.get_by_id(roll_id)
        if not roll:
            raise HTTPException(status_code=404, detail="Roll not found")
        return roll

    def get_by_client_id(self, client_id: int):
        rolls = self.repo.get_by_client_id(client_id)
        if not rolls:
            raise HTTPException(status_code=404, detail="No rolls found for this client")
        return rolls
    
    def get_clients(self):
        return self.repo.get_clients()
    
    def delete(self, roll_id: int):
        roll = self.repo.get_by_id(roll_id)
        if not roll:
            raise HTTPException(status_code=404, detail="Roll not found")
        self.repo.delete(roll)
        return {"detail": "Deleted successfully"}

    def update_waste(self, roll_id: int, waste: float):
        roll = self.repo.get_by_id(roll_id)
        if not roll:
            raise HTTPException(status_code=404, detail="Roll not found")
        return self.repo.update_waste(roll, waste)
