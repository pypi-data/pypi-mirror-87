from datetime import datetime
from enum import auto, IntEnum
from typing import cast, List, Literal, NamedTuple, Optional, Tuple

from arrow import Arrow
from autoname import AutoName
from pydantic import BaseModel, HttpUrl

from withings_api import str_or_raise
from withings_api.common import _flexible_tuple_of, arrow_or_none, enum_or_raise, str_or_none
from withings_api.models.response import ResponseBase


class NotifyAppli(IntEnum):
    """
    Data to notify_subscribe to.

    ref.
    http://developer.withings.com/oauth2/#section/Data-API/Start-using-Data-API
    2.e. Notification categories
    """

    WEIGHT = 1
    CIRCULATORY = 4
    ACTIVITY = 16
    SLEEP = 44
    USER = 46
    BED_IN = 50
    BED_OUT = 51
    INFLATION_DONE = 52

class NotifyConfigBase(BaseModel):
    appli: NotifyAppli
    callbackurl: HttpUrl
    comment: Optional[str]

class NotifyConfigList(NotifyConfigBase):
    """NotifyListProfile - notification configuration
    http://developer.withings.com/oauth2/#operation/notify-list
    """
    expires: Optional[datetime]


class NotifyListResponseBody(BaseModel):
    """ NotifyListResponse.
    http://developer.withings.com/oauth2/#operation/notify-list
    """

    profiles: List[NotifyConfigList]


class NotifyListResponse(ResponseBase):
    body: NotifyListResponseBody


class NotifyGetResponse(NotifyConfigBase):
    """NotifyGetResponse."""


class ActionType(AutoName):
    """
    http://developer.withings.com/oauth2/#section/Data-API/Start-using-Data-API
    """
    delete = auto()
    unlink = auto()
    update = auto()


class NotifyFormBase(BaseModel):
    """
    the form data notify webhook will be received
    """
    userid: int
    appli: NotifyAppli


class PeriodMixin(BaseModel):
    """
    attr for period notify webhook
    """
    startdate: datetime
    enddate: datetime


class InstantaneousMixin(BaseModel):
    """
    attr for instantaneous notify webhook
    """
    date: datetime


class SleepNotifyForm(PeriodMixin, NotifyFormBase):
    appli: Literal[NotifyAppli.SLEEP]


class UserEventNotifyForm(NotifyFormBase):
    appli: Literal[NotifyAppli.USER]
    action: ActionType


class SleepEventNotifyForm(InstantaneousMixin, NotifyFormBase):
    appli: Literal[NotifyAppli.BED_IN, NotifyAppli.BED_OUT, NotifyAppli.INFLATION_DONE]
    deviceid: str


class UnifiedNotifyWebhook(BaseModel):
    """  """
    userid: int
    appli: NotifyAppli

    # applies to user.metrics [1,2] users.activity[44]
    startdate: Optional[datetime]
    enddate: Optional[datetime]

    # applies to users.activity 12
    date: Optional[datetime]

    # applies to user.info
    action: Optional[ActionType]

    # applies to user.sleepevents
    deviceid: Optional[str]
