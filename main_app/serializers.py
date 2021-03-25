from tortoise.contrib.pydantic import pydantic_model_creator
from models import Twit, User


TwitSerializer = pydantic_model_creator(Twit, name="Twit")
TwitCreateSerializer = pydantic_model_creator(
    Twit,
    name="TwitCreate",
    exclude_readonly=True,
    exclude=("date_posted", "date_updated"),
)

UserSerializer = pydantic_model_creator(
    User,
    name="User",
    exclude=("password",),
)
UserCreateSerializer = pydantic_model_creator(
    User,
    name="UserCreate",
    exclude_readonly=True,
)
UserLoginSerializer = pydantic_model_creator(
    User,
    name="UserLogin",
)
