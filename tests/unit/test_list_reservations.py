from datetime import date, time

import pytest

from reservations.services.reservation_service import ReservationService


@pytest.fixture
def service() -> ReservationService:
    return ReservationService()


class TestListReservationsByDate:
    def test_returns_reservations_of_the_requested_date(self, service):
        # Dos reservas para la misma fecha en horarios distintos
        first = service.create_reservation("Ana", 4, date(2026, 9, 1), time(20, 0))
        second = service.create_reservation("Luis", 2, date(2026, 9, 1), time(21, 0))

        reservations = service.list_reservations_by_date(date(2026, 9, 1))

        # Ambas deben aparecer en el listado de esa fecha
        assert [r.code for r in reservations] == [first.code, second.code]

    def test_returns_empty_list_when_there_are_no_reservations(self, service):
        # Fecha sin ninguna reserva registrada
        reservations = service.list_reservations_by_date(date(2026, 9, 1))

        assert reservations == []

    def test_excludes_reservations_of_other_dates(self, service):
        # Una reserva por fecha, en dos fechas distintas
        expected = service.create_reservation("Ana", 4, date(2026, 9, 1), time(20, 0))
        service.create_reservation("Luis", 2, date(2026, 9, 2), time(20, 0))

        reservations = service.list_reservations_by_date(date(2026, 9, 1))

        # Solo la reserva del 1 de septiembre
        assert [r.code for r in reservations] == [expected.code]

    def test_excludes_cancelled_reservations_by_default(self, service):
        # Se cancela una de las dos reservas de la fecha
        active = service.create_reservation("Ana", 4, date(2026, 9, 1), time(20, 0))
        cancelled = service.create_reservation("Luis", 2, date(2026, 9, 1), time(21, 0))
        service.cancel_reservation(cancelled.code)

        reservations = service.list_reservations_by_date(date(2026, 9, 1))

        # Por defecto la reserva cancelada no se informa
        assert [r.code for r in reservations] == [active.code]

    def test_includes_cancelled_reservations_when_requested(self, service):
        # Misma situación, pero pidiendo explícitamente las canceladas
        active = service.create_reservation("Ana", 4, date(2026, 9, 1), time(20, 0))
        cancelled = service.create_reservation("Luis", 2, date(2026, 9, 1), time(21, 0))
        service.cancel_reservation(cancelled.code)

        reservations = service.list_reservations_by_date(
            date(2026, 9, 1), include_cancelled=True
        )

        # Se informan ambas y la cancelada queda identificada por su estado
        assert [r.code for r in reservations] == [active.code, cancelled.code]

    def test_returns_reservations_ordered_by_time(self, service):
        # Las reservas se registran en desorden respecto del horario
        late = service.create_reservation("Ana", 4, date(2026, 9, 1), time(22, 0))
        early = service.create_reservation("Luis", 2, date(2026, 9, 1), time(20, 0))

        reservations = service.list_reservations_by_date(date(2026, 9, 1))

        # El listado debe quedar ordenado cronológicamente
        assert [r.code for r in reservations] == [early.code, late.code]
