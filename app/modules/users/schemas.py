from pydantic import BaseModel, EmailStr, Field
from typing import Optional



# ----------------------------- User Schemas ------------------
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=3, max_length=32)
    telegram_id: Optional[int] = None


class UserResponse(UserBase):
    id: int
    telegram_id: Optional[int] = None
    is_active: bool

    class Config:
        from_attributes = True


# token schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True



# ----------------------------- Telegram Bot User Schema ------------------
# class tbotUserCreate(BaseModel):
#     telegram_id: int
#     telegram_username: str

# class tbotUserResponse(tbotUserCreate):
#     id: int
#     telegram_id: int
#     email: Optional[EmailStr] = None
#     is_active: bool
#     telegram_username: Optional[str] = None
    
#     class Config:
#         from_attributes = True




