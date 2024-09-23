from flask import Flask
from os import getenv
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

app = Flask("tmp")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URL")

db = SQLAlchemy(app)

while True:
    with app.app_context():

        print("\nHaluatko:")
        print("    A) ylentää käyttäjän opettajaksi?")
        print("    B) poistaa käyttäjän opettajuuden?")

        choice = input("\n( A / B ): ").lower().strip()

        if choice == "a":
            username = input("Käyttäjänimi: ").strip()

            if len(username) == 0:
                print("Virheellinen syöte!")
                continue

            query = (
                "UPDATE tlaras.user SET is_teacher = TRUE WHERE username = :username"
            )
            db.session.execute(text(query), {"username": username})
            db.session.commit()

            print("\nToiminto suoritettu.")
            break

        if choice == "b":
            query = "SELECT id, username FROM tlaras.user WHERE is_teacher = TRUE"
            teachers = db.session.execute(text(query)).fetchall()

            if not teachers:
                print("Ei opettajia.")
                continue

            print("\nOpettajat:")
            for i, teacher in enumerate(teachers):
                print("    ", end="")
                print(f"{i}) {teacher.username}")

            try:
                index = int(input(f"\n( 0 - {len(teachers) - 1} ): "))
                if index < 0 or index >= len(teachers):
                    raise ValueError
            except ValueError:
                print("Virheellinen syöte!")
                continue

            user_id = teachers[index].id

            query = "UPDATE tlaras.user SET is_teacher = FALSE WHERE id = :id"
            db.session.execute(text(query), {"id": user_id})
            db.session.commit()

            print("\nToiminto suoritettu.")
            break

        print("Virheellinen syöte!")
