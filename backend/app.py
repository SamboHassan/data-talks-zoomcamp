from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, fields
from datetime import datetime

from flask_smorest import abort


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:qwerty@localhost:5432/book-store"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Author(db.Model):
    __tablename__ = "Author"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    books = db.relationship("Book", backref="Author", cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, books):
        self.first_name = first_name
        self.last_name = last_name
        self.books = books

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return "<Author %d>" % self.id


class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author
        load_instance = True

    id = ma.Number(dump_only=True)
    firts_name = ma.String(required=True)
    lasts_name = ma.String(required=True)
    created_at = ma.String(dump_only=True)


class Book(db.Model):
    __tablename__ = "Book"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("Author.id"))

    def __init__(self, title, year, author_id=None):
        self.title = title
        self.year = year
        self.author_id = author_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class BookSchema:
    class Meta:
        model = Book

    id = ma.Integer(dump_only=True)
    title = ma.String(required=True)
    year = ma.String(required=True)
    author_id = ma.Integer()


@app.get("/authors")
def authors():
    authors = Author.query.all()
    author_books_query = (
        db.session.query(Author, Book)
        .join(Book)
        .filter(Author.id == Book.author_id)
        .all()
    )

    author_books = []

    for author, book in author_books_query:
        author_books.append({"id": book.id, "title": book.title, "year": book.year})

    if len(authors) == 0:
        abort(404)

    return jsonify(
        {
            "authors": {
                author.id: {
                    "firstname": author.first_name,
                    "lastname": author.last_name,
                    "created_at": author.created_at,
                    "books": author_books,
                }
                for author in authors
            }
        }
    )


@app.post("/authors")
def create_author():
    request_data = request.get_json()
    firstname = request_data["first_name"]
    lastname = request_data["last_name"]
    created_at = request_data["created_at"]

    author = Author(first_name=firstname, last_name=lastname, created_at=created_at)
    return jsonify(
        {
            "id": author.id,
            "first_name": author.first_name,
            "last_name": author.last_name,
            "created_at": author.created_at,
        }
    )


@app.get("/books")
def books():
    books = Book.query.all()
    return jsonify(
        {
            "Success": True,
            "books": {
                book.id: {
                    "title": book.title,
                    "year": book.year,
                    "author_id": book.author_id,
                }
                for book in books
            },
        }
    )


@app.post("/books")
def create_book():
    request_data = request.get_json()
    title = request_data["title"]
    year = request_data["year"]
    author_id = request_data["author_id"]

    if request_data["author_id"] not in request_data:
        abort(404, message="Author not found")

    book = Book(title=title, year=year, author_id=author_id)
    db.session.add(book)
    db.session.commit()

    return (
        jsonify(
            {
                "id": book.id,
                "title": book.title,
                "year": book.year,
                "author_id": book.author_id,
            }
        ),
        201,
    )


if __name__ == "__main__":
    app.run
