from __future__ import annotations

from datetime import date, time

from ..models.reservation import Reservation
from ..repositories.reservation_repository import InMemoryReservationRepository

DEFAULT_MAX_CAPACITY = 30


class ReservationService:
    def __init__(
        self,
        repository: InMemoryReservationRepository | None = None,
        max_capacity: int = DEFAULT_MAX_CAPACITY,
    ) -> None:
        self._repository = repository or InMemoryReservationRepository()
        self._max_capacity = max_capacity

    def create_reservation(
        self,
        customer_name: str,
        party_size: int,
        date: date,
        time: time,
    ) -> Reservation:
        raise NotImplementedError