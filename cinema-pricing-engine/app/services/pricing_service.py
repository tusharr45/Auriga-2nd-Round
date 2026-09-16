from decimal import Decimal, ROUND_HALF_UP


TWO_PLACES = Decimal("0.01")


def money(value):
    return Decimal(str(value)).quantize(
        TWO_PLACES,
        rounding=ROUND_HALF_UP
    )


def calculate_bill(
    ticket_price,
    quantity,
    is_member,
    festival_discount,
    member_discount_percent,
    member_discount_cap,
    convenience_fee_per_ticket,
    gst_percent,
):
    ticket_price = Decimal(str(ticket_price))
    quantity = Decimal(str(quantity))

    festival_discount = Decimal(str(festival_discount))
    member_discount_percent = Decimal(str(member_discount_percent))
    member_discount_cap = Decimal(str(member_discount_cap))
    convenience_fee_per_ticket = Decimal(str(convenience_fee_per_ticket))
    gst_percent = Decimal(str(gst_percent))

    # 1. Base ticket amount
    base_amount = money(ticket_price * quantity)

    # 2. Flat festival discount
    festival_discount_applied = min(
        festival_discount,
        base_amount
    )

    # 3. Amount after festival discount
    after_festival = base_amount - festival_discount_applied

    # 4. Member discount
    member_discount_applied = Decimal("0.00")

    if is_member:
        calculated_member_discount = (
            after_festival * member_discount_percent / Decimal("100")
        )

        member_discount_applied = min(
            calculated_member_discount,
            member_discount_cap,
            after_festival
        )

    member_discount_applied = money(member_discount_applied)

    # 5. Subtotal after discounts
    subtotal = money(
        after_festival - member_discount_applied
    )

    # 6. Convenience fee
    convenience_fee = money(
        convenience_fee_per_ticket * quantity
    )

    # 7. GST is applied after discounts + convenience fee
    taxable_amount = money(
        subtotal + convenience_fee
    )

    gst = money(
        taxable_amount * gst_percent / Decimal("100")
    )

    # 8. Final total
    total = money(
        taxable_amount + gst
    )

    return {
        "base_amount": money(base_amount),
        "festival_discount": money(-festival_discount_applied),
        "member_discount": money(-member_discount_applied),
        "subtotal": subtotal,
        "convenience_fee": convenience_fee,
        "taxable_amount": taxable_amount,
        "gst": gst,
        "total": total,
    }