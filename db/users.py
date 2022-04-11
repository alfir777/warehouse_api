import sqlalchemy

from .base import metadata

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, index=True, unique=True, autoincrement=True),
    sqlalchemy.Column('type', sqlalchemy.Enum('buyers', 'sellers', name='UserTypeEnum'), default='buyers'),
    sqlalchemy.Column('login', sqlalchemy.String, unique=True),
    sqlalchemy.Column('password', sqlalchemy.String),
    sqlalchemy.Column('is_admin', sqlalchemy.Boolean, default=False),
)
