from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from db import get_user
from api.models.user import User
import jwt

from typing import Annotated
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(user: User):
    exp = (datetime.now() + timedelta(
        minutes=settings.ACCESS_EXP)).timestamp() - 55
    encode_data = {
        'username': user.username,
        'role': user.role.value,
        'exp': exp
    }
    encoded_jwt = jwt.encode(
        encode_data,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(username)
    if user is None:
        raise credential_exception
    return user
