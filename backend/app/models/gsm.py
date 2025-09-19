from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Gsm(Base):
    __tablename__ = "gsm"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False,unique=True)
