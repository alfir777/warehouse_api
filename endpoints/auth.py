import logging

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import verify_password, create_access_token
from endpoints.depends import get_user_repository
from models.token import Token, Login
from repositories.users import UserRepository

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/', response_model=Token)
async def login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_login(login.login)
    if user is None or not verify_password(login.password, user.password):
        logger.info(f"{login.login} - incorrect username or password")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect username or password')
    logger.info(f"log in {user.login} ")
    return Token(
        access_token=create_access_token({'sub': user.login}),
        token_type='Bearer'
    )
