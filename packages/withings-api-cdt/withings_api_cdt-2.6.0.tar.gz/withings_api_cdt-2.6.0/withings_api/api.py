from abc import abstractmethod
from typing import Any, Callable, cast, Dict, Iterable, Optional, Union

import arrow
from oauthlib.oauth2 import WebApplicationClient
from requests import Response
from requests_oauthlib import OAuth2Session
from typing_extensions import Final

from withings_api import Credentials, DateType, GetActivityField, GetSleepField, GetSleepSummaryField, HeartGetResponse, \
    HeartListResponse, int_or_raise, MeasureGetActivityResponse, \
    MeasureGetMeasGroupCategory, \
    MeasureGetMeasResponse, MeasureType, \
    new_heart_get_response, new_heart_list_response, new_measure_get_activity_response, \
    new_measure_get_meas_response, new_sleep_get_response, new_sleep_get_summary_response, new_user_get_device_response, \
    NotifyAppli, NotifyGetResponse, NotifyListResponseBody, ParamsType, response_body_or_raise, \
    SleepGetResponse, SleepGetSummaryResponse, str_or_raise, update_params, UserGetDeviceResponse, WithingsAuth


class AbstractWithingsApi:
    """Abstract class for customizing which requests module you want."""

    URL: Final = "https://wbsapi.withings.net"
    PATH_V2_USER: Final = "v2/user"
    PATH_V2_MEASURE: Final = "v2/measure"
    PATH_MEASURE: Final = "measure"
    PATH_V2_SLEEP: Final = "v2/sleep"
    PATH_NOTIFY: Final = "notify"
    PATH_V2_HEART: Final = "v2/heart"

    @abstractmethod
    def _request(
            self, path: str, params: Dict[str, Any], method: str = "GET"
    ) -> Response:
        """Fetch data from the Withings API."""

    def request(
            self, path: str, params: Dict[str, Any], method: str = "GET"
    ) -> Response:
        """Request a specific service."""
        return self._request(method=method, path=path, params=params)

    def request_the_body(
            self, path: str, params: Dict[str, Any], method: str = "GET"
    ) -> Dict[str, Any]:
        """Request a specific service."""
        return response_body_or_raise(
                self._request(method=method, path=path, params=params).json()
        )

    def user_get_device(self) -> UserGetDeviceResponse:
        """
        Get user device.

        Some data related to user profile are available through those services.
        """
        return new_user_get_device_response(
                self.request_the_body(path=self.PATH_V2_USER, params={"action": "getdevice"})
        )

    def measure_get_activity(
            self,
            startdateymd: Optional[DateType] = None,
            enddateymd: Optional[DateType] = None,
            offset: Optional[int] = None,
            data_fields: Optional[Iterable[GetActivityField]] = None,
            lastupdate: Optional[DateType] = None,
    ) -> MeasureGetActivityResponse:
        """Get user created activities."""
        params: Final[ParamsType] = {}

        update_params(
                params,
                "startdateymd",
                startdateymd,
                lambda val: arrow.get(val).format("YYYY-MM-DD"),
        )
        update_params(
                params,
                "enddateymd",
                enddateymd,
                lambda val: arrow.get(val).format("YYYY-MM-DD"),
        )
        update_params(params, "offset", offset)
        update_params(
                params,
                "data_fields",
                data_fields,
                lambda fields: ",".join([field.value for field in fields]),
        )
        update_params(
                params, "lastupdate", lastupdate, lambda val: arrow.get(val).timestamp
        )
        update_params(params, "action", "getactivity")

        return new_measure_get_activity_response(
                self.request_the_body(path=self.PATH_V2_MEASURE, params=params)
        )

    def measure_get_meas(
            self,
            meastype: Optional[MeasureType] = None,
            category: Optional[MeasureGetMeasGroupCategory] = None,
            startdate: Optional[DateType] = None,
            enddate: Optional[DateType] = None,
            offset: Optional[int] = None,
            lastupdate: Optional[DateType] = None,
    ) -> MeasureGetMeasResponse:
        """Get measures."""
        params: Final[ParamsType] = {}

        update_params(params, "meastype", meastype, lambda val: val.value)
        update_params(params, "category", category, lambda val: val.value)
        update_params(
                params, "startdate", startdate, lambda val: arrow.get(val).timestamp
        )
        update_params(params, "enddate", enddate, lambda val: arrow.get(val).timestamp)
        update_params(params, "offset", offset)
        update_params(
                params, "lastupdate", lastupdate, lambda val: arrow.get(val).timestamp
        )
        update_params(params, "action", "getmeas")

        return new_measure_get_meas_response(
                self.request_the_body(path=self.PATH_MEASURE, params=params)
        )

    def sleep_get(
            self,
            startdate: Optional[DateType] = None,
            enddate: Optional[DateType] = None,
            data_fields: Optional[Iterable[GetSleepField]] = None,
    ) -> SleepGetResponse:
        """Get sleep data."""
        params: Final[ParamsType] = {}

        update_params(
                params, "startdate", startdate, lambda val: arrow.get(val).timestamp
        )
        update_params(params, "enddate", enddate, lambda val: arrow.get(val).timestamp)
        update_params(
                params,
                "data_fields",
                data_fields,
                lambda fields: ",".join([field.value for field in fields]),
        )
        update_params(params, "action", "get")

        return new_sleep_get_response(
                self.request_the_body(path=self.PATH_V2_SLEEP, params=params)
        )

    def sleep_get_summary(
            self,
            startdateymd: Optional[DateType] = None,
            enddateymd: Optional[DateType] = None,
            data_fields: Optional[Iterable[GetSleepSummaryField]] = None,
            offset: Optional[int] = None,
            lastupdate: Optional[DateType] = None,
    ) -> SleepGetSummaryResponse:
        """Get sleep summary."""
        params: Final[ParamsType] = {}

        update_params(
                params,
                "startdateymd",
                startdateymd,
                lambda val: arrow.get(val).format("YYYY-MM-DD"),
        )
        update_params(
                params,
                "enddateymd",
                enddateymd,
                lambda val: arrow.get(val).format("YYYY-MM-DD"),
        )
        update_params(
                params,
                "data_fields",
                data_fields,
                lambda fields: ",".join([field.value for field in fields]),
        )
        update_params(params, "offset", offset)
        update_params(
                params, "lastupdate", lastupdate, lambda val: arrow.get(val).timestamp
        )
        update_params(params, "action", "getsummary")

        return new_sleep_get_summary_response(
                self.request_the_body(path=self.PATH_V2_SLEEP, params=params)
        )

    def heart_get(self, signalid: int) -> HeartGetResponse:
        """Get ECG recording."""
        params: Final[ParamsType] = {}

        update_params(params, "signalid", signalid)
        update_params(params, "action", "get")

        return new_heart_get_response(
                self.request_the_body(path=self.PATH_V2_HEART, params=params)
        )

    def heart_list(
            self,
            startdate: Optional[DateType] = None,
            enddate: Optional[DateType] = None,
            offset: Optional[int] = None,
    ) -> HeartListResponse:
        """Get heart list."""
        params: Final[ParamsType] = {}

        update_params(
                params, "startdate", startdate, lambda val: arrow.get(val).timestamp,
        )
        update_params(
                params, "enddate", enddate, lambda val: arrow.get(val).timestamp,
        )
        update_params(params, "offset", offset)
        update_params(params, "action", "list")

        return new_heart_list_response(
                self.request_the_body(path=self.PATH_V2_HEART, params=params)
        )

    def notify_get(
            self, callbackurl: str, appli: Optional[NotifyAppli] = None
    ) -> NotifyGetResponse:
        """
        Get subscription.

        Return the last notification service that a user was subscribed to,
        and its expiry date.
        """
        params: Final[ParamsType] = {}

        update_params(params, "callbackurl", callbackurl)
        update_params(params, "appli", appli, lambda appli: appli.value)
        update_params(params, "action", "get")

        body = self.request_the_body(path=self.PATH_NOTIFY, params=params)
        return NotifyGetResponse(
                **body
        )

    def notify_list(self, appli: Optional[NotifyAppli] = None) -> NotifyListResponseBody:
        """List notification configuration for this user."""
        params: Final[ParamsType] = {}

        update_params(params, "appli", appli, lambda appli: appli.value)
        update_params(params, "action", "list")

        resp = self.request(path=self.PATH_NOTIFY, params=params)
        return NotifyListResponseBody.parse_raw(
                resp.content
        )

    def notify_revoke(
            self, callbackurl: Optional[str] = None, appli: Optional[NotifyAppli] = None
    ) -> None:
        """
        Revoke a subscription.

        This service disables the notification between the API and the
        specified applications for the user.
        """
        params: Final[ParamsType] = {}

        update_params(params, "callbackurl", callbackurl)
        update_params(params, "appli", appli, lambda appli: appli.value)
        update_params(params, "action", "revoke")

        self.request_the_body(path=self.PATH_NOTIFY, params=params)

    def notify_subscribe(
            self,
            callbackurl: str,
            appli: Optional[NotifyAppli] = None,
            comment: Optional[str] = None,
    ) -> None:
        """Subscribe to receive notifications when new data is available."""
        params: Final[ParamsType] = {}

        update_params(params, "callbackurl", callbackurl)
        update_params(params, "appli", appli, lambda appli: appli.value)
        update_params(params, "comment", comment)
        update_params(params, "action", "subscribe")

        self.request_the_body(path=self.PATH_NOTIFY, params=params)

    def notify_update(
            self,
            callbackurl: str,
            appli: NotifyAppli,
            new_callbackurl: str,
            new_appli: Optional[NotifyAppli] = None,
            comment: Optional[str] = None,
    ) -> None:
        """Update the callbackurl and or appli of a created notification."""
        params: Final[ParamsType] = {}

        update_params(params, "callbackurl", callbackurl)
        update_params(params, "appli", appli, lambda appli: appli.value)
        update_params(params, "new_callbackurl", new_callbackurl)
        update_params(params, "new_appli", new_appli, lambda new_appli: new_appli.value)
        update_params(params, "comment", comment)
        update_params(params, "action", "update")

        self.request_the_body(path=self.PATH_NOTIFY, params=params)


class WithingsApi(AbstractWithingsApi):
    """
    Provides entrypoint for calling the withings api.

    While withings-api takes care of automatically refreshing the OAuth2
    token so you can seamlessly continue making API calls, it is important
    that you persist the updated tokens somewhere associated with the user,
    such as a database table. That way when your application restarts it will
    have the updated tokens to start with. Pass a ``refresh_cb`` function to
    the API constructor and we will call it with the updated token when it gets
    refreshed.

    class WithingsUser:
        def refresh_cb(self, creds):
            my_savefn(creds)

    user = ...
    creds = ...
    api = WithingsApi(creds, refresh_cb=user.refresh_cb)
    """

    def __init__(
            self,
            credentials: Credentials,
            refresh_cb: Optional[Callable[[Credentials], None]] = None,
    ):
        """Initialize new object."""
        self.credentials = credentials
        self._refresh_cb: Final = refresh_cb
        token: Final = {
            "access_token": credentials.access_token,
            "refresh_token": credentials.refresh_token,
            "token_type": credentials.token_type,
            "expires_in": str(int(credentials.token_expiry) - arrow.utcnow().timestamp),
        }

        self._client: Final = OAuth2Session(
                credentials.client_id,
                token=token,
                client=WebApplicationClient(  # nosec
                        credentials.client_id, token=token, default_token_placement="query"
                ),
                auto_refresh_url="%s/%s" % (WithingsAuth.URL, WithingsAuth.PATH_TOKEN),
                auto_refresh_kwargs={
                    "action": "requesttoken",
                    "client_id": credentials.client_id,
                    "client_secret": credentials.consumer_secret,
                },
                token_updater=self._update_token,
        )

    def get_credentials(self) -> Credentials:
        """Get the current oauth credentials."""
        return self.credentials

    def refresh_token(self) -> None:
        """Manually refresh the token."""
        token_dict: Final = self._client.refresh_token(
                token_url=self._client.auto_refresh_url
        )
        self._update_token(token=token_dict)

    def _update_token(self, token: Dict[str, Union[str, int]]) -> None:
        """Set the oauth token."""
        self.credentials = Credentials(
                access_token=str_or_raise(token.get("access_token")),
                token_expiry=arrow.utcnow().timestamp
                             + int_or_raise(token.get("expires_in")),
                token_type=self.credentials.token_type,
                refresh_token=str_or_raise(token.get("refresh_token")),
                userid=self.credentials.userid,
                client_id=self.credentials.client_id,
                consumer_secret=self.credentials.consumer_secret,
        )

        if self._refresh_cb:
            self._refresh_cb(self.credentials)

    def _request(
            self, path: str, params: Dict[str, Any], method: str = "GET"
    ) -> Response:
        return self._client.request(
                        method=method,
                        url="%s/%s" % (self.URL.strip("/"), path.strip("/")),
                        params=params,
                )

    @property
    def token_expired(self):
        return self.credentials.is_expired