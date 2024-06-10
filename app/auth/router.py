from fastapi import (APIRouter, HTTPException,
                     Depends, Response, Request)
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.user import UserRegistration, UserLogin
from typing import Annotated

import app.auth.security as security
from app.auth.schemas import Session, SessionToRedis, Tokens, Payload
from app.auth.repository import add_session, get_session
from app.auth.dependencies import user_service_dep, fingerprint_dep
from app.log.logger import logger

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


async def check_user(
        userdata: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: user_service_dep):
    user: UserLogin = await user_service.get_user(userdata.username)
    if not user:
        raise HTTPException
    security.verify_password(userdata.password, user.password)
    return user.username


@router.post('/signin')
async def signin(userdata: UserRegistration, user_service: user_service_dep):
    userdata.password = security.hash_password(userdata.password)
    user = await user_service.create_user(userdata)
    return user


@router.post('/login')
async def authentication(response: Response,
                         fingerprint: fingerprint_dep,
                         user: Annotated[
                             str, 'username'
                             ] = Depends(check_user)):
    access_token: str = security.create_access_token(user)
    session_to_add: SessionToRedis = security.create_session(user, fingerprint)
    add_session(user, session_to_add.refresh_token, session_to_add.session)
    security.set_tokens_to_cookies(
        response,
        Tokens(
            access_token=access_token,
            refresh_token=session_to_add.refresh_token
        )
    )
    return Tokens(
        **{
            'access_token': access_token,
            'refresh_token': session_to_add.refresh_token
        }
    )


@router.post('/update')
async def update_tokens(request: Request, response: Response,
                        fingerprint: fingerprint_dep):
    tokens: Tokens = security.get_tokens_from_cookies(request)
    session: Session = get_session(tokens.refresh_token)
    if session:
        security.check_session(session, fingerprint=fingerprint)
        tokens: Tokens = await authentication(
            response, fingerprint, session.username)
        logger.debug('Tokens updated successfully!')
        return tokens
    else:
        raise HTTPException


@router.post('/authorize')
async def authorize(
        request: Request, response: Response, fingerprint: fingerprint_dep):
    tokens: Tokens = security.get_tokens_from_cookies(request)
    try:
        payload: Payload = security.check_access_token(tokens.access_token)
    except Exception:
        tokens = await update_tokens(request, response, fingerprint)
        payload: Payload = security.check_access_token(tokens.access_token)
    return Payload.model_validate(payload)
