from sqlalchemy import Column, Integer, String
from .database import Base


class Course(Base):
    __tablename__ = 'courses'

    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
