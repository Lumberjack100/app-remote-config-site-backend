import os
from typing import Optional

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # 数据库配置
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql://postgres:postgres@localhost:5432/remote_config"
    )

    # JWT配置
    SECRET_KEY: str = Field(
        default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30240)  # 3周

    # 默认用户配置
    DEFAULT_USER_ACCOUNT: str = Field(default="medo_gh")
    DEFAULT_USER_PASSWORD: str = Field(default="medo123456")
    DEFAULT_USER_NAME: str = Field(default="宫贺")
    DEFAULT_USER_COMPANY_ID: int = Field(default=138)
    DEFAULT_USER_COMPANY_NAME: str = Field(default="上海米度测控科技有限公司")

    @field_validator("DATABASE_URL", mode="before")
    def validate_database_url(cls, v: Optional[str]) -> str:
        return v or os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/remote_config")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings() 