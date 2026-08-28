from datetime import date, time
import pytest

from reservations.services.reservation_service import ReservationService

@pytest.fixture
def service() -> ReservationService:
    return ReservationService(max_capacity=30)

class TestCheckAvailability:
    def test_returns_max_capacity_when_no_reservations(self, service):
        # When checking availability for a specific date and time with no prior reservations
        available = service.check_availability(date(2026, 9, 1), time(20, 0))
        
        # Then the total maximum capacity should be available
        assert available == 30

    def test_returns_remaining_capacity_with_existing_reservations(self, service):
        # Given an existing reservation for 10 people
        service.create_reservation("Ana", 10, date(2026, 9, 1), time(20, 0))
        
        # When checking availability for the same slot
        available = service.check_availability(date(2026, 9, 1), time(20, 0))
        
        # Then the remaining capacity should be 20
        assert available == 20

    def test_returns_zero_when_fully_booked(self, service):
        # Given reservations that fill the entire capacity
        service.create_reservation("Ana", 20, date(2026, 9, 1), time(20, 0))
        service.create_reservation("Luis", 10, date(2026, 9, 1), time(20, 0))
        
        # When checking availability for the same slot
        available = service.check_availability(date(2026, 9, 1), time(20, 0))
        
        # Then the availability should be 0
        assert available == 0

    def test_availability_is_independent_by_time_slot(self, service):
        # Given a reservation at 20:00
        service.create_reservation("Ana", 15, date(2026, 9, 1), time(20, 0))
        
        # When checking availability for 21:00 on the same date
        available = service.check_availability(date(2026, 9, 1), time(21, 0))
        
        # Then the availability at 21:00 should not be affected
        assert available == 30
