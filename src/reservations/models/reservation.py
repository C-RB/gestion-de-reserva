from dataclasses import dataclass
from datetime import date, time
from enum import Enum


class ReservationStatus(Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"


@dataclass
class Reservation:
    code: str
    customer_name: str
    party_size: int
    date: date
    time: time
    status: ReservationStatus = ReservationStatus.ACTIVE

    @property
    def is_active(self) -> bool:
        return self.status == ReservationStatus.ACTIVE

    def cancel(self) -> None:
        self.status = ReservationStatus.CANCELLED
