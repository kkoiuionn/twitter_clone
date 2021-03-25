from fastapi import APIRouter, Depends, Header, Request
from models import Twit, User
from typing import List, Optional, Dict
from serializers import (
    TwitSerializer,
    UserSerializer,
    UserCreateSerializer,
    TwitCreateSerializer,
    UserLoginSerializer,
)
from services import UserService, TwitService

from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from fastapi_jwt_auth.exceptions import JWTDecodeError


class Config(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Config()


router = APIRouter(
    prefix="/api/v1",
    tags=["items"],
)


@router.get("/twits", response_model=List[TwitSerializer])
async def get_twits():
    """ Get all twits """
    return await TwitSerializer.from_queryset(Twit.all())


@router.post("/users", response_model=UserSerializer)
async def create_user(
    user: UserCreateSerializer,
    userService: UserService = Depends(),
):
    """ Create new user with new credentials """
    new_user = await userService.create_user(user)
    return await UserSerializer.from_tortoise_orm(new_user)


@router.get("/users/my", response_model=UserSerializer)
async def get_current_user(
    request: Request,
    authorization: AuthJWT = Depends(),
    Authorization: str = Header(None),
    userService: UserService = Depends(),
):
    """ Get current user by jwt token provided """
    try:
        current_username = authorization.get_jwt_subject()
        authorization.jwt_required()

        current_user = await userService.get_user(username=current_username)

        return UserSerializer.from_orm(current_user)
    except JWTDecodeError:
        return JSONResponse(
            {
                "status": "Error",
                "info": "Invalid or expired token",
            },
            status_code=400,
        )


@router.get("/users", response_model=List[UserSerializer])
async def get_users(username: Optional[str] = None):
    """ Get all users or find by username """
    if username:
        return await UserSerializer.from_queryset(
            User.filter(username__contains=username)
        )

    return await UserSerializer.from_queryset(User.all())


@router.post("/users/login", response_model=UserSerializer)
async def login_user(
    user: UserCreateSerializer,
    userService: UserService = Depends(),
    authorize: AuthJWT = Depends(),
):
    """ Get jwt access token with provided credentials """
    if await userService.login(user):
        access_token = authorize.create_access_token(subject=user.username)
        return {"access_token": access_token}
    return JSONResponse(
        {
            "status": "error",
            "info": "Invalid credentials",
        }
    )


@router.post("/twits", response_model=TwitSerializer)
async def create_twit(
    twit: TwitCreateSerializer,
    authorize: AuthJWT = Depends(),
    twitService: TwitService = Depends(),
    userService: UserService = Depends(),
    Authorization: str = Header(None),
):
    """ Creates new twit with author of jwt provided token """
    authorize.jwt_required()
    current_username = authorize.get_jwt_subject()
    current_user = await userService.get_user(username=current_username)

    new_twit = await twitService.create_twit(twit, current_user)

    return TwitSerializer.from_orm(new_twit)
