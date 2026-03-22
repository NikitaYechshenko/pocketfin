from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.main import logging

from app.core.database import get_async_session
from app.modules.users import models, schemas, security, deps

router = APIRouter(prefix="/auth", tags=["Auth"])

# 1. Registration
@router.post("/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_async_session)):
    # Check if email already exists
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = await security.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password, telegram_id=user.telegram_id)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# 2. Login (get JWT)
@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    # Find user
    result = await db.execute(select(models.User).where(models.User.email == form_data.username))
    user = result.scalars().first()

    # Verify password
    if not user or not await security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate token
    access_token = await security.create_access_token(data={"sub": user.email})
    logging.info(f"User {access_token} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}

# 3. Get "Me" (Protected route)
@router.get("/me", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    return current_user





# # 4 handles both login and registration
# @router.post("/tbot/", status_code=status.HTTP_200_OK)
# async def auth_tbot(user: schemas.tbotUserCreate, db: AsyncSession = Depends(get_async_session)):
    
#     # 1. LOGIN STEP: Проверяем, есть ли юзер
#     result = await db.execute(select(models.User).where(models.User.telegram_id == user.telegram_id))
#     db_user = result.scalars().first()
    
#     if db_user:
#         # Юзер найден, идем дальше к генерации токена
#         logging.info(f"Telegram user {db_user.telegram_id} authenticated successfully")
        
#     else:
#         # 2. REGISTRATION STEP: Если нет, создаем
#         new_user = models.User(
#             email=f"{user.telegram_id}@t.me", 
#             hashed_password=str(user.telegram_id), 
#             telegram_id=user.telegram_id,
#             telegram_username=user.telegram_username,
#         )
#         db.add(new_user)
        
#         try:
#             await db.commit()
#             await db.refresh(new_user)
#             db_user = new_user # Переназначаем переменную для шага 3
#             logging.info(f"New Telegram user {db_user.telegram_id} created successfully")
            
#         except IntegrityError:
#             await db.rollback()
#             logging.warning(f"Race condition detected: user {user.telegram_id} was already created in another thread.")
            
#             result = await db.execute(select(models.User).where(models.User.telegram_id == user.telegram_id))
#             db_user = result.scalars().first()
            
#     # 3. JWT token generation step (Теперь он выполняется ВСЕГДА)
#     access_token = await security.create_access_token(data={"sub": db_user.email})
#     logging.info(f"Telegram user {db_user.telegram_id} gets token {access_token}")

#     # 4. return token and user data
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "id": db_user.id,
#         "telegram_id": db_user.telegram_id,
#         "email": db_user.email,
#         "is_active": db_user.is_active
#     }