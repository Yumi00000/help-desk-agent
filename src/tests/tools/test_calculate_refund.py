import json
from datetime import datetime, timedelta

import pytest

from src.services import CalculateRefunds
from src.tools.calculate_refund import CalculateRefundTool

NOW = datetime.fromisoformat("2026-06-10T09:00:00+02:00")


def refund_for(hours_before_start: float, status: str = "confirmed") -> dict:
    booking = {
        "status": status,
        "start": (NOW + timedelta(hours=hours_before_start)).isoformat(),
        "rental_price_eur": 100.0,
        "booking_fee_eur": 2.0,
        "deposit_eur": 50.0,
    }
    return CalculateRefunds(booking).calculate(NOW)


class TestCalculateRefund:
    @pytest.mark.parametrize("hours_before_start, status, rental, deposit", [
        (72, "confirmed", 100.0, 50.0),   # 48h or more: 100%
        (48, "confirmed", 100.0, 50.0),
        (30, "confirmed", 50.0, 50.0),    # 24h to 48h: 50%
        (24, "confirmed", 50.0, 50.0),
        (10, "confirmed", 0.0, 50.0),     # less than 24h: 0%
        (72, "in_progress", 0.0, 0.0),    # cannot be cancelled: nothing
        (72, "completed", 0.0, 0.0),
        (72, "cancelled", 0.0, 0.0),
    ])
    def test_refund_rules(self, hours_before_start, status, rental, deposit):
        refund = refund_for(hours_before_start, status)
        assert refund["rental_refund_eur"] == rental
        assert refund["deposit_refund_eur"] == deposit
        assert refund["booking_fee_refund_eur"] == 0.0   # booking fee is never refunded
        assert refund["total_refund_eur"] == rental + deposit

    @pytest.mark.parametrize("days_from_now, total", [(0, 340.0), (1, 300.0)])
    def test_refund_tool(self, days_from_now, total):
        refund = json.loads(CalculateRefundTool().run({"booking_id": "CW-1002", "days_from_now": days_from_now}))
        assert refund["total_refund_eur"] == total

    def test_refund_tool_booking_not_found(self):
        assert "not found" in CalculateRefundTool().run({"booking_id": "CW-9999"})
