from pydantic_settings import BaseSettings # NEW

class Settings(BaseSettings):
    database: str
    host: str
    db_username: str
    password: str
    port_id: str

    class Config:
        env_file = "/home/murani/Documents/home_folder/LPSS/app_main/.env"

settings = Settings()