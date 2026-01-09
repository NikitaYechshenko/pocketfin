from fastapi import APIRouter
from app.modules.users.manager import auth_backend, fastapi_users
from app.modules.users.schemas import UserRead, UserCreate, UserUpdate

# Main router for the Users module
router = APIRouter()

# 1. Login / Logout / JWT
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# 2. Registration
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# 3. User management (/users/me, etc.)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)