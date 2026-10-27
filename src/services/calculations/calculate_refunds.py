from datetime import datetime


class CalculateRefunds:
    def __init__(self, booking: dict):
        self.booking = booking

    def calculate(self, now: datetime) -> dict[str, float]:
        if self.booking["status"] != "confirmed":
            return self._result(hours_before_start=0.0, refund_percent=0.0, deposit_refund=0.0)

        start = datetime.fromisoformat(self.booking["start"])
        hours_before_start = (start - now).total_seconds() / 3600

        if hours_before_start >= 48:
            refund_percent = 100.0
        elif hours_before_start >= 24:
            refund_percent = 50.0
        else:
            refund_percent = 0.0

        return self._result(hours_before_start, refund_percent, deposit_refund=self.booking["deposit_eur"])

    def _result(self, hours_before_start: float, refund_percent: float, deposit_refund: float) -> dict[str, float]:
        rental_refund = round(self.booking["rental_price_eur"] * refund_percent / 100, 2)
        return {
            "hours_before_start": round(hours_before_start, 2),
            "refund_percent": refund_percent,
            "rental_refund_eur": rental_refund,
            "deposit_refund_eur": deposit_refund,
            "booking_fee_refund_eur": 0.0,
            "total_refund_eur": round(rental_refund + deposit_refund, 2),
        }
