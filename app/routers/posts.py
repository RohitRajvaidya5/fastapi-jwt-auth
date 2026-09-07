
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from app.models import Post, User
from schemas import PostCreate, PostResponse
from auth import get_current_user
from app.repositories import post_repository


router = APIRouter()

@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db), skip: int = 0, limit:int = Query(default=10, le=100)):

    posts = (
        db.query(Post)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return posts

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):

    post = post_repository.get_post_by_id(db, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return post




@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    db_post = Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    db_post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if db_post.owner_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post owner information is missing."
        )

    if not cast(bool, db_post.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post."
        )

    db_post.title = post.title
    db_post.content = post.content

    db.commit()
    db.refresh(db_post)

    return db_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id:int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    db_post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post."
        )

    db.delete(db_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

