import json
from datetime import datetime

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from src.core.settings import DataSettings
from src.services import BookingLoader, CalculateRefunds


class CalculateRefundInput(BaseModel):
    booking_id: str = Field(description="Booking number, e.g. 'CW-1001'")


class CalculateRefundTool(BaseTool):
    name: str = "calculate_refund"
    description: str = "Calculate how much the customer gets back if they cancel a booking now: rental refund, deposit refund, booking fee refund and total, in EUR."
    args_schema: type[BaseModel] = CalculateRefundInput
    booking_loader: BookingLoader = BookingLoader(DataSettings())
    now: datetime = datetime.fromisoformat("2026-06-10T09:00:00+02:00")

    def _run(self, booking_id: str) -> str:
        booking = self.booking_loader.get_booking_by_id(booking_id)
        if booking is None:
            return f"Booking {booking_id} not found."
        refund = CalculateRefunds(booking).calculate(self.now)
        return json.dumps({"booking_id": booking_id, "status": booking["status"], **refund})
