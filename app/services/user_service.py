
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import user_repository
from app.schemas import UserCreate, UserUpdate
from utils import hash_password


def get_user(db: Session, user_id: int):
    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return user_repository.get_users(db, skip=skip, limit=limit)


def create_user(db: Session, user_data: UserCreate):
    if user_repository.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )

    return user_repository.create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password),
        role=user_data.role,
    )


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user(db, user_id)
    user.username = user_data.username
    user.email = user_data.email
    user.password = hash_password(user_data.password)
    return user_repository.update_user(db, user)


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    user_repository.delete_user(db, user)
