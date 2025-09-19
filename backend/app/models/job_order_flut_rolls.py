from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base


class JobOrderFlutRoll(Base):
    __tablename__ = "job_order_flut_rolls"

    id = Column(Integer, primary_key=True, index=True)
    job_order_item_id = Column(Integer, ForeignKey("job_order_items.id", ondelete="CASCADE"), nullable=True)
    flut_id = Column(Integer, ForeignKey("flut.id", ondelete="CASCADE"), nullable=True)
    paper_roll_id = Column(Integer, ForeignKey("paper_rolls.id", ondelete="CASCADE"), nullable=True)

    allocated_width = Column(Float, nullable=True)
    calculated_weight = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    job_order_item = relationship("JobOrderItem", back_populates="flut_rolls")
    flut = relationship("Flut")
    paper_roll = relationship("PaperRoll", back_populates="job_order_links")

