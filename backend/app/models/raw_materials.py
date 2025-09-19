from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from app.database import Base

class RawMaterial(Base):
    __tablename__ = "raw_material"

    id = Column(Integer, primary_key=True)
    serial_number = Column(String, unique=True)
    category = Column(String, nullable=False)
    supplier_name = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    paper_type = Column(String, nullable=False)
    roll_width = Column(Float, nullable=False)
    gsm = Column(Float, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
    job_order_id = Column(Integer, nullable=False)
    status = Column(String, default="Not priced")

    paper_rolls = relationship(
        "PaperRoll",
        backref=backref("raw_material", passive_deletes=True),  
        passive_deletes=True
    )