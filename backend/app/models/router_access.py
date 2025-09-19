from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class RouterAccess(Base):
    __tablename__ = "router_access"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("department.id", ondelete="CASCADE"))
    resource_name = Column(String, nullable=False)  # e.g., 'paper_rolls', 'raw_materials'

    department = relationship("Department", back_populates="router_accesses")
