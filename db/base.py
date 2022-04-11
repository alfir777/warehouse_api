from databases import Database
from sqlalchemy import create_engine, MetaData

from core.settings import settings

database = Database(settings.database_url)
metadata = MetaData()
engine = create_engine(
    settings.database_url
)
