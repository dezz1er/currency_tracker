from sqlalchemy import select

from app.database.models import Users
from app.repositories.base_repository import Repository


class UserRepository(Repository):
    model = Users

    async def find_by_username(self, username: str) -> model:
        model = self.model
        stmt = await self.session.execute(
            select(model).where(model.username == username)
        )
        result: model = stmt.scalars().first()
        return result

    async def find_by_id(self, user_id: int) -> model:
        model = self.model
        stmt = await self.session.execute(
            select(model).where(model.get_primary_key() == user_id)
        )
        result: model = stmt.scalars().first()
        return result
