from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class PaperType(Base):
    __tablename__ = "paper_type"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False,unique=True)
