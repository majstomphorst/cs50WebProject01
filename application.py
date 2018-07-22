import os

from flask import Flask, redirect, render_template, request, session, url_for, flash
from functools import wraps
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import xml.etree.ElementTree as et
import urllib.request

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

@app.route("/select", methods=["POST"])
@login_required
def select():
    print(request.form.get("select"))
    return render_template("search.html")

@app.route("/search", methods=["GET","POST"])
@login_required
def search():

    if request.method == "POST":
        search_query = request.form.get("look_up")
        search1 = str(search_query) + '%'

        result = db.execute("SELECT * FROM books WHERE title LIKE :search1 OR title = :search_query LIMIT 10",
        {"search_query": search_query,
        "search1": search1}).fetchall()
        return render_template("search.html", result = result)
    else:
        return render_template("search.html")

@app.route("/result/<string:isbn>")
@login_required
def result(isbn):

    url = "https://www.goodreads.com/search/index.xml?key=YwERiouZJhFQ1W1Qj0baWQ&q=" + str(isbn)
    f = urllib.request.urlopen(url)

    tree = et.parse(f)
    root = tree.getroot()

    result = root.find('./search/results/work/best_book')

    book = {}
    book['title'] = result.find('./title').text
    book['image_url'] = result.find('./image_url').text
    book['author'] = result.find('./author/name').text
    book['isbn'] = isbn
    book['average_rating'] = root.find('./search/results/work/average_rating').text

    return render_template("result.html", head = "Found a book!", book = book)

if __name__ == "__main__":
    main()
