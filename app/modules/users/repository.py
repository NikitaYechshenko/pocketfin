from sqlalchemy.orm import Session
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate


class UserRepository:
    # Найти пользователя по email (нужно для проверки уникальности и логина)
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    # Backward-compatible alias (used by service layer)
    @staticmethod
    def get_by_email(db: Session, email: str):
        return UserRepository.get_user_by_email(db=db, email=email)

    # Создать пользователя (сохранить уже готовый объект)
    @staticmethod
    def create_user(db: Session, user_data: UserCreate, hashed_password: str):
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Обновляем объект, чтобы получить присвоенный ID
        return db_user

    # Backward-compatible alias (used by service layer)
    @staticmethod
    def create(db: Session, user_data: UserCreate, hashed_password: str):
        return UserRepository.create_user(
            db=db, user_data=user_data, hashed_password=hashed_password
        )
    
    # get ALL users
    @staticmethod
    def get_all_users(db: Session, skip: int, limit: int):
        return db.query(User).offset(skip).limit(limit).all()
