from pydantic import BaseModel, ConfigDict
from typing import Annotated
from datetime import datetime
from app.api.schemas.roles import Roles


class Session(BaseModel):
    username: str
    fingerprint: str
    exp_at: Annotated[float, 'datetime.timestamp()']
    created_at: Annotated[
        float | datetime,
        'datetime.timestamp(), datetime'
    ] = datetime.now()

    model_config = ConfigDict(from_attributes=True)


class Payload(BaseModel):
    username: str
    role: Roles | str
    exp: float

    model_config = ConfigDict(from_attributes=True)


class Tokens(BaseModel):
    access_token: str | None = None
    refresh_token: str


class SessionToRedis(BaseModel):
    refresh_token: str
    session: Session
