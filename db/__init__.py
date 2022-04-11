from .base import metadata, engine
from .users import users
from .warehouses import warehouses

metadata.create_all(bind=engine)
