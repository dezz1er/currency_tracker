from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.user import UserRegistration, UserLogin 
from typing import Annotated

import app.auth.security as security
from app.auth.schemas import Session, SessionToRedis, Tokens, Payload
from app.auth.repository import add_session, get_session
from app.auth.dependencies import user_service_dep
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
def authentication(response: Response)    
