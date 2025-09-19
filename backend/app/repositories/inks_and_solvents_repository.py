from app.repositories.base import BaseRepository
from app.models.ink_and_solvents import InksandSolvents
from sqlalchemy.orm import Session 

class InksandSolventsRepository(BaseRepository[InksandSolvents]):
    def __init__(self, db: Session): 
        super().__init__(InksandSolvents, db) 