class ReservationError(Exception):
    """Base exception for all reservation domain errors."""


class MissingRequiredDataError(ReservationError):
    """Raised when a required reservation field is missing."""


class InvalidPartySizeError(ReservationError):
    """Raised when the number of people is less than or equal to zero."""


class InsufficientCapacityError(ReservationError):
    """Raised when there is no availability for the requested date and time."""


class ReservationNotFoundError(ReservationError):
    """Raised when a reservation code does not exist."""


class ReservationAlreadyCancelledError(ReservationError):
    """Raised when trying to cancel a reservation that is already cancelled."""