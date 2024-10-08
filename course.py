from sqlalchemy import text


def get_course(db, course_id):
    query = """
        SELECT 
        c.id, c.name, c.description, 
        u.username AS creator 

        FROM tlaras.course AS c 

        LEFT JOIN tlaras.user AS u 
        ON u.id = c.user_id

        WHERE c.id = :course_id
    """
    return db.session.execute(text(query), {"course_id": course_id}).fetchone()
