from decimal import Decimal

import pytest

from app.models.pricing import PricingConfig, TicketTier
from app.services.pricing_service import PricingError, calculate_booking_price


TIERS = {
    "Silver": TicketTier("Silver", Decimal("120"), 10),
    "Gold": TicketTier("Gold", Decimal("180"), 2),
    "Recliner": TicketTier("Recliner", Decimal("300"), 1),
}


def test_calculates_line_items_discounts_fee_gst_and_total():
    result = calculate_booking_price(
        {"Silver": 2, "Gold": 1},
        TIERS,
        PricingConfig(
            festival_discount=Decimal("50"),
            member_discount_percent=Decimal("10"),
            member_discount_cap=Decimal("30"),
            convenience_fee_per_ticket=Decimal("12.50"),
            gst_rate=Decimal("18"),
        ),
        is_member=True,
    )

    assert result.ticket_subtotal == Decimal("420.00")
    assert result.festival_discount == Decimal("50.00")
    assert result.member_discount == Decimal("30.00")
    assert result.discounted_subtotal == Decimal("340.00")
    assert result.convenience_fee == Decimal("37.50")
    assert result.gst == Decimal("67.95")
    assert result.total == Decimal("445.45")
    assert result.lines[0].subtotal == Decimal("240.00")


def test_member_discount_is_not_applied_to_non_member():
    result = calculate_booking_price(
        {"Silver": 1},
        TIERS,
        PricingConfig(member_discount_percent=Decimal("20")),
    )

    assert result.member_discount == Decimal("0.00")
    assert result.total == Decimal("120.00")


def test_rejects_sold_out_tier():
    with pytest.raises(PricingError, match="not enough Gold seats"):
        calculate_booking_price({"Gold": 3}, TIERS)


def test_rounds_each_money_result_to_paise():
    result = calculate_booking_price(
        {"Silver": 1},
        {"Silver": TicketTier("Silver", Decimal("99.999"), 1)},
        PricingConfig(gst_rate=Decimal("18.5")),
    )

    assert result.ticket_subtotal == Decimal("100.00")
    assert result.gst == Decimal("18.50")
    assert result.total == Decimal("118.50")