from __future__ import annotations

from datetime import date, time

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
        date: date,
        time: time,
    ) -> Reservation:
        self._validate(customer_name, party_size, date, time)
        self._ensure_availability(party_size, date, time)

        reservation = Reservation(
            code=self._generate_code(),
            customer_name=customer_name,
            party_size=party_size,
            date=date,
            time=time,
        )
        return self._repository.save(reservation)

    def _validate(
        self,
        customer_name: str,
        party_size: int,
        date: date,
        time: time,
    ) -> None:
        if not customer_name or not customer_name.strip():
            raise MissingRequiredDataError(
                "El nombre del cliente es un dato obligatorio."
            )
        if date is None:
            raise MissingRequiredDataError("La fecha es un dato obligatorio.")
        if time is None:
            raise MissingRequiredDataError("La hora es un dato obligatorio.")
        if not isinstance(party_size, int) or party_size <= 0:
            raise InvalidPartySizeError(
                "El número de personas debe ser un entero mayor a cero."
            )

    def _ensure_availability(
        self,
        party_size: int,
        date: date,
        time: time,
    ) -> None:
        occupied = sum(
            reservation.party_size
            for reservation in self._repository.find_by_date(date)
            if reservation.time == time
            and reservation.status == ReservationStatus.ACTIVE
        )
        if occupied + party_size > self._max_capacity:
            raise InsufficientCapacityError(
                "No hay disponibilidad para la fecha y hora solicitada."
            )

    def _generate_code(self) -> str:
        code = f"RES-{self._next_code:04d}"
        self._next_code += 1
        return code