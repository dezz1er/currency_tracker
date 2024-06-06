from typing import Annotated
from fastapi import Depends
from app.services.user_servise import UserService
from app.utils.uow import UnitOfWork, IUnitOfWork
from aioredis import Redis
from app.auth.db import get_redis


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


def get_user_service(uow: UOWDep) -> UserService:
    return UserService(uow)


user_service_dep = Annotated[UserService, Depends(get_user_service)]
redis_dep = Annotated[Redis, Depends(get_redis)]
