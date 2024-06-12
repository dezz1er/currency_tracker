from app.utils.uow import IUnitOfWork
from app.api.schemas.user import UserRegistration, UserLogin


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user(
            self, user_id: int | None = None,
            username: str | None = None) -> UserLogin:
        if any((user_id, username)):
            async with self.uow:
                if user_id:
                    user = \
                        await self.uow.users_repos.find_by_id(
                            user_id
                            )
                if username:
                    user = \
                        await self.uow.users_repos.find_by_username(
                            username
                            )
                if user:
                    return UserLogin.model_validate(user)
                raise Exception

    async def add_user(self, user_data: UserRegistration):
        async with self.uow:
            stmt = await self.uow.users_repos.add_one(user_data.model_dump())
            result = stmt.to_read_model()
            await self.uow.commit()
            return result
