"""Authentication Models."""
from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import BaseModel, Field


def utc_now():
    return datetime.now(timezone.utc)


class OAuth2TokenResponse(BaseModel):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: str
    issued: datetime = Field(default_factory=utc_now)

    def is_valid(self) -> bool:
        return (self.issued + timedelta(seconds=self.expires_in)) > utc_now()