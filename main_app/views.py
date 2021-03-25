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
    return await TwitSerializer.from_queryset(Twit.all())


@router.post("/users", response_model=UserSerializer)
async def create_user(
    user: UserCreateSerializer,
    userService: UserService = Depends(),
):
    new_user = await userService.create_user(user)
    return await UserSerializer.from_tortoise_orm(new_user)


@router.get("/users/my")
async def get_current_user(
    request: Request,
    authorization: AuthJWT = Depends(),
    Authorization: str = Header(None),
):
    authorization.jwt_required()

    current_user = authorization.get_jwt_subject()
    current_user = await User.filter(username=current_user).first()

    return await UserSerializer.from_queryset_single(current_user)


@router.get("/users", response_model=List[UserSerializer])
async def get_users(username: Optional[str] = None):
    if username:
        return await UserSerializer.from_queryset(
            User.filter(username__contains=username)
        )

    return await UserSerializer.from_queryset(User.all())


@router.post("/users/login")
async def login_user(
    user: UserCreateSerializer,
    userService: UserService = Depends(),
    authorize: AuthJWT = Depends(),
):
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
    Authorization: str = Header(
        "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTYxNjU5NTg0NywibmJmIjoxNjE2NTk1ODQ3LCJqdGkiOiI2OWE1N2NkYi1jY2JjLTRlYTMtOTA0Zi1hMTNlMjUxOGNjNzIiLCJleHAiOjE2MTY1OTY3NDcsInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6ZmFsc2V9.OANnrTBuNfcpjYj7-Mt1_wJEJLaOtY43lqUhFhd4UCk"
    ),
):
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    print(current_user)

    new_twit = await twitService.create_twit(twit, current_user)

    return TwitSerializer.from_orm(new_twit)
