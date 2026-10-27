import json

import pytest

from src.core.settings import DataSettings
from src.services import BookingLoader
from src.tools.get_booking import GetBookingTool


def get_booking(booking_id: str, booking_tool: GetBookingTool = GetBookingTool()) -> dict:
    return json.loads(booking_tool.run(booking_id))


class TestBookingCalls:
    @pytest.mark.parametrize("booking_id", ["CW-1001", "CW-1005", "CW-1010"])
    def test_booking_exists(self, booking_id):
        assert get_booking(booking_id)["id"] == booking_id

    def test_booking_details(self):
        booking = get_booking("CW-1004")
        assert booking["status"] == "confirmed"
        assert booking["paid_with"] == "voucher"
        assert booking["add_ons"] == ["child_seat"]

    @pytest.mark.parametrize("booking_id", ["CW-9999", "", "abc"])
    def test_booking_not_found(self, booking_id):
        booking = get_booking(booking_id)
        assert booking["id"] is None
        assert "not found" in booking["error"]

    @pytest.mark.parametrize("booking_id", ["cw-1002", " CW-1002 "])
    def test_booking_id_is_normalized(self, booking_id):
        assert get_booking(booking_id)["id"] == "CW-1002"

    def test_missing_bookings_file(self, tmp_path):
        data_settings = DataSettings()
        data_settings.BOOKINGS_PATH = tmp_path / "missing.json"
        booking = get_booking("CW-1002", GetBookingTool(booking_loader=BookingLoader(data_settings)))
        assert booking["id"] is None
        assert "not available" in booking["error"]

    def test_tool_definition(self):
        booking_tool = GetBookingTool()
        assert booking_tool.name == "get_booking"
        assert list(booking_tool.args) == ["booking_id"]
