from pydantic import BaseModel, EmailStr
from roles import Roles


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegistration(UserLogin):
    role: Roles = Roles.guest.value


class User(BaseModel):
    id: str
    username: str
    role: str
    email: EmailStr


class UserInDb(User):
    hashed_password: str
