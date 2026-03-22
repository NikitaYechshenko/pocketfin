import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.modules.users.router import router as users_router
from app.modules.portfolio.router import router as portfolio_router
from app.modules.transactions.router import router as asset_router


# Application lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info("Starting Global Asset Tracker")
    yield
    logging.info("Shutting down Global Asset Tracker")


# Initialize FastAPI application
app = FastAPI(
    title="Global Asset Tracker",
    lifespan=lifespan,
    swagger_ui_parameters={'persistAuthorization': True},
)


# ===== CORS MIDDLEWARE =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== ROUTERS =====
app.include_router(users_router)
app.include_router(portfolio_router)
app.include_router(asset_router)


# ===== ROOT ENDPOINT =====

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Global Asset Tracker",
        "docs": "/docs"
    }
