from datetime import datetime

from pydantic import BaseModel, EmailStr

# Базовая схема (общие поля)
class UserBase(BaseModel):
    email: EmailStr

# Схема для РЕГИСТРАЦИИ (клиент шлет пароль)
class UserCreate(UserBase):
    password: str

# Схема для ВХОДА (клиент шлет email и пароль)
class UserLogin(UserBase):
    password: str

# Схема для ОТВЕТА (мы НЕ возвращаем пароль, возвращаем id и активность)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Чтобы Pydantic читал данные из SQLAlchemy моделей

# Схема для ТОКЕНА (то, что мы вернем после успешного входа)
class Token(BaseModel):
    access_token: str
    token_type: str