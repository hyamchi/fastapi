from pydantic import BaseSettings

class Settings(BaseSettings):
    database_servername: str
    database_driver: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    database_username: str
    database_password: str 
       
    class Config:
        env_file = ".env"

settings = Settings()