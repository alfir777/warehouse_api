from fastapi import APIRouter, Depends, HTTPException, status

from core.security import verify_password, create_access_token
from endpoints.depends import get_user_repository
from models.token import Token, Login
from repositories.users import UserRepository

router = APIRouter()


@router.post('/', response_model=Token)
async def login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_login(login.login)
    if user is None or not verify_password(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    return Token(
        access_token=create_access_token({'sub': user.login}),
        token_type='Bearer'
    )