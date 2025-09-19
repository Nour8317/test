from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Flut(Base):
    __tablename__ = "flut"

    id = Column(Integer, primary_key=True)
    layer_number = Column(Integer, nullable=False)
    paper_type = Column(String(100), nullable=False)
    supplier = Column(String(255), nullable=True)
    weight = Column(Float, nullable=True)
    calculated_weight = Column(Float, nullable=True)  # <-- Add this line

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    american_box_id = Column(Integer, ForeignKey("american_box.id"), nullable=True)
    roll_id = Column(Integer, ForeignKey("rolls.id"), nullable=True)
    sheet_carton_id = Column(Integer, ForeignKey("sheet_carton.id"), nullable=True)

    american_box = relationship("AmericanBox", back_populates="flutes")
    sheet_carton = relationship("SheetCarton", back_populates="flutes")
    roll = relationship("Rolls", back_populates="flutes")
