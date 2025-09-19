from app.repositories.base import BaseRepository
from app.models.packaging import Packaging
from sqlalchemy.orm import Session

class PackagingRepository(BaseRepository[Packaging]):
    def __init__(self, db: Session): 
        super().__init__(Packaging, db) 