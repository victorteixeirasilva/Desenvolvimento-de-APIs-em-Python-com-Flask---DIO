from flask import Flask

app = Flask(__name__)

@app.route("/olamundo/", methods=["POST", "GET", "PUT", "DELETE"])
def hello_world():
    return "<p>Hello, World!</p>"