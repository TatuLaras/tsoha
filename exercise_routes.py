from app import app, db
from user import get_logged_in_user
from flask import json, redirect, request, session
from sqlalchemy import text


@app.route("/answer/<int:exercise_id>", methods=["POST"])
def answer(exercise_id):
    #  NOTE: exercise_id is either exercise_choice_id or exercise_text_id,
    #  not an actual id in the database

    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # ensure all necessary data is present
    answer = request.form.get("answer", "")
    course_article_id = request.form.get("course_article_id", 0)
    course_id = request.form.get("course_id", 0)

    if answer == 0 or course_article_id == 0 or course_id == 0:
        return (
            """400, Bad request: answer, course_article_id, 
        course_id need to be present in form data and non-zero""",
            400,
        )

    # all exercise elements on the page have an id like #choice-2 or #text-1
    choice = "choice" in request.form
    exercise_element_id = f"{'choice' if choice else 'text'}-{exercise_id}"

    # check if the answer is correct

    is_correct = False

    if choice:
        query = """
            SELECT is_correct 
            FROM tl_exercise_choice_option 
            WHERE exercise_choice_id = :exercise_id AND id = :answer
        """
        choice = db.session.execute(
            text(query), {"exercise_id": exercise_id, "answer": answer}
        ).fetchone()

        if choice:
            is_correct = choice.is_correct

    else:
        query = "SELECT 1 FROM tl_exercise_text WHERE id = :exercise_id AND answer = :answer"
        is_correct = db.session.execute(
            text(query), {"exercise_id": exercise_id, "answer": answer}
        ).fetchone()

    if is_correct:
        # register points
        query = """
            INSERT INTO tl_points 
            (user_id, type, point) 
            VALUES 
            (:user_id, :type, :point) 
            ON CONFLICT DO NOTHING
        """
        db.session.execute(
            text(query),
            {"user_id": user.id, "type": 2 if choice else 1, "point": exercise_id},
        )
        db.session.commit()

    else:
        # this enables us to highlight the incorrect exercise later on
        session["incorrect"] = exercise_element_id

    #  TODO: Maybe have a limited number of tries?
    #  TODO: Access this route through javascript instead of doing the form?

    # redirect back to where we came from
    return redirect(
        f"/course/{course_id}?article={course_article_id}#{exercise_element_id}"
    )


@app.route("/exercise/text/update/<int:exercise_id>", methods=["POST"])
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

    query = "UPDATE tl_exercise_text SET question = :question, answer = :answer WHERE id = :id"
    db.session.execute(
        text(query), {"id": exercise_id, "question": question, "answer": answer}
    )
    db.session.commit()

    redirect_url = request.form.get("redirect_url", None)
    if redirect_url:
        return redirect(redirect_url)

    return redirect("/")


@app.route("/exercise/choice/update/<int:exercise_id>", methods=["POST"])
def update_exercise_choice(exercise_id):
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # ensure that the user is a teacher and owns the course the exercise belongs to

    query = """
        SELECT 1 

        FROM tl_exercise_choice AS ec

        LEFT JOIN tl_course_article AS ca
        ON ca.id = ec.course_article_id

        LEFT JOIN tl_course AS c 
        ON c.id = ca.course_id 

        WHERE ec.id = :id AND c.user_id = :user_id
    """

    is_own = db.session.execute(
        text(query), {"id": exercise_id, "user_id": user.id}
    ).fetchone()

    if not user.is_teacher or not is_own:
        return "403: Forbidden", 403

    # ensure that all the necessary data is present and valid

    question = request.form.get("question", None)

    #  NOTE: Here we do something iffy. We use two different arrays for the labels and "is_correct" field.
    #   Form arrays are quaranteed to be in the order they are in the document however, so I don't see an issue with this.
    #   Also flask doesn't seem to support multidimensional arrays from forms.

    choices = request.form.get("choices", None)

    if not question or len(question) == 0:
        return "400: Bad Request", 400

    # do it

    query = "UPDATE tl_exercise_choice SET question = :question WHERE id = :id"
    db.session.execute(text(query), {"id": exercise_id, "question": question})

    # delete all old choices, just easier this way
    query = "DELETE FROM tl_exercise_choice_option WHERE exercise_choice_id = :id"
    db.session.execute(text(query), {"id": exercise_id})

    if choices:
        # insert choices

        choices = json.loads(choices)

        # collecting all choices (options) into a single insert query
        values = ""

        for choice in choices:
            if "label" not in choice or "is_correct" not in choice:
                continue

            choice_label = choice["label"].strip()
            if len(choice_label) == 0:
                continue

            comma = "," if len(values) > 0 else ""

            values = f"{values}{comma}(:id, '{choice['label']}', {'TRUE' if choice['is_correct'] else 'FALSE'})"

        if len(values) != 0:
            query = f"INSERT INTO tl_exercise_choice_option (exercise_choice_id, label, is_correct) VALUES {values}"
            db.session.execute(text(query), {"id": exercise_id})

    db.session.commit()

    redirect_url = request.form.get("redirect_url", None)
    if redirect_url:
        return redirect(redirect_url)

    return redirect("/")


@app.route("/exercise", methods=["POST"])
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
