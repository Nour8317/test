from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey, String, func
from sqlalchemy.orm import relationship
from app.database import Base


class ClientJobOrder(Base):
    __tablename__ = "client_job_orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("client_account.id", ondelete="CASCADE"))
    job_order_id = Column(Integer, ForeignKey("job_orders.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now())