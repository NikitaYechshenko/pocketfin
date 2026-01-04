import logging
from fastapi import FastAPI
import uvicorn
from app.core.database import Base, engine

from app.modules.users import router as user


app = FastAPI()

app.include_router(user.router)
