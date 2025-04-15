from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import inspect

from dio_bank.src.app import Post, db

app = Blueprint('posts', __name__, url_prefix='/posts')

def _create_post():
    data = request.json
    post = Post()
    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.add(post)
    db.session.commit()


def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "created": post.created,
            "author_id": post.author_id
        }
        for post in posts
    ]


@app.route('/', methods=["GET", "POST"])
def handle_post():
    if request.method == "POST":
        _create_post()
        return {"message": "Post Created!"}, HTTPStatus.CREATED
    else:
        return {"posts": _list_posts()}


@app.route("/<int:post_id>")
def get_id(post_id):
    post = db.get_or_404(Post, post_id)
    return {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "created": post.created,
            "author_id": post.author_id
        }


@app.route("/<int:post_id>", methods=["DELETE"])
def delete(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT