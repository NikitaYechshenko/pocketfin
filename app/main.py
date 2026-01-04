import logging
from fastapi import FastAPI
import uvicorn
from app.modules.users import router as user
from app.core.database import Base, engine
logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(user.router)

Base.metadata.create_all(bind=engine)
