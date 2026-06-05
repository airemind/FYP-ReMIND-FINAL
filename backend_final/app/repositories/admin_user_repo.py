from sqlalchemy.orm import Session
from app.models.user import User


def get_users(
    db: Session, page: int = 1, limit: int = 15, search: str = None, role: str = None
):
    query = db.query(User)

    # search
    if search:
        query = query.filter(User.username.ilike(f"%{search}%"))

    # filter role
    if role:
        query = query.filter(User.role == role)
    total = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()
    return users, total
