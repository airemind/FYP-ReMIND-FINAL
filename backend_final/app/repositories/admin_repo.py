from sqlalchemy.orm import Session
from app.models.admin import Admin


def get_admin_by_admin_id(db: Session, admin_id: str):
    return db.query(Admin).filter(Admin.admin_id == admin_id).first()
