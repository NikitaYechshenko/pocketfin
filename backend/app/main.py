import logging
from fastapi import FastAPI
import uvicorn
from backend.app.routers import user
from backend.app.core.database_sqlalchemy import Base, engine
logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(user.router)

Base.metadata.create_all(bind=engine)
