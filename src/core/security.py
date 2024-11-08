import os
from pydantic_settings  import BaseSettings


class SecurityConfig(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30 days

    class Config:
        env_file = ".env"


security_config = SecurityConfig()