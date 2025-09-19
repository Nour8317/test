from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class AmericanBox(Base):
    __tablename__ = "american_box"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client_account.id"))
    client = relationship("ClientAccount", back_populates="american_boxes")
    gsm = Column(Float)
    carton_length = Column(Float)
    carton_width = Column(Float)
    carton_height = Column(Float)
    tounge_dimension = Column(Float)
    glue_type = Column(String(100))
    design = Column(String(255))
    form = Column(String(255))
    polygon_type = Column(String(100))
    polygon_category = Column(String(100))
    notes = Column(Text)
    sheet_length = Column(Float)
    sheet_width = Column(Float)
    flap_dimension = Column(Float)
    piece_weight = Column(Float)
    total_weight = Column(Float)
    total_length = Column(Float)
    rolls_weight = Column(Float)
    waste_weight = Column(Float)
    cost = Column(Float)        
    currency = Column(String(10))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    flutes = relationship("Flut", back_populates="american_box", cascade="all, delete-orphan")
