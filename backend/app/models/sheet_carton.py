from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class SheetCarton(Base):
    __tablename__ = "sheet_carton"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client_account.id"))
    client = relationship("ClientAccount", back_populates="sheet_cartons")
    gsm = Column(Float)
    polygon_type = Column(String(100))
    polygon_category = Column(String(100))
    form = Column(String(255))
    design = Column(String(255))
    notes = Column(Text)
    sheet_length = Column(Float)
    sheet_width = Column(Float)
    total_weight = Column(Float)
    rolls_weight = Column(Float)
    waste_weight = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    cost = Column(Float)        
    currency = Column(String(10))
    flutes = relationship("Flut", back_populates="sheet_carton")
