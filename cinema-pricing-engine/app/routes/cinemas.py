from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Cinema
from app.schemas import CinemaCreate, CinemaResponse


router = APIRouter(prefix="/cinemas", tags=["Cinemas"])


@router.post("/", response_model=CinemaResponse)
def create_cinema(
    data: CinemaCreate,
    db: Session = Depends(get_db)
):
    cinema = Cinema(name=data.name)

    db.add(cinema)
    db.commit()
    db.refresh(cinema)

    return cinema


@router.get("/", response_model=list[CinemaResponse])
def get_cinemas(db: Session = Depends(get_db)):
    return db.query(Cinema).all()