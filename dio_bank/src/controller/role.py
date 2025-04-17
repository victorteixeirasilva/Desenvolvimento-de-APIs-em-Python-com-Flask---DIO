from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from dio_bank.src.app import Role, db


app = Blueprint('role', __name__, url_prefix='/role')

@app.route('/', methods=["GET", "POST"])
# @jwt_required()
def handle_role():

    if request.method == "POST":
        data = request.json
        role = Role(name=data["name"])
        db.session.add(role)
        db.session.commit()
        return {"message": "Role Created!"}, HTTPStatus.CREATED
    else:
        return {"users": _list_roles()}


def _list_roles():
    query = db.select(Role)
    roles = db.session.execute(query).scalars()
    return [
        {
            "id": role.id,
            "name": role.name
        }
        for role in roles
    ]