from datetime import date, time

import pytest

from reservations.exceptions.reservation_errors import (
    ReservationAlreadyCancelledError,
    ReservationNotFoundError,
)
from reservations.models.reservation import ReservationStatus
from reservations.services.reservation_service import ReservationService


@pytest.fixture
def service() -> ReservationService:
    return ReservationService()


class TestCancelReservation:
    def test_cancels_an_existing_reservation(self, service):
        reservation = service.create_reservation(
            "Juan Pérez", 2, date(2026, 9, 1), time(20, 0)
        )

        cancelled = service.cancel_reservation(reservation.code)

        assert cancelled.status == ReservationStatus.CANCELLED

    def test_rejects_cancellation_of_nonexistent_code(self, service):
        with pytest.raises(ReservationNotFoundError):
            service.cancel_reservation("RES-9999")

    def test_rejects_cancellation_of_already_cancelled_reservation(self, service):
        reservation = service.create_reservation(
            "Juan Pérez", 2, date(2026, 9, 1), time(20, 0)
        )
        service.cancel_reservation(reservation.code)

        with pytest.raises(ReservationAlreadyCancelledError):
            service.cancel_reservation(reservation.code)
