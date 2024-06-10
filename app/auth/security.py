from secrets import token_hex

import jwt.exceptions
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from db import get_user
from app.api.schemas.user import User
import jwt

from typing import Annotated
from fastapi import Depends, HTTPException, status, Request, Response
from datetime import datetime, timedelta
from app.core.config import settings
from app.auth.schemas import Session, SessionToRedis, Tokens, Payload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    if not pwd_context.verify(plain_password, hashed_password):
        raise HTTPException
    return True


def get_fingerprint(request: Request):
    fingerprint = request.headers.get('user-agent')
    return fingerprint


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


def create_session(username: str, fingerprint: str):
    refresh_token = token_hex(8)
    session = Session(
        username=username,
        exp_at=(
            datetime.now() + timedelta(days=settings.REFRESH_EXP)
            ).timestamp(),
        fingerprint=fingerprint,
        created_at=datetime.now()
    )
    return SessionToRedis(refresh_token=refresh_token, session=session)


def set_tokens_to_cookies(response: Response, tokens: Tokens):
    response.set_cookie('access_token', tokens.access_token, httponly=True)
    response.set_cookie('refresh_token', tokens.access_token, httponly=True)
    return response


def get_tokens_from_cookies(request: Request):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        return Tokens(access_token=access_token, refresh_token=refresh_token)
    else:
        raise HTTPException


def check_session(session: Session, fingerprint: str):
    if session:
        if session.fingerprint != fingerprint:
            raise HTTPException
        if session.exp_at < datetime.now().timestamp():
            raise HTTPException
    return True


def check_access_token(access_token: str):
    if not access_token:
        raise HTTPException
    try:
        payload = jwt.decode(
            access_token, 
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM])
        return Payload.model_validate(payload)
    except jwt.exceptions.DecodeError:
        raise HTTPException
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException
