from typing import Optional
from fastapi_users import schemas

# 1. Схема для чтения (то, что отдаем фронту)
class UserRead(schemas.BaseUser[int]):
    # id, email, is_active, is_superuser, is_verified уже включены
    pass

# 2. Схема для создания (регистрация)
class UserCreate(schemas.BaseUserCreate):
    # email, password, is_active, is_superuser, is_verified уже включены
    pass

# 3. Схема для обновления (редактирование профиля)
class UserUpdate(schemas.BaseUserUpdate):
    pass