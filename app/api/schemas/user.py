from pydantic import BaseModel, ConfigDict
from .roles import Roles


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserRegistration(UserLogin):
    role: str = Roles.user.value


class User(BaseModel):
    id: int
    username: str
    role: str


class UserInDb(User):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
