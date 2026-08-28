from datetime import date, time
import pytest

from reservations.services.reservation_service import ReservationService

@pytest.fixture
def service() -> ReservationService:
    return ReservationService(max_capacity=30)

class TestCheckAvailability:
    def test_returns_max_capacity_when_no_reservations(self, service):
        # Revisa para fecha y hora sin reservas anteriores
        available = service.check_availability(date(2026, 9, 1), time(20, 0))
        # Máximo debería estar disponible
        assert available == 30

    def test_returns_remaining_capacity_with_existing_reservations(self, service):
        # Entrega una reserva de 10 personas
        service.create_reservation("Ana", 10, date(2026, 9, 1), time(20, 0))
        # Revisa disponibilidad
        available = service.check_availability(date(2026, 9, 1), time(20, 0))
        # Debe entregar una disponibilad restante de 20
        assert available == 20

    def test_returns_zero_when_fully_booked(self, service):
        # Reservas que llenan la disponibilidad de tiempo
        service.create_reservation("Ana", 20, date(2026, 9, 1), time(20, 0))
        service.create_reservation("Luis", 10, date(2026, 9, 1), time(20, 0))
        # Revisa la disponibilidad
        available = service.check_availability(date(2026, 9, 1), time(20, 0))
        # No es posible la reserva
        assert available == 0

    def test_availability_is_independent_by_time_slot(self, service):
        # Una reserva a las 8
        service.create_reservation("Ana", 15, date(2026, 9, 1), time(20, 0))
        
        # Revisa reserva para las 9 del mismo día
        available = service.check_availability(date(2026, 9, 1), time(21, 0))
        
        # Disponibilidad de las 9 no se debe ver afectada
        assert available == 30
