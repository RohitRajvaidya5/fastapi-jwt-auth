
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.services import user_service
from database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from typing import List, cast
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token
from utils import verify_password
from app.schemas import Token
from app.auth import get_current_user, require_admin

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
    return user_service.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id:int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)

@router.post("/", response_model=UserResponse)
def create_user(
    user : UserCreate,
    db : Session = Depends(get_db)
):
    return user_service.create_user(db, user)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id : int,
    updated_user : UserUpdate,
    db : Session = Depends(get_db)
):
    return user_service.update_user(db, user_id, updated_user)


@router.delete("/{user_id}")
def delete_user(
    user_id : int,
    db : Session = Depends(get_db),
    admin:User=Depends(require_admin)):
    user_service.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


