import os
from pydantic_settings  import BaseSettings

class DBConfig(BaseSettings):
    DB_URL: str = os.getenv("DB_URL")
    DB_NAME: str = os.getenv("DB_NAME")

    class Config:
        env_file = ".env"

db_config = DBConfig()


