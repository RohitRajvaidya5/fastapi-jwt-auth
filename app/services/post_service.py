

from app.exceptions import PostNotFoundException, UnauthorizedActionException
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import cast
from app.models import User
from app.repositories import post_repository
from schemas import PostCreate


def create_post(
        db: Session,
        post_data: PostCreate,
        current_user: User
):
    db_post = post_repository.create_post(db, post_data, current_user)

    return db_post


def update_post(
        db: Session,
        post_id: int,
        post_data: PostCreate,
        current_user: User
         ):

    post = post_repository.get_post_by_id(db, post_id)

    if post is None:
        raise PostNotFoundException()

    if cast(int, post.owner_id) != cast(int, current_user.id):
        raise UnauthorizedActionException()

    setattr(post, "title", post_data.title)
    setattr(post, "content", post_data.content)

    return post_repository.update_post(db, post)

def delete_post(
        db: Session,
        post_id: int,
        current_user: User
        ):

    post = post_repository.get_post_by_id(db, post_id)

    if post is None:
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     detail="Post not found"
        # )
        raise PostNotFoundException()

    if cast(int, post.owner_id) != cast(int, current_user.id):
        raise UnauthorizedActionException()

    return post_repository.delete_post(db, post)
