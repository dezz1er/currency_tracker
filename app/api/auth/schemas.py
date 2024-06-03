from pydantic import BaseModel, ConfigDict
from typing import Annotated
from datetime import datetime
from api.models.roles import Roles


class SessionCreate(BaseModel):
    refresh_token: str
    user_id: int
    fingerprint: str
    exp_at: Annotated[float, 'datetime.timestamp()']
    created_at: Annotated[float | datetime, 'datetime.timestamp(), datetime'] = datetime.now()


class Session(SessionCreate):
    session_id: str


class Payload(BaseModel):
    username: str
    role: Roles | str
    exp: float

    model_config = ConfigDict(from_attributes=True)


class Tokens(BaseModel):
    access_token: str | None = None
    refresh_token: str
