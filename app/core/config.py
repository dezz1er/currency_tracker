from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_KEY: str
    APP_NAME: str
    ADMIN_EMAIL: str

    SECRET_KEY: str
    ALGORITHM: str

    REFRESH_EXP: int
    ACCESS_EXP: int

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    TEST_DB_NAME: str
    DB_DRIVER_SYNC: str
    DB_DRIVER_ASYNC: str

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_AUTH_DB: int = 0
    USER_MAX_ACTIVE_SESSIONS: int = 5

    @property
    def ASYNC_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def TEST_DATABASE_URL(self):
        return (
            f"postgresql://{self.DB_USER}:"
            f"{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
