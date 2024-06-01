from abc import ABC, abstractmethod

from app.db import async_session_maker
from api.repositories import SessionsRepository, UserRepository


class IUnitOfWork(ABC):
    sessions_repos: SessionsRepository
    users_repos: UserRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def __aenter__(self):
        ...

    @abstractmethod
    def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        # repositories
        self.session_repos = SessionsRepository(self.session)
        self.users_repos = UserRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()
