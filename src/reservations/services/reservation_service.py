from __future__ import annotations

from datetime import date as DateType, time as TimeType

from ..exceptions.reservation_errors import (
    InsufficientCapacityError,
    InvalidPartySizeError,
    MissingRequiredDataError,
)
from ..models.reservation import Reservation, ReservationStatus
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
        self._next_code = 1

    def create_reservation(
        self,
        customer_name: str,
        party_size: int,
        reservation_date: DateType,
        reservation_time: TimeType,
    ) -> Reservation:
        self._validate(customer_name, party_size, reservation_date, reservation_time)

        reservation = Reservation(
            code=self._generate_code(),
            customer_name=customer_name,
            party_size=party_size,
            date=reservation_date,
            time=reservation_time,
        )
        return self._repository.save(reservation)

    def _validate(
        self,
        customer_name: str,
        party_size: int,
        reservation_date: DateType | None,
        reservation_time: TimeType | None,
    ) -> None:
        if not customer_name or not customer_name.strip():
            raise MissingRequiredDataError(
                "El nombre del cliente es un dato obligatorio."
            )
        if reservation_date is None:
            raise MissingRequiredDataError("La fecha es un dato obligatorio.")
        if reservation_time is None:
            raise MissingRequiredDataError("La hora es un dato obligatorio.")
        if not isinstance(party_size, int) or party_size <= 0:
            raise InvalidPartySizeError(
                "El número de personas debe ser un entero mayor a cero."
            )
    
    def _occupied_capacity(
        self,
        reservation_date: DateType,
        reservation_time: TimeType,
    ) -> int:
        return sum(
            reservation.party_size
            for reservation in self._repository.find_by_date(reservation_date)
            if reservation.time == reservation_time
            and reservation.status == ReservationStatus.ACTIVE
        )

    def _generate_code(self) -> str:
        code = f"RES-{self._next_code:04d}"
        self._next_code += 1
        return code