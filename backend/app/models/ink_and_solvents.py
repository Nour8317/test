from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base



class InksandSolvents(Base):
    __tablename__ = "inks_and_solvents"
    id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String, nullable=True)
    material_type = Column(String, nullable=True)
    color = Column(String)
    weight = Column(Float)
    quantity = Column(Integer)
    supplier_name = Column(String)
    color_code = Column(String)
    cost = Column(Float, nullable=True)
    received_at = Column(DateTime, default=datetime.utcnow)