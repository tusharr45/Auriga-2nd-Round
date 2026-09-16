from fastapi import FastAPI

from app.database import Base, engine
from app.models import (
    Cinema,
    Show,
    SeatTier,
    Booking,
    PricingRules,
)

from app.routes.cinemas import router as cinema_router
from app.routes.shows import router as show_router
from app.routes.bookings import router as booking_router
from app.routes.pricing import router as pricing_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Cinema Pricing Engine",
    description="Cinema ticket booking and pricing engine",
    version="1.0.0",
)


app.include_router(cinema_router)
app.include_router(show_router)
app.include_router(booking_router)
app.include_router(pricing_router)


@app.get("/")
def root():
    return {
        "message": "Cinema Pricing Engine API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }