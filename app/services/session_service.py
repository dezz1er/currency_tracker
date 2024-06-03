import aioredis
from datetime import datetime
import json


class SessionService:
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def add_session(
            self,
            user_id: int,
            refresh_token: str,
            fingerprint: str,
            exp_at: float,
            created_at: datetime) -> dict:
        session_id = str(user_id) + ':' + refresh_token
        session_data = {
            "user_id": user_id,
            "refresh_token": refresh_token,
            "fingerprint": fingerprint,
            "exp_at": exp_at,
            "created_at": created_at
        }
        user_sessions = await self.get_user_sessions(user_id)

        if len(user_sessions >= 5):
            print(f'user {user_id} sessions have been deleted')
            await self.clear_user_sessions(user_id)

        await self.redis.set(
            session_id,
            json.dumps(session_data),
            expire=int(exp_at - datetime.now().timestamp())
        )
        return session_data

    async def get_session(self, session_id: str) -> dict:
        session_data = await self.redis.get(session_id)
        if session_data:
            return json.loads(session_data)
        return None

    async def get_user_sessions(self, user_id: int) -> list:
        keys = await self.redis.keys(f"{user_id}:*")
        sessions = []
        for key in keys:
            sessions_data = await self.redis.get(key)
            if sessions_data:
                sessions.append(json.loads(sessions_data))
        return sessions

    async def clear_user_sessions(self, user_id: int):
        keys = await self.redis.keys(f"{user_id}:*")
        if keys:
            await self.redis.delete(*keys)
