from fastapi import status
from sqlalchemy.orm import Session
from app.models import Post


def create_post(db: Session, post_data, current_user):
    db_post = Post(
        title=post_data.title,
        content=post_data.content,
        owner_id=current_user.id
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Post)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_post_by_id(db: Session, post_id: int):
    return (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )


def update_post(db: Session, post: Post):

   db.commit()
   db.refresh(post)

   return post

def delete_post(db: Session, post: Post):
    db.delete(post)
    db.commit()

    return status.HTTP_204_NO_CONTENT
