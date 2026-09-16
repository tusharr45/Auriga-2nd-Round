from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Cinema, Show, SeatTier
from app.schemas import (
    ShowCreate,
    ShowResponse,
    SeatTierCreate,
    SeatTierResponse,
)


router = APIRouter(prefix="/shows", tags=["Shows"])


@router.post("/", response_model=ShowResponse)
def create_show(
    data: ShowCreate,
    db: Session = Depends(get_db)
):
    cinema = db.query(Cinema).filter(
        Cinema.id == data.cinema_id
    ).first()

    if not cinema:
        raise HTTPException(
            status_code=404,
            detail="Cinema not found"
        )

    show = Show(
        cinema_id=data.cinema_id,
        movie_name=data.movie_name,
        show_time=data.show_time,
    )

    db.add(show)
    db.commit()
    db.refresh(show)

    return show


@router.get("/", response_model=list[ShowResponse])
def get_shows(db: Session = Depends(get_db)):
    return db.query(Show).all()


@router.post(
    "/tiers",
    response_model=SeatTierResponse
)
def create_seat_tier(
    data: SeatTierCreate,
    db: Session = Depends(get_db)
):
    show = db.query(Show).filter(
        Show.id == data.show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )

    tier = SeatTier(
        show_id=data.show_id,
        name=data.name,
        price=data.price,
        total_seats=data.total_seats,
        available_seats=data.total_seats,
    )

    db.add(tier)
    db.commit()
    db.refresh(tier)

    return tier


@router.get(
    "/{show_id}/tiers",
    response_model=list[SeatTierResponse]
)
def get_show_tiers(
    show_id: int,
    db: Session = Depends(get_db)
):
    show = db.query(Show).filter(
        Show.id == show_id
    ).first()

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )

    return db.query(SeatTier).filter(
        SeatTier.show_id == show_id
    ).all()