from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field






app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:qwerty@localhost:5432/book-store"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Author(db.Model):
    __tablename__ = "Author"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    specialization = db.Column(db.String(50))
    
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
        
    def __repr__(self):
        return '<Product %d>' % self.id
    
    
    
class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author
        load_instance = True
        
    id = ma.auto_field()
    name = ma.auto_field()
    specialization = ma.auto_field()
    





@app.route("/authors", methods = ['GET'])
def index():
    get_authors = Author.query.all()
    author_schema = AuthorSchema(many=True)
    authors, error = author_schema.dumps(get_authors)
    return make_response(jsonify({"authors": authors}))


if __name__ == "__main__":
    app.run
