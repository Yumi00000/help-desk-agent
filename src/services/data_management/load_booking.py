import json

from src.core.settings import DataSettings


class BookingLoader:
    def __init__(self, data_settings: DataSettings):
        self.booking_path = data_settings.BOOKINGS_PATH

    def load_bookings(self):
        with open(self.booking_path, "r") as f:
            return json.load(f)

    def get_booking_by_id(self, booking_id: str):
        bookings = self.load_bookings()
        return next((booking for booking in bookings if booking["id"] == booking_id), None)

    def get_bookings_status(self, booking_id: str):
        booking = self.get_booking_by_id(booking_id)
        return booking["status"] if booking else None
