from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DB_URL: str = Field(default="postgresql+asyncpg://workout:workout@localhost:5432/workout")


settings = Settings()
