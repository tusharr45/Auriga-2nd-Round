from sqlalchemy import Column, Integer, String, Numeric, ForeignKey

from app.database import Base


class SeatTier(Base):
    __tablename__ = "seat_tiers"

    id = Column(Integer, primary_key=True, index=True)

    show_id = Column(
        Integer,
        ForeignKey("shows.id"),
        nullable=False
    )

    name = Column(String, nullable=False)

    price = Column(Numeric(10, 2), nullable=False)

    total_seats = Column(Integer, nullable=False)

    available_seats = Column(Integer, nullable=False)