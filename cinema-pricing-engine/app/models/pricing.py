from sqlalchemy import Column, Integer, Numeric

from app.database import Base


class PricingRules(Base):
    __tablename__ = "pricing_rules"

    id = Column(Integer, primary_key=True, index=True)

    festival_discount = Column(
        Numeric(10, 2),
        nullable=False,
        default=50.00
    )

    member_discount_percent = Column(
        Numeric(5, 2),
        nullable=False,
        default=10.00
    )

    member_discount_cap = Column(
        Numeric(10, 2),
        nullable=False,
        default=100.00
    )

    convenience_fee_per_ticket = Column(
        Numeric(10, 2),
        nullable=False,
        default=10.00
    )

    gst_percent = Column(
        Numeric(5, 2),
        nullable=False,
        default=18.00
    )