import sqlalchemy

from .base import metadata

warehouses = sqlalchemy.Table(
    'warehouses',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, index=True, unique=True, autoincrement=True),
    sqlalchemy.Column('product', sqlalchemy.String, unique=True),
    sqlalchemy.Column('amount', sqlalchemy.Integer),
)
