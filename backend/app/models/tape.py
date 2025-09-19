from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Tape(Base):
    __tablename__ = "tape"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable= True)
    size_raw = Column(String, nullable= True)
    width = Column(Float, nullable= True)
    thickness = Column(String, nullable= True)
    length = Column(Float, nullable= True)
    gross_weight = Column(Float, nullable= True)
    roll_number = Column(String, nullable= True)
    made_in = Column(String, nullable= True)