from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class PaperRoll(Base):
    __tablename__ = "paper_rolls"

    id = Column(Integer, primary_key=True, index=True)
    raw_id = Column(Integer, ForeignKey("raw_material.id", ondelete="CASCADE"))
    roll_id = Column(Integer, nullable=False)
    paper_type = Column(String, nullable=False)
    gsm = Column(Float, nullable=False)
    roll_width = Column(Float, nullable=False)
    job_order_id = Column(Integer)
    serial_number = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False, default="available")
    degree = Column(String)
    weight = Column(Float)
    cost = Column(Float)
    currency = Column(String)

    
    job_order_links = relationship("JobOrderFlutRoll", back_populates="paper_roll")



