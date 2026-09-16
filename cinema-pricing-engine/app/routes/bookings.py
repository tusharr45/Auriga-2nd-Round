from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Booking, Show, SeatTier, PricingRules
from app.schemas import BookingCreate, BookingResponse
from app.services.pricing_service import calculate_bill


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db)
):
    # Find show
    show = db.query(Show).filter(
        Show.id == data.show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )

    # Find seat tier
    tier = db.query(SeatTier).filter(
        SeatTier.id == data.seat_tier_id
    ).first()

    if not tier:
        raise HTTPException(
            status_code=404,
            detail="Seat tier not found"
        )

    # Make sure tier belongs to requested show
    if tier.show_id != data.show_id:
        raise HTTPException(
            status_code=400,
            detail="Seat tier does not belong to this show"
        )

    # Check availability
    if tier.available_seats <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"{tier.name} seats are sold out"
        )

    if data.quantity > tier.available_seats:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Only {tier.available_seats} "
                f"{tier.name} seats are available"
            )
        )

    # Get pricing rules
    rules = db.query(PricingRules).first()

    if not rules:
        rules = PricingRules()
        db.add(rules)
        db.commit()
        db.refresh(rules)

    # Calculate complete bill
    bill = calculate_bill(
        ticket_price=tier.price,
        quantity=data.quantity,
        is_member=data.is_member,
        festival_discount=rules.festival_discount,
        member_discount_percent=rules.member_discount_percent,
        member_discount_cap=rules.member_discount_cap,
        convenience_fee_per_ticket=rules.convenience_fee_per_ticket,
        gst_percent=rules.gst_percent,
    )

    # Create booking
    booking = Booking(
        show_id=data.show_id,
        seat_tier_id=data.seat_tier_id,
        quantity=data.quantity,
        is_member=data.is_member,
    )

    # Reserve seats
    tier.available_seats -= data.quantity

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "booking_id": booking.id,
        "show_id": booking.show_id,
        "seat_tier": tier.name,
        "quantity": booking.quantity,
        "is_member": booking.is_member,
        "bill": bill,
    }


@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    tier = db.query(SeatTier).filter(
        SeatTier.id == booking.seat_tier_id
    ).first()

    return {
        "booking_id": booking.id,
        "show_id": booking.show_id,
        "seat_tier": tier.name if tier else None,
        "quantity": booking.quantity,
        "is_member": booking.is_member,
        "created_at": booking.created_at,
    }