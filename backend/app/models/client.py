from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class ClientAccount(Base):
    __tablename__ = "client_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    contact = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    american_boxes = relationship("AmericanBox", back_populates="client")
    sheet_cartons = relationship("SheetCarton", back_populates="client")
    rolls = relationship("Rolls", back_populates="client")
    job_orders = relationship("JobOrder", secondary="client_job_orders", back_populates="clients")

