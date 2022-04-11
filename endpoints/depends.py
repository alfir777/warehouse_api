from fastapi import Depends, HTTPException, status

from core.security import JWTBearer, decode_access_token
from db.base import database
from models.user import User
from repositories.users import UserRepository
from repositories.warehouses import WarehouseRepository


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_warehouse_repository() -> WarehouseRepository:
    return WarehouseRepository(database)


async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer())) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credentials are not valid')
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    login: str = payload.get('sub')
    if login is None:
        raise cred_exception
    user = await users.get_by_login(login=login)
    if user is None:
        raise cred_exception
    return user
