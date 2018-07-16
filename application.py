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

    user = User()

    session.clear()
    user.username = request.form.get("username")
    user.password = request.form.get("password")

    if not user.username and not user.password:
        flash("Provide a username and a password")
        return redirect(url_for("index"))

    # TODO try catch?
    user.login()

    return redirect(url_for("index"))

@app.route("/register", methods=["POST"])
def register():

    user = User()

    user.username = request.form.get("username")
    user.email = request.form.get("email")
    user.password = request.form.get("password")

    if not user.username and not user.password and not user.email:
        flash("Provide a username, password and email.")
        return redirect(url_for("index"))

    user.register()

    return redirect(url_for("index"))

@app.route("/signout", methods=["POST"])
@login_required
def signout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/search", methods=["GET","POST"])
@login_required
def search():
    print("search")

    print(request.form.get("look_up"))


    return render_template("search.html")

if __name__ == "__main__":
    main()
