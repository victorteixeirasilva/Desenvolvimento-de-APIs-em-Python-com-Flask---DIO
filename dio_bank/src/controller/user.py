from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import inspect, select

from dio_bank.src.app import User, db

app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    data = request.json
    user = User(username=data["username"], password=data["password"], role_id=data["role_id"])
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role_id": user.role_id
        }
        for user in users
    ]

@app.route('/', methods=["GET", "POST"])
@jwt_required()
def handle_user():
    user = db.session.query(User).filter(User.username == get_jwt_identity()).first()
    if user.role_id != 1:
        return {"message": "User Dont have acces."}, HTTPStatus.FORBIDDEN
    if request.method == "POST":
        _create_user()
        return {"message": "User Created!"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}


@app.route("/<int:user_id>")
def get_id(user_id):
    user = db.get_or_404(User, user_id)
    return {
            "id": user.id,
            "username": user.username
        }

@app.route("/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT


@app.route("/<int:user_id>", methods=["PATCH"])
def update(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    # if "username" in data:
    #     user.username = data["username"]
    #     db.session.commit()

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {
            "id": user.id,
            "username": user.username
        }
