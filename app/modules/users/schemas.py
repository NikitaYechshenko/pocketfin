from typing import Optional
from fastapi_users import schemas

# 1. Schema for reading (response to frontend)
class UserRead(schemas.BaseUser[int]):
    # id, email, is_active, is_superuser, is_verified are already included
    pass

# 2. Schema for creation (registration)
class UserCreate(schemas.BaseUserCreate):
    # email, password, is_active, is_superuser, is_verified are already included
    pass

# 3. Schema for updates (profile editing)
class UserUpdate(schemas.BaseUserUpdate):
    pass