from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    no_of_managers = Column(Integer)
    employees = relationship("EmployeeDepartment", back_populates="department", cascade="all, delete")
    router_accesses = relationship("RouterAccess", back_populates="department", cascade="all, delete")
