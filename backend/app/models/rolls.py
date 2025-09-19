from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Rolls(Base):
    __tablename__ = "rolls"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client_account.id"))
    client = relationship("ClientAccount", back_populates="rolls")
    gsm = Column(Float)
    roll_width = Column(Float)
    design = Column(String(255))
    form = Column(String(255))
    notes = Column(Text)
    polygon_type = Column(String(100))
    polygon_category = Column(String(100))
    total_weight = Column(Float)
    waste_weight = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    cost = Column(Float)         
    currency = Column(String(10))
    flutes = relationship("Flut", back_populates="roll")
