from __future__ import annotations

from datetime import date

from ..models.reservation import Reservation


class InMemoryReservationRepository:
    def __init__(self) -> None:
        self._reservations: dict[str, Reservation] = {}

    def save(self, reservation: Reservation) -> Reservation:
        raise NotImplementedError

    def find(self, code: str) -> Reservation | None:
        raise NotImplementedError

    def find_by_date(self, date: date) -> list[Reservation]:
        raise NotImplementedError