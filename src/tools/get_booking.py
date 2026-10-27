import json

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from src.core.settings import DataSettings
from src.services import BookingLoader


class GetBookingInput(BaseModel):
    booking_id: str = Field(description="Booking number, e.g. 'CW-1001'")


class GetBookingTool(BaseTool):
    name: str = "get_booking"
    description: str = "Get the details of one booking by its booking number: status, bike type, dates, prices and payment."
    args_schema: type[BaseModel] = GetBookingInput
    booking_loader: BookingLoader =BookingLoader(DataSettings())

    def _run(self, booking_id: str) -> str:
        booking = self.booking_loader.get_booking_by_id(booking_id)
        if booking is None:
            return json.dumps({"id": None, "error": f"Booking {booking_id} not found."})
        return json.dumps(booking)
