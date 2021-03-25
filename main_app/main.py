from typing import Optional
from fastapi import FastAPI
from views import router
from ext import create_app


app = create_app()