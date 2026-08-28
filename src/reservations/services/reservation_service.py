from __future__ import annotations

from datetime import date as DateType, time as TimeType

from ..exceptions.reservation_errors import (
    InsufficientCapacityError,
    InvalidPartySizeError,
    MissingRequiredDataError,
    ReservationAlreadyCancelledError,
    ReservationNotFoundError,
)
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
        self._next_code = 1

    def create_reservation(
        self,
        customer_name: str,
        party_size: int,
        reservation_date: DateType,
        reservation_time: TimeType,
    ) -> Reservation:
        self._validate(customer_name, party_size, reservation_date, reservation_time)
        self.check_availability(reservation_date, reservation_time, party_size)

        reservation = Reservation(
            code=self._generate_code(),
            customer_name=customer_name,
            party_size=party_size,
            date=reservation_date,
            time=reservation_time,
        )
        return self._repository.save(reservation)

    def check_availability(
        self,
        reservation_date: DateType,
        reservation_time: TimeType,
        party_size: int = 0,
    ) -> int:
        available = self._max_capacity - self._occupied_capacity(
            reservation_date, reservation_time
        )
        if party_size > available:
            raise InsufficientCapacityError(
                "No hay disponibilidad para la fecha y hora solicitada."
            )
        return available

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

    def _ensure_availability(
        self,
        party_size: int,
        reservation_date: DateType,
        reservation_time: TimeType,
    ) -> None:
        available = self.check_availability(reservation_date, reservation_time)

        if party_size > available:
            raise InsufficientCapacityError(
                "No hay disponibilidad para la fecha y hora solicitada."
            )

    def _occupied_capacity(
        self,
        reservation_date: DateType,
        reservation_time: TimeType,
    ) -> int:
        return sum(
            reservation.party_size
            for reservation in self.list_reservations_by_date(reservation_date)
            if reservation.time == reservation_time
        )

    def cancel_reservation(self, code: str) -> Reservation:
        reservation = self._get_reservation_or_raise(code)
        if not reservation.is_active:
            raise ReservationAlreadyCancelledError(
                f"La reserva '{code}' ya se encuentra cancelada."
            )
        reservation.cancel()
        return reservation

    def list_reservations_by_date(
        self,
        reservation_date: DateType,
        include_cancelled: bool = False,
    ) -> list[Reservation]:
        reservations = [
            reservation
            for reservation in self._repository.find_by_date(reservation_date)
            if include_cancelled or reservation.is_active
        ]
        return sorted(reservations, key=lambda reservation: reservation.time)

    def _get_reservation_or_raise(self, code: str) -> Reservation:
        reservation = self._repository.find(code)
        if reservation is None:
            raise ReservationNotFoundError(
                f"No existe una reserva con el código '{code}'."
            )
        return reservation

    def _generate_code(self) -> str:
        code = f"RES-{self._next_code:04d}"
        self._next_code += 1
        return code