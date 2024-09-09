from app import app, db
from user import get_logged_in_user
from flask import redirect, render_template, request
from sqlalchemy import text


@app.route("/")
def index():
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # get my courses
    query = """
        SELECT 
        c.id, c.name, c.description,
        u.username AS creator

        FROM tl_course_user AS cu 

        LEFT JOIN tl_course AS c 
        ON c.id = cu.course_id 

        LEFT JOIN tl_user AS u
        ON u.id = c.user_id

        WHERE cu.user_id = :user_id
    """
    result = db.session.execute(text(query), {"user_id": user.id})
    my_courses = result.fetchall()

    # get all courses
    query = """
        SELECT 
        c.id, c.name, c.description, 
        u.username AS creator 

        FROM tl_course AS c 

        LEFT JOIN tl_user AS u 
        ON u.id = c.user_id
    """
    result = db.session.execute(text(query))
    all_courses = result.fetchall()

    colors = ["#eb3b5a", "#fa8231", "#f7b731", "#20bf6b", "#0fb9b1"]
    colors_len = len(colors)

    return render_template(
        "index.html",
        user=True,
        all_courses=all_courses,
        my_courses=my_courses,
        colors=colors,
        colors_len=colors_len,
    )


@app.route("/course/<int:course_id>")
def course(course_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # get course

    query = """
        SELECT 
        c.id, c.name, c.description, 
        u.username AS creator 

        FROM tl_course AS c 

        LEFT JOIN tl_user AS u 
        ON u.id = c.user_id

        WHERE c.id = :course_id
    """
    result = db.session.execute(text(query), {"course_id": course_id})
    course = result.fetchone()

    if not course:
        return redirect("/")

    # check if user is on course, if not show the join page instead of the actual course page

    query = "SELECT 1 FROM tl_course_user WHERE user_id = :user_id AND course_id = :course_id"
    has_joined = db.session.execute(
        text(query), {"user_id": user.id, "course_id": course_id}
    ).fetchone()

    if not has_joined:
        return render_template("join.html", course=course)

    # get extra things only needed for the actual course page

    # outline
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
            SELECT id, question
            FROM tl_exercise_text
            WHERE course_article_id = :course_article_id
        """
        text_exercises = db.session.execute(
            text(query), {"course_article_id": article_id}
        ).fetchall()

        # multiple choice exercises

        query = """
            SELECT id, question
            FROM tl_exercise_choice
            WHERE course_article_id = :course_article_id
        """
        questions = db.session.execute(
            text(query), {"course_article_id": article_id}
        ).fetchall()

        for question in questions:
            query = "SELECT id, label FROM tl_exercise_choice_option WHERE exercise_choice_id = :exercise_choice_id"
            choices = db.session.execute(
                text(query), {"exercise_choice_id": question.id}
            ).fetchall()

            choice_exercises.append((question, choices))

    return render_template(
        "course.html",
        course=course,
        user=True,
        articles=articles,
        current_article=current_article,
        text_exercises=text_exercises,
        choice_exercises=choice_exercises,
    )


@app.route("/join/<int:course_id>")
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
