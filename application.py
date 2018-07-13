import os

from flask import Flask, redirect, render_template
from flask import request, session, url_for
from functools import wraps

from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *
from helpers import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html", sigin = "")


@app.route("/signin", methods=["GET", "POST"])
def signin():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("give a username!")
        if not password:
            return apology("give me a password!")

        # query database of user
        user = db.execute("""SELECT * FROM users WHERE username = :username
                              AND password = :password""", {
                          "username": username,
                          "password": password}
                          ).fetchall()
        db.commit()
        # print(user[0]['id'])

        if not user:
            return apology("no match!", "balen")

        session["id"] = user[0]["id"]

        print(session["id"])

        return apology("NICE!" "working")

    else:

        return render_template("signin.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # create_users_db()

    if request.method == "POST":

        # TODO: check user input

        # crating empty user
        new_user = User()

        new_user.username = request.form.get("username")
        new_user.email = request.form.get("email")
        new_user.password = request.form.get("password")

        new_user.register()

    return render_template("register.html")


def create_users_db():
    db.execute("""CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR NOT NULL,
        email VARCHAR NOT NULL,
        password VARCHAR NOT NULL
    );""")
    db.commit()


def apology(top="", bottom=""):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(top), bottom=escape(bottom))

if __name__=="__main__":
    main()
