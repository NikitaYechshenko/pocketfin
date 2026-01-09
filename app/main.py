import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.users.schemas import UserRead, UserCreate, UserUpdate
from app.modules.users.manager import auth_backend, fastapi_users
from app.modules.portfolio.router import router as portfolio_router
from app.modules.asset.router import router as asset_router
from app.modules.users.router import router as users_router

app = FastAPI(title="Asset Tracker",
              swagger_ui_parameters={'persistAuthorization': True},)

# CORS (Required for frontend!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === FASTAPI USERS ROUTERS ===

# Connect all user-related routes (auth, register, users) in one line
app.include_router(users_router)

# Connect portfolios
app.include_router(portfolio_router)

# Connect assets
app.include_router(asset_router)