from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database import Base


class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)

    cinema_id = Column(
        Integer,
        ForeignKey("cinemas.id"),
        nullable=False
    )

    movie_name = Column(String, nullable=False)

    show_time = Column(DateTime, nullable=False)