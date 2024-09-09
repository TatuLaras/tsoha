from app import app, db
from flask import render_template, request, session, redirect
from sqlalchemy import text
import bcrypt


@app.route("/signup", methods=["GET"])
def signup_get():
    return render_template("auth_form.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = request.form["username"]
    password = request.form["password"]

    # validate
    if len(username) < 2 or len(username) > 50:
        return render_template(
            "auth_form.html", error="Käyttäjänimen on oltava 2 - 50 merkkiä."
        )

    if len(password) < 8:
        return render_template(
            "auth_form.html", error="Salasanan on oltava vähintään 8 merkkiä."
        )

    # check if username exists
    query = "SELECT 1 FROM tl_user WHERE username = :username"
    result = db.session.execute(text(query), {"username": username})
    username_exists = result.fetchone()

    if username_exists:
        return render_template("auth_form.html", error="Käyttäjänimi on jo käytössä.")

    # all in order, register user

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    query = "INSERT INTO tl_user (username, password) VALUES (:username, :password)"
    db.session.execute(
        text(query), {"username": username, "password": hashed_password.decode()}
    )
    db.session.commit()

    return redirect("/login")


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("auth_form.html", login=True)


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    query = "SELECT id, username, password FROM tl_user WHERE username = :username"
    result = db.session.execute(text(query), {"username": username})
    user = result.fetchone()

    print("1")
    if not user:
        return render_template(
            "auth_form.html", error="Käyttäjänimi tai salasana on väärin.", login=True
        )

    hashed = user.password
    if not bcrypt.checkpw(password.encode(), hashed.encode()):
        return render_template(
            "auth_form.html", error="Käyttäjänimi tai salasana on väärin.", login=True
        )

    session["user_id"] = user.id
    return redirect("/")


@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")
