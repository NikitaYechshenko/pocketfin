from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.users import repository, schemas, models
from app.core import security

class UserService:
    
    # ЛОГИКА РЕГИСТРАЦИИ
    @staticmethod
    def register_user(db: Session, user_in: schemas.UserCreate):
        # 1. Проверяем, не занят ли email
        existing_user = repository.UserRepository.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # 2. Хэшируем пароль
        hashed_pw = security.get_password_hash(user_in.password)
        
        # 3. Сохраняем через репозиторий
        return repository.UserRepository.create(db, user_in, hashed_pw)

    # ЛОГИКА ВХОДА (АУТЕНТИФИКАЦИЯ)
    @staticmethod
    def authenticate_user(db: Session, user_in: schemas.UserLogin):
        # 1. Ищем юзера
        user = repository.UserRepository.get_by_email(db, email=user_in.email)
        
        # 2. Если юзера нет ИЛИ пароль не подошел -> ошибка
        if not user or not security.verify_password(user_in.password, user.hashed_password):
            return None # Логин не удался
            
        return user # Логин успешен
    # Логика получения всех пользователей
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return repository.UserRepository.get_all_users(db, skip=skip, limit=limit)