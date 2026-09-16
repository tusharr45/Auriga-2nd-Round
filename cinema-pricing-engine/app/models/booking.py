from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    show_id = Column(
        Integer,
        ForeignKey("shows.id"),
        nullable=False
    )

    seat_tier_id = Column(
        Integer,
        ForeignKey("seat_tiers.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    is_member = Column(Boolean, nullable=False, default=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )