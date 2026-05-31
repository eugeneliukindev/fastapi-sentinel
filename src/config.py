from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_DIR = Path(__file__).resolve().parent.parent


class _DatabaseSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    driver: Annotated[str, Field(default="postgresql+asyncpg", alias="drivername", frozen=True)]
    username: str
    password: SecretStr
    host: str = "localhost"
    port: int = 5432
    name: Annotated[str, Field(alias="database")]

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.driver,
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="MY_APP__",
        env_file=[
            BASE_DIR / ".env.example",
            BASE_DIR / ".env",
        ],
    )

    db: _DatabaseSettings


settings = Settings()
