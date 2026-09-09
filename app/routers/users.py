
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import get_db
from app.models import User
from schemas import UserCreate, UserResponse, UserUpdate
from typing import List, cast
from utils import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token
from utils import verify_password
from schemas import Token
from auth import get_current_user, require_admin

router = APIRouter()

# def get_current_user():
#     return "max"

# @router.get("/me")
# def get_me(
#     current_user: User = Depends(get_current_user)
# ):
#     return current_user
@router.get("/profile")
def get_profile(
    current_user : str = Depends(get_current_user)
):
    return {
        "logged_in_user" : current_user
    }


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
    db.query(User)
    .filter(User.email == form_data.username)
    .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, cast(str, user.password)
        ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data={"sub": user.email})

    return {
    "access_token": access_token,
    "token_type": "bearer"}



# @router.get("/")
# def get_users():
#     return[
#         {"username":"john"},
#         {"username":"rohit"}
#     ]

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit : int = 10,
    db: Session = Depends(get_db)
):
    # users = db.query(User).all()
    users = (
    db.query(User)
    .offset(skip)
    .limit(limit)
    .all()
)

    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id:int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.post("/", response_model=UserResponse)
def create_user(
    user : UserCreate,
    db : Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail="Email already exists."
        )

    db_user = User(
            username = user.username,
            email = user.email,
            password = hash_password(user.password),
            role = user.role
        )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id : int,
    updated_user : UserUpdate,
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

    setattr(user, "username", updated_user.username)
    setattr(user, "email", updated_user.email)
    setattr(user, "password", updated_user.password)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id : int,
    db : Session = Depends(get_db),
    admin:User=Depends(require_admin)):

    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


