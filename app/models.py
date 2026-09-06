from enum import unique

from sqlalchemy import Column, Integer, String, func, TIMESTAMP,text
from .database import Base


class Course(Base):
    __tablename__ = 'courses'

    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )