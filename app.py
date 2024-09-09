from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URL")
app.secret_key = getenv("SESSION_SECRET")

db = SQLAlchemy(app)


import auth_routes
import course_routes
import exercise_routes
