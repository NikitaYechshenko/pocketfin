from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db # Функция получения сессии БД
from app.modules.users import schemas, service
from app.core import security

router = APIRouter(prefix="/users", tags=["Users"])

# 1. РЕГИСТРАЦИЯ
@router.post("/register", response_model=schemas.UserResponse)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Просто передаем задачу в сервис
    return service.UserService.register_user(db=db, user_in=user_data)

# 2. ВХОД (LOGIN)
@router.post("/login", response_model=schemas.Token)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    # Вызываем сервис для проверки логина/пароля
    user = service.UserService.authenticate_user(db=db, user_in=user_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Если всё ок, генерируем токен
    access_token = security.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

# 3. Получение всех пользователей
@router.get("/", response_model=list[schemas.UserResponse])
def read_users(skip:int = 10, limit = 100, db:Session = Depends(get_db)):
    readed_users = service.UserService.get_all_users(db, skip = skip, limit = limit)
    return readed_users
    