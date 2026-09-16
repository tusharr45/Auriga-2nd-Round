from sqlalchemy import Column, Integer, String

from app.database import Base


class Cinema(Base):
    __tablename__ = "cinemas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)