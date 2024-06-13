from typing import Annotated
from fastapi import Depends
from app.services.user_servise import UserService
from app.utils.uow import UnitOfWork, IUnitOfWork
from redis import Redis
from app.auth.db import get_redis
from app.auth import security

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


def get_user_service(uow: UOWDep) -> UserService:
    return UserService(uow)


user_service_dep = Annotated[UserService, Depends(get_user_service)]
fingerprint_dep = Annotated[str, Depends(security.get_fingerprint)]
redis_dep = Annotated[Redis, Depends(get_redis)]
