from sqlalchemy import Column, Float, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class JobOrderItem(Base):
    __tablename__ = "job_order_items"

    id = Column(Integer, primary_key=True, index=True)
    job_order_id = Column(Integer, ForeignKey("job_orders.id", ondelete="CASCADE"), nullable=False)
    item_type = Column(String(50), nullable=False)  
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    sheet_length = Column(Float, nullable=True)
    sheet_width = Column(Float, nullable=True)
    number_of_outs = Column(Integer, nullable=True)

    job_order = relationship("JobOrder", back_populates="items")
    flut_rolls = relationship("JobOrderFlutRoll", back_populates="job_order_item", cascade="all, delete-orphan")

