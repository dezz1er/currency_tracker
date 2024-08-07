from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey
from app.api.schemas.user import UserInDb
from app.database.db import Base


class Roles(Base):
    __tablename__ = 'roles'

    role: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)


class Users(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(ForeignKey(Roles.role))

    @staticmethod
    def get_primary_key():
        return Users.user_id

    def to_read_model(self) -> UserInDb:
        return UserInDb(
            id=self.user_id,
            username=self.username,
            hashed_password=self.password,
            role=self.role
        )
