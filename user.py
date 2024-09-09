from flask import session
from sqlalchemy import text


def is_logged_in() -> bool:
    return session.get("user_id", 0) != 0


def get_logged_in_user(db):
    user_id = session.get("user_id", 0)
    query = "SELECT id, username, is_teacher FROM tl_user WHERE id = :user_id"
    result = db.session.execute(text(query), {"user_id": user_id})
    return result.fetchone()
