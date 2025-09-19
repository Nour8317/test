from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class EmployeeDepartment(Base):
    __tablename__ = "employee_department"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id", ondelete="CASCADE"))
    department_id = Column(Integer, ForeignKey("department.id", ondelete="CASCADE"))

    employee = relationship("Employee", back_populates="departments")
    department = relationship("Department", back_populates="employees")

    __table_args__ = (UniqueConstraint("employee_id", "department_id", name="uix_employee_department"),)
