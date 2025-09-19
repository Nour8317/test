from app.repositories.base import BaseRepository
from app.models.gsm import Gsm

class GsmRepository(BaseRepository[Gsm]):
    def __init__(self,db):
        super().__init__(Gsm,db)
