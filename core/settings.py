import os

from dotenv import load_dotenv
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

TESTING = False
if os.path.isfile('./.env'):
    load_dotenv('./.env')
else:
    exit('DO cp ./.env_template.py ./.env and set token!')
if os.environ['TESTING'] == 'True':
    TESTING = True
elif os.environ['TESTING'] == 'False':
    TESTING = False

if TESTING:
    DATABASE_URL_TESTING = os.environ['DATABASE_URL_TESTING']
    settings.database_url = DATABASE_URL_TESTING
