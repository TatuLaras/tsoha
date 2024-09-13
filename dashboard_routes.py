from app import app, db
from user import get_logged_in_user
from course import get_course
from flask import redirect, render_template, request, session
from sqlalchemy import text


@app.route("/dashboard")
def dashboard():
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    if not user.is_teacher:
        return "403: Forbidden", 403

    # get all possible get params (all are optional)
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
        query = "SELECT id, course_id, title, content FROM tl_course_article WHERE course_id = :course_id"
        articles = db.session.execute(
            text(query), {"course_id": current_course_id}
        ).fetchall()

        # etc ..
        if not current_article_id:
            raise NameError()

        # get current article
        query = (
            "SELECT id, course_id, title, content FROM tl_course_article WHERE id = :id"
        )
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

            current_exercise = ("choice", exercise, [])
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


@app.route("/update/course/<int:course_id>", methods=["POST"])
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


@app.route("/add/course", methods=["POST"])
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


@app.route("/update/article/<int:article_id>", methods=["POST"])
def update_article(article_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # ensure that the user is a teacher and owns the course the article belongs to

    query = """
        SELECT 1 

        FROM tl_course_article AS a 

        LEFT JOIN tl_course AS c 
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

    if not title or len(title) == 0:
        return "400: Bad Request", 400

    # do it

    query = (
        "UPDATE tl_course_article SET title = :title, content = :content WHERE id = :id"
    )
    db.session.execute(
        text(query), {"id": article_id, "title": title, "content": content}
    )
    db.session.commit()

    redirect_url = request.form.get("redirect_url", None)
    if redirect_url:
        return redirect(redirect_url)

    return redirect("/")


@app.route("/add/article", methods=["POST"])
def add_article():
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    course_id = request.form.get("course_id", None)

    if not course_id:
        return "400: Bad Request", 400

    # ensure that the user is a teacher and owns the course

    query = "SELECT 1 FROM tl_course WHERE id = :id AND user_id = :user_id"
    is_own = db.session.execute(
        text(query), {"id": course_id, "user_id": user.id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    query = "INSERT INTO tl_course_article (course_id, title, content) VALUES (:course_id, 'Uusi artikkeli', '') RETURNING id"
    article = db.session.execute(text(query), {"course_id": course_id}).fetchone()
    if not article:
        return "500: Internal Server Error", 500

    db.session.commit()

    return redirect(f"/dashboard?course={course_id}&article={article.id}")


@app.route("/update/text/<int:exercise_id>", methods=["POST"])
def update_exercise_text(exercise_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # ensure that the user is a teacher and owns the course the exercise belongs to

    query = """
        SELECT 1 

        FROM tl_exercise_text AS et

        LEFT JOIN tl_course_article AS ca
        ON ca.id = et.course_article_id


        LEFT JOIN tl_course AS c 
        ON c.id = ca.course_id 

        WHERE et.id = :id AND c.user_id = :user_id
    """

    is_own = db.session.execute(
        text(query), {"id": exercise_id, "user_id": user.id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    # ensure that all the necessary data is present and valid

    question = request.form.get("question", None)
    answer = request.form.get("answer", "")

    if not question or len(question) == 0:
        return "400: Bad Request", 400

    # do it

    query = (
        "UPDATE tl_exercise_text SET question = :question, answer = :answer WHERE id = :id"
    )
    db.session.execute(
        text(query), {"id": exercise_id, "question": question, "answer": answer}
    )
    db.session.commit()

    redirect_url = request.form.get("redirect_url", None)
    if redirect_url:
        return redirect(redirect_url)

    return redirect("/")


@app.route("/add/exercise", methods=["POST"])
def add_exercise():
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    course_article_id = request.form.get("article_id", None)
    course_id = request.form.get("course_id", None)
    exercise_type = request.form.get("type", None)

    if not course_article_id or not exercise_type or not course_id:
        return "400: Bad Request", 400

    # ensure that the user is a teacher and owns the course the article belongs to

    query = """
        SELECT 1 

        FROM tl_course_article AS a 

        LEFT JOIN tl_course AS c 
        ON c.id = a.course_id 

        WHERE a.id = :id AND c.user_id = :user_id
    """

    is_own = db.session.execute(
        text(query), {"id": course_article_id, "user_id": user.id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    query = None

    if exercise_type == "text":
        query = """
            INSERT INTO tl_exercise_text (course_article_id, question, answer)
            VALUES (:article_id, 'Uusi tekstitehtävä', '')
            RETURNING id
        """

    elif exercise_type == "choice":
        query = """
            INSERT INTO tl_exercise_choice (course_article_id, question)
            VALUES (:article_id, 'Uusi monivalintatehtävä')
            RETURNING id
        """

    if not query:
        return "400: Bad Request", 400

    exercise = db.session.execute(
        text(query), {"article_id": course_article_id}
    ).fetchone()

    db.session.commit()

    if not exercise:
        return "500: Internal Server Error", 500

    return redirect(
        f"/dashboard?course={course_id}&article={course_article_id}&exercise={exercise.id}&type={exercise_type}"
    )
