from sqlalchemy.orm import Session
from app.models import Post


def get_post_by_id(db: Session, post_id: int):
    return (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )