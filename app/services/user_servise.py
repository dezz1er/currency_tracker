from app.utils.uow import IUnitOfWork
from app.schemas.user import UserRegistration, UserInDb


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user(
            self, user_id: int | None,
            username: str | None = None) -> UserInDb:
        if any(user_id, username):
            async with self.uow:
                if user_id:
                    user: UserInDb = \
                        await self.uow.users_repos.find_by_id(
                            user_id
                            )
                if username:
                    user: UserInDb = \
                        await self.uow.users_repos.find_by_username(
                            username
                            )
                if user:
                    return UserInDb.model_validate(user)
                raise Exception

    async def add_user(self, user_data: UserRegistration):
        async with self.uow:
            stmt = await self.uow.users_repos.add_one(user_data.model_dump())
            result = UserInDb.model_validate(stmt)
            await self.uow.commit()
            return result
