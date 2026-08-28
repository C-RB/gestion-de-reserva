from datetime import date, time

import pytest

from reservations.exceptions.reservation_errors import (
    InsufficientCapacityError,
    InvalidPartySizeError,
    MissingRequiredDataError,
)
from reservations.models.reservation import Reservation, ReservationStatus
from reservations.repositories.reservation_repository import (
    InMemoryReservationRepository,
)
from reservations.services.reservation_service import ReservationService


@pytest.fixture
def service() -> ReservationService:
    return ReservationService()


class TestCreateReservation:
    def test_creates_reservation_with_data_and_unique_code(self, service):
        reservation = service.create_reservation(
            "Juan Pérez", 2, date(2026, 9, 1), time(20, 0)
        )

        assert isinstance(reservation, Reservation)
        assert reservation.customer_name == "Juan Pérez"
        assert reservation.party_size == 2
        assert reservation.date == date(2026, 9, 1)
        assert reservation.time == time(20, 0)
        assert reservation.status == ReservationStatus.ACTIVE
        assert reservation.code

    def test_generates_unique_codes(self, service):
        first = service.create_reservation(
            "Ana", 2, date(2026, 9, 1), time(20, 0)
        )
        second = service.create_reservation(
            "Luis", 3, date(2026, 9, 2), time(21, 0)
        )

        assert first.code != second.code

    @pytest.mark.parametrize("customer_name", [None, "", "   "])
    def test_rejects_missing_customer_name(self, service, customer_name):
        with pytest.raises(MissingRequiredDataError):
            service.create_reservation(
                customer_name, 2, date(2026, 9, 1), time(20, 0)
            )

    def test_rejects_missing_date(self, service):
        with pytest.raises(MissingRequiredDataError):
            service.create_reservation(
                "Juan Pérez", 2, None, time(20, 0)
            )

    def test_rejects_missing_time(self, service):
        with pytest.raises(MissingRequiredDataError):
            service.create_reservation(
                "Juan Pérez", 2, date(2026, 9, 1), None
            )

    @pytest.mark.parametrize("party_size", [0, -1, -10])
    def test_rejects_non_positive_party_size(self, service, party_size):
        with pytest.raises(InvalidPartySizeError):
            service.create_reservation(
                "Juan Pérez", party_size, date(2026, 9, 1), time(20, 0)
            )