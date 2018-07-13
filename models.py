import os

from flask import Flask, redirect, render_template
from flask import request, session,  url_for

from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class User:

    def __init__(self, username = None, email = None, password = None):
        self.user_id = None
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        str = f"username: {self.username}\nemail: {self.email}\npassword: {self.password}"
        return str

    def register(self):
        db.execute("""INSERT INTO users (username, email, password)
                    VALUES (:username, :email, :password)""",
            {"username": self.username,
             "email": self.email,
             "password": self.password })

        db.commit()
