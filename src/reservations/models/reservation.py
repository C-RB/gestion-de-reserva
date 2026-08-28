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