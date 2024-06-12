from aioredis import Redis, ConnectionPool
from app.core.config import settings


async def create_redis_pool():
    return await ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_AUTH_DB,
        decode_responses=True
    )


pool = create_redis_pool()


def get_redis() -> Redis:
    return Redis(connection_pool=pool)
