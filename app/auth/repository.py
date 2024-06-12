import json

from aioredis import Redis
from app.log import logger
from app.core.config import settings
from .schemas import Session
from .db import get_redis


async def add_session(
        user: str,
        refresh_token: str,
        session: Session,
        cache: Redis = get_redis()):
    if await cache.hlen(user) > settings.USER_MAX_ACTIVE_SESSIONS:
        session = await cache.hgetall(user)
        for k in session.keys():
            await cache.hdel('refresh_tokens', k)
        await cache.delete(user)
        logger.debug(f'all sessions from user {user} been cleared')
    await cache.hset(user, refresh_token, session.model_dump_json())
    await cache.hset('refresh_tokens', refresh_token, user)
    logger.debug(f'Added session {refresh_token}')


async def get_user_sessions(
        user: str, cache: Redis = get_redis()) -> dict[str: Session]:
    sessions = await cache.hgetall(user)
    if sessions:
        for k, v in sessions.items():
            sessions[k] = Session(**json.loads(v))
    return sessions


async def get_session(refresh_token: str, cache: Redis = get_redis()) -> Session:
    user = await cache.hget('refresh_tokens', refresh_token)
    if user:
        session = await user.hget(user, refresh_token)
        if session:
            session = Session(**json.loads(session))
        return session
