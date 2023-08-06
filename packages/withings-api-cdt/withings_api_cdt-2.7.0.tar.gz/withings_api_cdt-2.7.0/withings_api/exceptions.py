from typing import Any


class StatusException(Exception):
    """Status exception."""

    def __init__(self, status: Any):
        """Create instance."""
        super().__init__("Error code %s" % str(status))


class AuthFailedException(StatusException):
    """Withings status error code exception."""


class InvalidParamsException(StatusException):
    """Withings status error code exception."""


class UnauthorizedException(StatusException):
    """Withings status error code exception."""


class ErrorOccurredException(StatusException):
    """Withings status error code exception."""


class TimeoutException(StatusException):
    """Withings status error code exception."""


class BadStateException(StatusException):
    """Withings status error code exception."""


class TooManyRequestsException(StatusException):
    """Withings status error code exception."""


class UnknownStatusException(StatusException):
    """Unknown status code but it's still not successful."""