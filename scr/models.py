from sqlalchemy import Column, DateTime, Integer

from .database import Base


class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    key = Column(Integer, unique=True, index=True)
    Expires = Column(DateTime, nullable=True)