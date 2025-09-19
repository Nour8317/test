from sqlalchemy.orm import Session
from app.models.chemicals import Chemicals
from app.schemas.chemicals import ChemicalsCreate, ChemicalsUpdate

class ChemicalsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, chemical: ChemicalsCreate):
        db_chemical = Chemicals(**chemical.dict())
        self.db.add(db_chemical)
        self.db.commit()
        self.db.refresh(db_chemical)
        return db_chemical

    def get_all(self):
        return self.db.query(Chemicals).all()

    def get_by_id(self, chemical_id: int):
        return self.db.query(Chemicals).filter(Chemicals.id == chemical_id).first()

    def update(self, chemical_id: int, updated_data: ChemicalsUpdate):
        chemical = self.get_by_id(chemical_id)
        if not chemical:
            return None
        for key, value in updated_data.dict().items():
            setattr(chemical, key, value)
        self.db.commit()
        self.db.refresh(chemical)
        return chemical

    def delete(self, chemical_id: int):
        chemical = self.get_by_id(chemical_id)
        if not chemical:
            return None
        self.db.delete(chemical)
        self.db.commit()
        return chemical
