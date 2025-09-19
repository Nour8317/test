from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class JobOrder(Base):
    __tablename__ = "job_orders"

    id = Column(Integer, primary_key=True, index=True)
    working_width = Column(Float, nullable=False)
    calculated_weight = Column(Float, nullable=False)
    order_type = Column(String, nullable=False)
    meter_length = Column(Float, nullable=True)

    items = relationship("JobOrderItem", back_populates="job_order", cascade="all, delete")
    clients = relationship("ClientAccount", secondary="client_job_orders", back_populates="job_orders")
