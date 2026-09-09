
from typing import cast

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status
from app.services import post_service
from database import get_db
from app.models import User
from app.schemas import PostCreate, PostResponse
from app.auth import get_current_user
from app.repositories import post_repository


router = APIRouter()

@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db), skip: int = 0, limit:int = Query(default=10, le=100)):
    return post_repository.get_posts(db, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.get_post(db, post_id)


@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    return post_service.create_post(db, post, current_user)


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return post_service.update_post(db, post_id, post_data, current_user)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id:int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return post_service.delete_post(db, post_id, current_user)

