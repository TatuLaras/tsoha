from app import app, db
from user import get_logged_in_user
from flask import redirect, render_template, request, session
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
