from fastapi import FastAPI
from views import router
from tortoise.contrib.fastapi import register_tortoise


def create_app():
    app = FastAPI()
    app.include_router(router)

    register_tortoise(
        app,
        db_url="sqlite://twitter.db",
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    return app