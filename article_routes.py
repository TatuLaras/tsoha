from app import app, db
from user import get_logged_in_user
from course import get_course
from flask import redirect, render_template, request, session
from sqlalchemy import text


@app.route("/article", methods=["POST"])
def add_article():
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    course_id = request.form.get("course_id", None)

    if not course_id:
        return "400: Bad Request", 400

    # ensure that the user is a teacher and owns the course

    query = "SELECT 1 FROM tlaras.course WHERE id = :id AND user_id = :user_id"
    is_own = db.session.execute(
        text(query), {"id": course_id, "user_id": user.id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    query = "INSERT INTO tlaras.course_article (course_id, title, content) VALUES (:course_id, 'Uusi artikkeli', '') RETURNING id"
    article = db.session.execute(text(query), {"course_id": course_id}).fetchone()
    if not article:
        return "500: Internal Server Error", 500

    db.session.commit()

    return redirect(f"/dashboard?course={course_id}&article={article.id}")


@app.route("/article/update/<int:article_id>", methods=["POST"])
def update_article(article_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # ensure that the user is a teacher and owns the course the article belongs to

    query = """
        SELECT 1 

        FROM tlaras.course_article AS a 

        LEFT JOIN tlaras.course AS c 
        ON c.id = a.course_id 

        WHERE a.id = :id AND c.user_id = :user_id
    """

    is_own = db.session.execute(
        text(query), {"id": article_id, "user_id": user.id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    # ensure that all the necessary data is present and valid

    title = request.form.get("title", None)
    content = request.form.get("content", "")
    ordering = request.form.get("ordering", "0")

    try:
        ordering = int(ordering)
    except ValueError:
        return "400: Bad Request", 400

    if not title or len(title) == 0:
        return "400: Bad Request", 400

    # do it

    query = """
        UPDATE tlaras.course_article 
        SET title = :title, content = :content, ordering = :ordering 
        WHERE id = :id
    """
    db.session.execute(
        text(query),
        {"id": article_id, "title": title, "content": content, "ordering": ordering},
    )
    db.session.commit()

    redirect_url = request.form.get("redirect_url", None)
    if redirect_url:
        return redirect(redirect_url)

    return redirect("/")


@app.route("/article/delete/<int:article_id>", methods=["POST"])
def article_delete(article_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # ensure that the user is a teacher and owns the course

    query = """
        SELECT 1 

        FROM tlaras.course_article AS a 

        LEFT JOIN tlaras.course AS c 
        ON c.id = a.course_id 

        WHERE a.id = :id AND c.user_id = :user_id
    """

    is_own = db.session.execute(
        text(query), {"id": article_id, "user_id": user.id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    confirmed = request.form.get("confirmed", None)
    redirect_url = request.form.get("redirect_url", "/")

    if not confirmed:
        return render_template(
            "delete_confirmation.html",
            item_title=f"artikkeli",
            return_url=redirect_url,
            action=f"/article/delete/{article_id}",
        )

    query = "DELETE FROM tlaras.course_article WHERE id = :id"
    db.session.execute(text(query), {"id": article_id})
    db.session.commit()

    return redirect(redirect_url)
