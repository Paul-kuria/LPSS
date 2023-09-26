import os

from pydantic_settings import BaseSettings  # NEW

base_path = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    database: str
    host: str
    db_username: str
    password: str
    port_id: str

    class Config:
        env_file = os.path.join(base_path, ".env")


settings = Settings()
