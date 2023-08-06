"""Aiohwenergy errors."""


class AiohwenergyException(Exception):
    """Base error for aiohwenergy."""


class RequestError(AiohwenergyException):
    """Unable to fulfill request.

    Raised when host or API cannot be reached.
    """

class Unauthorized(AiohwenergyException):
    """Application is not authorized."""


class InvalidState(AiohwenergyException):
    """Raised when the device is not in the correct state to handle the request."""


ERRORS = {
    1: Unauthorized,
    2: Unauthorized,
    3: Unauthorized,
    10: RequestError,
    11: RequestError,
    12: RequestError,
    13: RequestError,
    14: RequestError,
    15: RequestError,
    16: InvalidState,
}


def raise_error(code, message):
    cls = ERRORS.get(code, AiohwenergyException)
    raise cls("{}: {}".format(code, message))