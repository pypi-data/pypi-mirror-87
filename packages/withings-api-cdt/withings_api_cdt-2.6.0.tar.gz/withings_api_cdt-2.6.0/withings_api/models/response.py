from typing import Any, Dict, Optional

from pydantic import BaseModel, validator

from withings_api.const import STATUS_AUTH_FAILED, STATUS_BAD_STATE, STATUS_ERROR_OCCURRED, STATUS_INVALID_PARAMS, \
    STATUS_SUCCESS, \
    STATUS_TIMEOUT, STATUS_TOO_MANY_REQUESTS, STATUS_UNAUTHORIZED
from withings_api.exceptions import AuthFailedException, BadStateException, ErrorOccurredException, \
    InvalidParamsException, \
    TimeoutException, TooManyRequestsException, UnauthorizedException, \
    UnknownStatusException


def raise_status_error(status: Optional[int]):
    if status is None:
        raise UnknownStatusException(status=status)
    elif status in STATUS_SUCCESS:
        return
    elif status in STATUS_AUTH_FAILED:
        raise AuthFailedException(status=status)
    elif status in STATUS_INVALID_PARAMS:
        raise InvalidParamsException(status=status)
    elif status in STATUS_UNAUTHORIZED:
        raise UnauthorizedException(status=status)
    elif status in STATUS_ERROR_OCCURRED:
        raise ErrorOccurredException(status=status)
    elif status in STATUS_TIMEOUT:
        raise TimeoutException(status=status)
    elif status in STATUS_BAD_STATE:
        raise BadStateException(status=status)
    elif status in STATUS_TOO_MANY_REQUESTS:
        raise TooManyRequestsException(status=status)
    else:
        raise UnknownStatusException(status=status)


class ResponseBase(BaseModel):
    status: Optional[int] = None
    body: Dict[str, Any]
