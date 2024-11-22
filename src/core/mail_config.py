import os
from pydantic_settings  import BaseSettings


class MailConfig(BaseSettings):
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")

    class Config:
        env_file = ".env"


mail_connection_config = MailConfig()