from __future__ import annotations

from datetime import date as DateType

from ..models.reservation import Reservation


class InMemoryReservationRepository:
    def __init__(self) -> None:
        self._reservations: dict[str, Reservation] = {}

    def save(self, reservation: Reservation) -> Reservation:
        self._reservations[reservation.code] = reservation
        return reservation

    def find(self, code: str) -> Reservation | None:
        return self._reservations.get(code)

    def find_by_date(self, reservation_date: DateType) -> list[Reservation]:
        return [
            reservation
            for reservation in self._reservations.values()
            if reservation.date == reservation_date
        ]