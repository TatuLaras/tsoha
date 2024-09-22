from app import app, db
from user import get_logged_in_user
from course import get_course
from flask import json, redirect, render_template, request, session
from sqlalchemy import text


@app.route("/dashboard")
def dashboard():
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    if not user.is_teacher:
        return "403: Forbidden", 403

    # get params (all are optional)
    current_course_id = request.args.get("course", None)
    current_article_id = request.args.get("article", None)
    current_exercise_id = request.args.get("exercise", None)
    current_exercise_type = request.args.get("type", None)

    # get all courses
    query = "SELECT id, name FROM tl_course WHERE user_id = :user_id ORDER BY id DESC"
    courses = db.session.execute(text(query), {"user_id": user.id}).fetchall()

    # item that is shown in the leftmost inspector panel
    inspector_item = None

    current_course = None
    articles = []
    current_article = None
    exercises = []
    current_exercise = None

    # the try catch block is to avoid a long chain of nested ifs
    try:
        # stop here if there's not course id present
        if not current_course_id:
            raise NameError()

        # get current course

        current_course = get_course(db, current_course_id)
        inspector_item = ("Muokkaa kurssia", "course", current_course)

        # get articles of current course
        query = """
            SELECT id, course_id, title, content, ordering 
            FROM tl_course_article 
            WHERE course_id = :course_id 
            ORDER BY ordering ASC, id ASC
        """
        articles = db.session.execute(
            text(query), {"course_id": current_course_id}
        ).fetchall()

        # etc ..
        if not current_article_id:
            raise NameError()

        # get current article
        query = """
            SELECT id, course_id, title, content, ordering 
            FROM tl_course_article 
            WHERE id = :id
        """
        current_article = db.session.execute(
            text(query), {"id": current_article_id}
        ).fetchone()
        inspector_item = ("Muokkaa artikkelia", "article", current_article)

        # get exercises of current article
        query = """
            SELECT id, 
            (CASE WHEN LENGTH(question) < :max_chars THEN question
                ELSE SUBSTRING(question, 1, :max_chars - 3) || '...'
            END) AS question,
            'choice' AS type 

            FROM tl_exercise_choice

            WHERE course_article_id = :article_id

            UNION

            SELECT id, 
            (CASE WHEN LENGTH(question) < :max_chars THEN question
                ELSE SUBSTRING(question, 1, :max_chars - 3) || '...'
            END) AS question,
            'text' AS type 

            FROM tl_exercise_text
            WHERE course_article_id = :article_id

            ORDER BY type DESC, id ASC
        """
        exercises = db.session.execute(
            text(query), {"article_id": current_article_id, "max_chars": 30}
        ).fetchall()

        if not current_exercise_id or not current_exercise_type:
            raise NameError()

        # get current exercise

        if current_exercise_type == "choice":
            query = "SELECT id, question FROM tl_exercise_choice WHERE id = :id"
            exercise = db.session.execute(
                text(query), {"id": current_exercise_id}
            ).fetchone()

            query = """
                SELECT label, is_correct
                FROM tl_exercise_choice_option
                WHERE exercise_choice_id = :exercise_choice_id
            """
            choices = db.session.execute(
                text(query), {"exercise_choice_id": current_exercise_id}
            ).fetchall()

            current_exercise = ("choice", exercise, choices)
            inspector_item = (
                "Muokkaa monivalintatehtävää",
                "exercise-choice",
                exercise,
            )

        else:
            query = "SELECT id, question, answer FROM tl_exercise_text WHERE id = :id"
            exercise = db.session.execute(
                text(query), {"id": current_exercise_id}
            ).fetchone()

            current_exercise = ("text", exercise)
            inspector_item = (
                "Muokkaa tekstitehtävää",
                "exercise-text",
                exercise,
            )

    except NameError:
        # NameError was chosen at random, it does not represent anything besides "exit this block"
        pass

    return render_template(
        "dashboard.html",
        user=user,
        courses=courses,
        articles=articles,
        exercises=exercises,
        current_course=current_course,
        current_article=current_article,
        current_exercise=current_exercise,
        inspector_item=inspector_item,
    )


@app.route("/dashboard/stats/<int:course_id>", methods=["GET"])
def dashboard_stats(course_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    query = "SELECT 1 FROM tl_course WHERE user_id = :user_id AND id = :id"
    is_own = db.session.execute(
        text(query), {"user_id": user.id, "id": course_id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    query = """
        SELECT * FROM 
        (
            SELECT 
                'text' AS type,
                et.id AS exercise_id,
                et.question,
                MAX(ca.id) AS course_article_id,
                MAX(ca.title) AS title,
                MAX(ca.ordering) AS ordering,
                ARRAY_AGG(p.user_id) AS users

            FROM tl_exercise_text AS et

            LEFT JOIN tl_course_article AS ca
            ON ca.id = et.course_article_id

            LEFT JOIN tl_points AS p
            ON p.type = 1 AND p.point = et.id

            WHERE ca.course_id = :course_id

            GROUP BY et.id


            UNION


            SELECT 
                'choice' AS type,
                ec.id AS exercise_id,
                ec.question,
                MAX(ca.id) AS course_article_id,
                MAX(ca.title) AS title,
                MAX(ca.ordering) AS ordering,
                ARRAY_AGG(p.user_id) AS users

            FROM tl_exercise_choice AS ec

            LEFT JOIN tl_course_article AS ca
            ON ca.id = ec.course_article_id

            LEFT JOIN tl_points AS p
            ON p.type = 2 AND p.point = ec.id

            WHERE ca.course_id = :course_id

            GROUP BY ec.id

        ) AS result

        ORDER BY ordering ASC, course_article_id ASC, exercise_id ASC
    """

    exercise_stats = db.session.execute(
        text(query), {"course_id": course_id}
    ).fetchall()

    query = """
        SELECT 
            u.id, u.username,
            "percentage"(u.id, :course_id) AS percentage

        FROM tl_course_user AS cu

        LEFT JOIN tl_user AS u
        ON u.id = cu.user_id

        WHERE cu.course_id = :course_id
    """

    course_users = db.session.execute(text(query), {"course_id": course_id}).fetchall()

    print(exercise_stats)

    return render_template(
        "dashboard_stats.html",
        user=user,
        exercise_stats=exercise_stats,
        course_users=course_users,
    )
