from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_BASE_URI'] = "postgresql://postgres:qwerty@localhost:5432/book-store"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def home():
    return "<h1>Hello World<h1>"


if __name__ == "__main__":
    app.run
