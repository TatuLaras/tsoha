from flask_wtf import CSRFProtect
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from user import get_logged_in_user
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URL")
app.secret_key = getenv("SESSION_SECRET")

db = SQLAlchemy(app)
csrf = CSRFProtect(app)


@app.route("/")
def index():
    user = get_logged_in_user(db)
    if not user:
        return redirect("/login")

    # get my courses
    query = """
        SELECT 
        c.id, c.name, c.description,
        u.username AS creator,
        tlaras."percentage"(:user_id, cu.course_id) AS percentage

        FROM tlaras.course_user AS cu 

        LEFT JOIN tlaras.course AS c 
        ON c.id = cu.course_id 

        LEFT JOIN tlaras.user AS u
        ON u.id = c.user_id

        WHERE cu.user_id = :user_id

        ORDER BY c.id DESC
    """
    result = db.session.execute(text(query), {"user_id": user.id})
    my_courses = result.fetchall()

    # get all courses

    query = """
        SELECT 
        c.id, c.name, c.description,
        u.username AS creator

        FROM tlaras.course AS c 

        LEFT JOIN tlaras.user AS u 
        ON u.id = c.user_id

        ORDER BY c.id DESC
    """
    result = db.session.execute(text(query))
    all_courses = result.fetchall()

    colors = ["#eb3b5a", "#fa8231", "#f7b731", "#20bf6b", "#0fb9b1"]
    colors_len = len(colors)

    skip = "tutorial" in session
    session["tutorial"] = "yes"

    return render_template(
        "index.html",
        user=user,
        all_courses=all_courses,
        my_courses=my_courses,
        colors=colors,
        colors_len=colors_len,
        show_tutorial=not skip,
    )


import auth_routes
import course_routes
import exercise_routes
import dashboard_routes
import article_routes
