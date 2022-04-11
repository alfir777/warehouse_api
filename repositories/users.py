from typing import List, Optional

from core.security import hash_password
from db.users import users
from models.user import User, UserIn
from .base import BaseRepository


class UserRepository(BaseRepository):
    async def register(self, u: UserIn) -> User:
        user = User(
            login=u.login,
            type=u.type,
            password=hash_password(u.password),
            is_admin=False,
        )
        values = {**user.dict()}
        values.pop('id', None)
        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def update(self, id: int, u: UserIn) -> User:
        user = User(
            id=id,
            login=u.login,
            type=u.type,
            password=hash_password(u.password),
            is_admin=False,
        )
        values = {**user.dict()}
        values.pop('id', None)
        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return user

    async def get_by_login(self, login: str) -> Optional[User]:
        query = users.select().where(users.c.login == login)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)
