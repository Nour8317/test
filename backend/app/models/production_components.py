from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ProductionComponents(Base):
    __tablename__ = "production_component"
    id = Column(Integer, primary_key=True, index=True)
    component = Column(String)
    material_name = Column(String, nullable= True)
    material_type = Column(String, nullable= True)
    color = Column(String)
    weight = Column(Float)
    quantity = Column(Integer)
    color_code = Column(String)
    dimensions = Column(Float) 
    updated_at = Column(DateTime, default=datetime.utcnow)
