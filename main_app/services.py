from models import User, Twit
from serializers import UserCreateSerializer, TwitCreateSerializer
import hashlib


class TwitService:
    async def create_twit(
        self,
        twit: TwitCreateSerializer,
        current_user: User,
    ):
        """ Creates and returns new twit instance. Authorization: Bearer $TOKEN header required! """
        new_twit = await Twit.create(
            text=twit.text,
            author=current_user,
        )
        return new_twit


class UserService:
    async def create_user(
        self,
        user: UserCreateSerializer,
    ):
        """ Creates and returns new user instance """
        new_user = await User.create(
            username=user.username,
            password=hashlib.sha256(user.password.encode()).hexdigest(),
        )
        return new_user

    async def login(
        self,
        user: UserCreateSerializer,
    ):
        """ Returns user if credentials are valid """
        logged_user = await User.filter(
            username=user.username,
            password=hashlib.sha256(user.password.encode()).hexdigest(),
        ).first()
        return logged_user

    async def get_user(
        self,
        **kwargs,
    ):
        """ Returns user instance by kwargs """
        return await User.filter(**kwargs).first()
