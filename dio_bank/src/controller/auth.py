from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from dio_bank.src.app import User, db

app = Blueprint('auth', __name__, url_prefix='/auth')

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    userDb = db.session.query(User).filter(User.username == username).first()
    if username != userDb.username or password != userDb.password:
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=username)
    return {"access_token":access_token}

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        return {"msg": "POST funciona!"}, 200
    return {"msg": "GET funciona!"}, 200