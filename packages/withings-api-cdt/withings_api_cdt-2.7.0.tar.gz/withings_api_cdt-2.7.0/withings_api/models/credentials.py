from datetime import timedelta

import arrow
from pydantic import BaseModel


class Credentials(BaseModel):
    """Credentials."""

    access_token: str
    token_expiry: int
    token_type: str
    refresh_token: str
    userid: int
    client_id: str
    consumer_secret: str

    @property
    def expires_in(self) -> timedelta:
        return arrow.get(self.token_expiry) - arrow.utcnow()

    @property
    def is_expired(self):
        return self.expires_in.total_seconds() <= 0
