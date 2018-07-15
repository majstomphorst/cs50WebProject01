import os

from flask import Flask, redirect, render_template
from flask import request, session, url_for, flash
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
    return render_template("index.html")

@app.route("/signin", methods=["POST"])
def signin():

    session.clear()

    username = request.form.get("username")
    password = request.form.get("password")

    if not username and not password:
        flash("Provide a username and a password")
        return redirect(url_for("index"))

    user = db.execute("SELECT * FROM users WHERE\
                   username = :username AND password = :password",
                  {"username": username, "password": password}).fetchall()
    db.commit()

    if len(user) == 1:
        session["id"] = user[0]["id"]
        session["username"] = user[0]["username"]
    else:
        flash("signin credentials are wrong. Try again")

    return redirect(url_for("index"))

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username and not password and not email:
        flash("Provide a username, password and email.")
        return redirect(url_for("index"))

    username_check = db.execute("SELECT * FROM users WHERE\
                                username = :username",
                                {"username": username}).fetchall()

    if len(username_check) == 1:
        flash("username taken sorry!")
        return redirect(url_for("index"))

    db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",  { "username": username, "email": email, "password": password})
    db.commit()
    user = db.execute("SELECT * FROM users WHERE\
                   username = :username AND password = :password",
                  {"username": username, "password": password}).fetchall()
    session["id"] = user[0]["id"]
    session["username"] = user[0]["username"]

    db.commit()

    return redirect(url_for("index"))

@app.route("/signout", methods=["POST"])
@login_required
def signout():
    session.clear()
    return redirect(url_for("index"))

def create_users_db():
    db.execute("""CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR NOT NULL,
        email VARCHAR NOT NULL,
        password VARCHAR NOT NULL
    );""")
    db.commit()

if __name__ == "__main__":
    main()
