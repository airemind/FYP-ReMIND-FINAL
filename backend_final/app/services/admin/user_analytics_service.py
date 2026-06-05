from sqlalchemy.orm import Session
from app.models.user import User


def get_user_analytics(db: Session):

    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    inactive_users = db.query(User).filter(User.is_active == False).count()
    logged_in_users = db.query(User).filter(User.is_logged_in == True).count()
    logged_out_users = db.query(User).filter(User.is_logged_in == False).count()
    logged_in_active_users = (
        db.query(User).filter(User.is_logged_in == True, User.is_active == True).count()
    )

    logged_in_inactive_users = (
        db.query(User)
        .filter(User.is_logged_in == True, User.is_active == False)
        .count()
    )

    logged_out_active_users = (
        db.query(User)
        .filter(User.is_logged_in == False, User.is_active == True)
        .count()
    )

    logged_out_inactive_users = (
        db.query(User)
        .filter(User.is_logged_in == False, User.is_active == False)
        .count()
    )

    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "logged_in_users": logged_in_users,
        "logged_out_users": logged_out_users,
        "logged_in_active_users": logged_in_active_users,
        "logged_in_inactive_users": logged_in_inactive_users,
        "logged_out_active_users": logged_out_active_users,
        "logged_out_inactive_users": logged_out_inactive_users,
        "graph_data": {
            "labels": [
                "LoggedIn + Active",
                "LoggedIn + Inactive",
                "LoggedOut + Active",
                "LoggedOut + Inactive",
            ],
            "values": [
                logged_in_active_users,
                logged_in_inactive_users,
                logged_out_active_users,
                logged_out_inactive_users,
            ],
        },
    }
