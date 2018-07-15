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
    print("call index")
    return render_template("index.html", sigin = session["user_id"])

@app.route("/signin", methods=["GET", "POST"])
def signin():
    print("call signin")
    session["user_id"] = "Maxim"
    return redirect(url_for("index"))

@app.route("/register", methods=["POST"])
def register():
    print("call register")
    session["user_id"] = "Maxim"
    return redirect(url_for("index"))

@app.route("/signout", methods=["GET", "POST"])
@login_required
def signout():
    print("call signout")
    session["user_id"] = None
    print(session)
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
