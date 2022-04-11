from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = 'postgresql://user:password@postgresserver/db'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITM: str = 'HS256'
    SECRET_KEY: str = 'fc4a048fd80768b1c7b8eb941b84eb58e8f451818fc3c7429bfcc2e5f61b9473'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
