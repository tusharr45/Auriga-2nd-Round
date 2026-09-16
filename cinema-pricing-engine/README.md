# Cinema Pricing Engine
A FastAPI-based cinema ticket booking and pricing engine.
The application manages cinemas, shows, seat tiers, bookings, and configurable pricing rules. It calculates the final ticket amount by applying discounts, convenience fees, and GST.

## Features

- Create and manage cinemas
- Create movie shows
- Configure seat tiers such as Silver, Gold, and Recliner
- Configure seat prices and availability
- Book multiple seats
- Prevent booking more seats than available
- Prevent booking a seat tier belonging to another show
- Festival discount support
- Member percentage discount with a configurable cap
- Per-ticket convenience fee
- GST calculation
- Decimal-based monetary calculations
- Automatic seat availability update after booking
- REST API with Swagger documentation
- SQLite database using SQLAlchemy

---

## Tech Stack

- Python 3
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- SQLite
- Swagger / OpenAPI

---

## Project Structure
cinema-pricing-engine/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cinema.py
│   │   ├── show.py
│   │   ├── seat_tier.py
│   │   ├── booking.py
│   │   └── pricing.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── cinemas.py
│   │   ├── shows.py
│   │   ├── bookings.py
│   │   └── pricing.py
│   │
│   └── services/
│       └── pricing_service.py
│
├── cinema.db
├── requirements.txt
├── README.md
├── REASONING.md
└── AI_LOGS.md