from datetime import date, time
import pytest

from reservations.services.reservation_service import ReservationService

@pytest.fixture
def service() -> ReservationService:
    return ReservationService(max_capacity=30)

class TestCheckAvailability:
    def test_returns_max_capacity_when_no_reservations(self, service):
        available = service.check_availability(date(2026, 9, 1), time(20, 0))
        
        assert available == 30

    def test_returns_remaining_capacity_with_existing_reservations(self, service):
        service.create_reservation("Ana", 10, date(2026, 9, 1), time(20, 0))
        
        available = service.check_availability(date(2026, 9, 1), time(20, 0))
        
        assert available == 20

    def test_returns_zero_when_fully_booked(self, service):
        service.create_reservation("Ana", 20, date(2026, 9, 1), time(20, 0))
        service.create_reservation("Luis", 10, date(2026, 9, 1), time(20, 0))
        
        available = service.check_availability(date(2026, 9, 1), time(20, 0))
        
        assert available == 0

    def test_availability_is_independent_by_time_slot(self, service):
        service.create_reservation("Ana", 15, date(2026, 9, 1), time(20, 0))
        
        available = service.check_availability(date(2026, 9, 1), time(21, 0))
        
        assert available == 30
