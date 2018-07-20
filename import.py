import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine("postgres://jrxmibonjppwdp:861680f71f8990135bc6cff0724f2fae69f3906f51c04afd14fdd20c2a5199a5@ec2-54-217-205-90.eu-west-1.compute.amazonaws.com:5432/d2nc77m3g9ig0d")
db = scoped_session(sessionmaker(bind=engine))

def main():
    print("hello")
    create_books_db()
    import_books()

def create_books_db():
    db.execute("""CREATE TABLE books (
        isbn TEXT PRIMARY KEY,
        title TEXT,
        author TEXT,
        year INT
    );""")
    db.commit()

def import_books():
    f = open("documents/books.csv")
    reader = csv.reader(f)
    next(reader, None)

    i = 0

    for isbn, title, author, year in reader:

        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                {"isbn": str(isbn), "title": title, "author": author, "year": int(year)})
        db.commit()




if __name__ == "__main__":
    main()
