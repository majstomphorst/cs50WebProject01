import os

from flask import Flask, redirect, render_template
from flask import request, session,  url_for, flash

from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class User:

    def __init__(self, id = None, username = None, email = None, password = None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        str = f"username: {self.username}\n\
                email: {self.email}\n\
                password:{self.password}"
        return str

    def register(self):
        username_check = db.execute("SELECT * FROM users WHERE\
                                    username = :username",
                                    {"username": self.username}).fetchall()

        if len(username_check) == 1:
            flash("username taken sorry!")
            return redirect(url_for("index"))

        db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",  { "username": self.username, "email": self.email, "password": self.password})
        db.commit()

        user = db.execute("SELECT * FROM users WHERE\
                            username = :username AND password = :password",
                      {"username": self.username, "password": self.password}).fetchall()

        self.id = user[0]["id"]
        session["id"] = user[0]["id"]
        session["username"] = user[0]["username"]

        db.commit()

    def login(self):
        user = db.execute("SELECT * FROM users WHERE\
                       username = :username AND password = :password",
                      {"username": self.username, "password": self.password}).fetchall()
        db.commit()

        if len(user) == 1:
            # TODO only give session the user object
            self.id = user[0]["id"]
            session["id"] = user[0]["id"]
            session["username"] = user[0]["username"]
        else:
            flash("signin credentials are wrong. Try again")


    def create_users_db():
        db.execute("""CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            password VARCHAR NOT NULL
        );""")
        db.commit()

class Book:

    def __init__(self, title = None, author = None, isbn = None,
                 image_url = None, average_rating = None,
                 reviews = None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.image_url = image_url
        self.average_rating = average_rating
        self.reviews = reviews

    def get_reviews(self):
        self.reviews = db.execute("SELECT * FROM review WHERE isbn = :isbn",
        {"isbn": self.isbn}).fetchall()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function
