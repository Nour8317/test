from sqlalchemy.orm import Session
from .base import BaseRepository
from app.models import PaperType

class PaperTypeRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(PaperType, db)