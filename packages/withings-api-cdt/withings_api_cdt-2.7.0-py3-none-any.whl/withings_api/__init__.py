"""
Python library for the Withings Health API.

Withings Health API
<https://developer.health.withings.com/api>
"""
import datetime
from types import LambdaType
from typing import Any, Dict, Iterable, Optional, Union

import arrow
from requests_oauthlib import OAuth2Session
from typing_extensions import Final

from .common import (
    AuthScope,
    GetActivityField,
    GetSleepField,
    GetSleepSummaryField,
    HeartGetResponse,
    HeartListResponse,
    MeasureGetActivityResponse,
    MeasureGetMeasGroupCategory,
    MeasureGetMeasResponse,
    MeasureType,
    SleepGetResponse,
    SleepGetSummaryResponse,
    UserGetDeviceResponse,
    int_or_raise,
    new_heart_get_response,
    new_heart_list_response,
    new_measure_get_activity_response,
    new_measure_get_meas_response,
    new_sleep_get_response,
    new_sleep_get_summary_response,
    new_user_get_device_response,
    response_body_or_raise,
    str_or_raise,
)
from .models.credentials import Credentials
from .models.notify import NotifyAppli, NotifyGetResponse, \
    NotifyListResponseBody

DateType = Union[arrow.Arrow, datetime.date, datetime.datetime, int, str]
ParamsType = Dict[str, Union[str, int, bool]]


def update_params(
        params: ParamsType, name: str, current_value: Any, new_value: Any = None
) -> None:
    """Add a conditional param to a params dict."""
    if current_value is None:
        return

    if isinstance(new_value, LambdaType):
        params[name] = new_value(current_value)
    else:
        params[name] = new_value or current_value


class WithingsAuth:
    """Handles management of oauth2 authorization calls."""

    URL: Final = "https://account.withings.com"
    PATH_AUTHORIZE: Final = "oauth2_user/authorize2"
    PATH_TOKEN: Final = "oauth2/token"  # nosec

    def __init__(
            self,
            client_id: str,
            consumer_secret: str,
            callback_uri: str,
            scope: Iterable[AuthScope] = tuple(),
            mode: Optional[str] = None,
    ):
        """Initialize new object."""
        self._client_id: Final = client_id
        self._consumer_secret: Final = consumer_secret
        self._callback_uri: Final = callback_uri
        self._scope: Final = scope
        self._mode: Final = mode
        self._session: Final = OAuth2Session(
                self._client_id,
                redirect_uri=self._callback_uri,
                scope=",".join((scope.value for scope in self._scope)),
        )

    def get_authorize_url(self, state: Optional[str] = None) -> str:
        """Generate the authorize url."""
        url: Final = str(
                self._session.authorization_url("%s/%s" % (self.URL, self.PATH_AUTHORIZE), state=state)[
                    0
                ]
        )

        if self._mode:
            return url + "&mode=" + self._mode

        return url

    def get_credentials(self, code: str) -> Credentials:
        """Get the oauth credentials."""
        response = self._session.fetch_token(
                "%s/oauth2/token" % self.URL,
                code=code,
                client_secret=self._consumer_secret,
                include_client_id=True,
        )
        response['token_expiry'] = arrow.utcnow().timestamp + response.get("expires_in")

        return Credentials(client_id=self._client_id, consumer_secret=self._consumer_secret, **response)


