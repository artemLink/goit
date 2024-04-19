from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = ("postgresql+async://postgres://1111@localhost:5432/contactbook")
    SECRET_KEY_JWT: str = "secret"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = "username"
    MAIL_PASSWORD: str = "password"
    MAIL_FROM: str = "example@example.com"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "localhost"
    REDIS_DOMAIN: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = "dir0ipjit"
    CLD_API_KEY: int = 331623919883923
    CLD_API_SECRET: str = "secret"

    @field_validator("ALGORITHM")
    def validate_algorithm(cls, v):
        if v not in ["HS256", "HS512"]:
            raise ValueError("Invalid algorithm")
        return v

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()
