import json
from datetime import datetime, timedelta

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from src.core.settings import DataSettings
from src.services import BookingLoader, CalculateRefunds


class CalculateRefundInput(BaseModel):
    booking_id: str = Field(description="Booking number, e.g. 'CW-1001'")
    days_from_now: int = Field(default=0, description="When the customer cancels, in days from now: 0 = now, 1 = tomorrow, 2 = in two days")


class CalculateRefundTool(BaseTool):
    name: str = "calculate_refund"
    description: str = "Calculate how much the customer gets back if they cancel a booking now or in a few days: rental refund, deposit refund, booking fee refund and total, in EUR."
    args_schema: type[BaseModel] = CalculateRefundInput
    booking_loader: BookingLoader = BookingLoader(DataSettings())
    now: datetime = datetime.fromisoformat("2026-06-10T09:00:00+02:00")

    def _run(self, booking_id: str, days_from_now: int = 0) -> str:
        booking = self.booking_loader.get_booking_by_id(booking_id)
        if booking is None:
            return f"Booking {booking_id} not found."
        if days_from_now < 0:
            return "days_from_now cannot be negative."
        cancel_at = self.now + timedelta(days=days_from_now)
        refund = CalculateRefunds(booking).calculate(cancel_at)
        return json.dumps({"booking_id": booking_id, "status": booking["status"], "cancel_at": cancel_at.isoformat(), **refund})
