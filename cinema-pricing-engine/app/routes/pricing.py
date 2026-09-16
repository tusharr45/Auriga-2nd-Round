from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PricingRules
from app.schemas import PricingRulesCreate


router = APIRouter(
    prefix="/pricing",
    tags=["Pricing"]
)


@router.get("/")
def get_pricing_rules(
    db: Session = Depends(get_db)
):
    rules = db.query(PricingRules).first()

    if not rules:
        rules = PricingRules()
        db.add(rules)
        db.commit()
        db.refresh(rules)

    return rules


@router.put("/")
def update_pricing_rules(
    data: PricingRulesCreate,
    db: Session = Depends(get_db)
):
    rules = db.query(PricingRules).first()

    if not rules:
        rules = PricingRules()
        db.add(rules)

    rules.festival_discount = data.festival_discount
    rules.member_discount_percent = data.member_discount_percent
    rules.member_discount_cap = data.member_discount_cap
    rules.convenience_fee_per_ticket = data.convenience_fee_per_ticket
    rules.gst_percent = data.gst_percent

    db.commit()
    db.refresh(rules)

    return rules