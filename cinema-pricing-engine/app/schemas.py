from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CinemaCreate(BaseModel):
    name: str = Field(min_length=1)


class CinemaResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ShowCreate(BaseModel):
    cinema_id: int
    movie_name: str = Field(min_length=1)
    show_time: datetime


class ShowResponse(BaseModel):
    id: int
    cinema_id: int
    movie_name: str
    show_time: datetime

    class Config:
        from_attributes = True


class SeatTierCreate(BaseModel):
    show_id: int
    name: str = Field(min_length=1)
    price: Decimal = Field(gt=0)
    total_seats: int = Field(gt=0)


class SeatTierResponse(BaseModel):
    id: int
    show_id: int
    name: str
    price: Decimal
    total_seats: int
    available_seats: int

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    show_id: int
    seat_tier_id: int
    quantity: int = Field(gt=0)
    is_member: bool = False


class PricingRulesCreate(BaseModel):
    festival_discount: Decimal = Field(ge=0)
    member_discount_percent: Decimal = Field(ge=0, le=100)
    member_discount_cap: Decimal = Field(ge=0)
    convenience_fee_per_ticket: Decimal = Field(ge=0)
    gst_percent: Decimal = Field(ge=0, le=100)


class Bill(BaseModel):
    base_amount: Decimal
    festival_discount: Decimal
    member_discount: Decimal
    subtotal: Decimal
    convenience_fee: Decimal
    taxable_amount: Decimal
    gst: Decimal
    total: Decimal


class BookingResponse(BaseModel):
    booking_id: int
    show_id: int
    seat_tier: str
    quantity: int
    is_member: bool
    bill: Bill