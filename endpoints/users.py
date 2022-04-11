from typing import List

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, status

from endpoints.depends import get_user_repository, get_current_user
from models.user import UserOut, UserIn, User
from repositories.users import UserRepository

router = APIRouter()


@router.get('/read', response_model=List[UserOut])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        skip: int = 0):
    return await users.get_all(limit=limit, skip=skip)


@router.post('/register', response_model=UserOut)
async def register(
        user: UserIn,
        users: UserRepository = Depends(get_user_repository)):
    try:
        return await users.register(u=user)
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user exists')


@router.put('/update', response_model=UserOut)
async def update_user(
        id: int,
        user: UserIn,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)):
    old_user = await users.get_by_id(id=id)
    if old_user is None or old_user.login != current_user.login:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return await users.update(id=id, u=user)
