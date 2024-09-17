from app import app, db
from user import get_logged_in_user
from course import get_course
from flask import redirect, render_template, request, session
from sqlalchemy import text


@app.route("/course/<int:course_id>", methods=["GET"])
def course(course_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # get course information
    course = get_course(db, course_id)

    if not course:
        return "404: Course not found", 404

    # check if user is on course, if not show the join page instead of the actual course page

    query = "SELECT 1 FROM tl_course_user WHERE user_id = :user_id AND course_id = :course_id"
    has_joined = db.session.execute(
        text(query), {"user_id": user.id, "course_id": course_id}
    ).fetchone()

    if not has_joined:
        return render_template("join.html", course=course, user=user)

    # get extra things only needed for the actual course page

    # outline / course articles
    query = "SELECT id, title FROM tl_course_article WHERE course_id = :course_id ORDER BY ordering ASC"
    articles = db.session.execute(text(query), {"course_id": course.id}).fetchall()

    # current article (GET-params)
    current_article = None

    text_exercises = []
    choice_exercises = []

    article_id = request.args.get("article", 0)

    if article_id != 0:
        query = (
            "SELECT id, ordering, title, content FROM tl_course_article WHERE id = :id"
        )
        current_article = db.session.execute(text(query), {"id": article_id}).fetchone()

        # text exercises

        query = """
            SELECT e.id, e.question, e.answer,

            CASE WHEN p.point IS NULL
            THEN 0 ELSE 1
            END AS completed

            FROM tl_exercise_text AS e

            LEFT JOIN tl_points AS p
            ON p.user_id = :user_id AND p.point = e.id AND p.type = 1

            WHERE e.course_article_id = :course_article_id
        """
        text_exercises = db.session.execute(
            text(query), {"course_article_id": article_id, "user_id": user.id}
        ).fetchall()

        # multiple choice exercises

        query = """
            SELECT e.id, e.question,

            CASE WHEN p.point IS NULL
            THEN 0 ELSE 1
            END AS completed

            FROM tl_exercise_choice AS e

            LEFT JOIN tl_points AS p
            ON p.user_id = :user_id AND p.point = e.id AND p.type = 2

            WHERE e.course_article_id = :course_article_id
        """
        questions = db.session.execute(
            text(query), {"course_article_id": article_id, "user_id": user.id}
        ).fetchall()

        for question in questions:
            query = "SELECT id, label, is_correct FROM tl_exercise_choice_option WHERE exercise_choice_id = :exercise_choice_id"
            choices = db.session.execute(
                text(query), {"exercise_choice_id": question.id}
            ).fetchall()

            choice_exercises.append((question, choices))

    # there might be info in a session variable about a failed exercise
    incorrect = session.get("incorrect", None)
    if incorrect:
        del session["incorrect"]

    return render_template(
        "course.html",
        course=course,
        user=user,
        articles=articles,
        current_article=current_article,
        text_exercises=text_exercises,
        choice_exercises=choice_exercises,
        incorrect=incorrect,
    )


@app.route("/join/<int:course_id>", methods=["GET"])
def join(course_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # register user for course and redirect to course page

    query = """
        INSERT INTO tl_course_user (user_id, course_id) 
        VALUES (:user_id, :course_id)
        ON CONFLICT DO NOTHING
    """
    db.session.execute(text(query), {"user_id": user.id, "course_id": course_id})
    db.session.commit()
    return redirect(f"/course/{course_id}")


@app.route("/stats/<int:course_id>", methods=["GET"])
def stats(course_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    course = get_course(db, course_id)

    if not course:
        return "404: Course not found", 404

    query = """
        SELECT ca.id, ca.title,
        CAST(
        (
            SELECT COUNT(*)

            FROM tl_points AS p

            LEFT JOIN tl_exercise_text AS set
            ON set.id = p.point AND p.type = 1

            LEFT JOIN tl_exercise_choice AS sec
            ON sec.id = p.point AND p.type = 2

            WHERE p.user_id = :user_id AND 
            (sec.course_article_id = ca.id OR set.course_article_id = ca.id)
        ) 
        AS DECIMAL)
        /
        COUNT(*) 
        AS percentage

        FROM tl_course_article AS ca 

        LEFT JOIN tl_exercise_text AS et
        ON et.course_article_id = ca.id

        LEFT JOIN tl_exercise_choice AS ec
        ON ec.course_article_id = ca.id

        WHERE course_id = :course_id

        GROUP BY ca.id
        ORDER BY ca.ordering ASC
    """
    stats = db.session.execute(
        text(query), {"user_id": user.id, "course_id": course.id}
    ).fetchall()
    print(stats)

    return render_template("stats.html", course=course, user=True, stats=stats)


@app.route("/course/update/<int:course_id>", methods=["POST"])
def update_course(course_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # ensure that the user 1. owns the course 2. is a teacher

    query = "SELECT 1 FROM tl_course WHERE user_id = :user_id AND id = :id"
    is_own = db.session.execute(
        text(query), {"user_id": user.id, "id": course_id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    # ensure that all the necessary data is present and valid

    name = request.form.get("name", None)
    description = request.form.get("description", "")

    if not name or len(name) == 0:
        return "400: Bad Request", 400

    # do it

    query = (
        "UPDATE tl_course SET name = :name, description = :description WHERE id = :id"
    )
    db.session.execute(
        text(query), {"id": course_id, "name": name, "description": description}
    )
    db.session.commit()

    redirect_url = request.form.get("redirect_url", None)
    if redirect_url:
        return redirect(redirect_url)

    return redirect("/")


@app.route("/course", methods=["POST"])
def add_course():
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    if not user.is_teacher:
        return "403: Forbidden", 403

    query = "INSERT INTO tl_course (user_id, name) VALUES (:user_id, 'Uusi kurssi') RETURNING id"
    course = db.session.execute(text(query), {"user_id": user.id}).fetchone()
    if not course:
        return "500: Internal Server Error", 500

    db.session.commit()

    return redirect(f"/dashboard?course={course.id}")


@app.route("/course/delete/<int:course_id>", methods=["POST"])
def delete_course(course_id):

    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # ensure that the user is a teacher and owns the course

    query = "SELECT 1 FROM tl_course WHERE id = :id AND user_id = :user_id"

    is_own = db.session.execute(
        text(query), {"id": course_id, "user_id": user.id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    confirmed = request.form.get("confirmed", None)
    redirect_url = request.form.get("redirect_url", None)

    if not confirmed:
        course = get_course(db, course_id)
        if not course:
            return "500: Internal Server Error", 500

        return render_template(
            "delete_confirmation.html",
            item_title=f"kurssi {course.name}",
            return_url=redirect_url if redirect_url else "/",
            action=f"/course/delete/{course_id}",
        )

    query = "DELETE FROM tl_course WHERE id = :id"
    db.session.execute(text(query), {"id": course_id})
    db.session.commit()

    return redirect(redirect_url if redirect_url else "/")
