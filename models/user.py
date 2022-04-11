from typing import Optional

from pydantic import BaseModel, validator
from pydantic.types import Enum


class UserTypeEnum(str, Enum):
    buyers = 'buyers'
    sellers = 'sellers'


class User(BaseModel):
    id: Optional[str] = None
    type: UserTypeEnum
    login: str
    password: str
    is_admin: bool


class UserIn(BaseModel):
    login: str
    type: UserTypeEnum
    password: str
    password2: str

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError("password don't match")
        return v


class UserOut(BaseModel):
    id: Optional[str] = None
    type: UserTypeEnum
    login: str
