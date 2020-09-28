from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('user', __name__, url_prefix='/user')

def getUserPosts(username):
    posts = get_db().execute(
    'SELECT p.id, title, body, created, author_id, username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE u.username = ?',
    (username,)).fetchall()

    return posts


@bp.route('/<username>')
@login_required
def user(username):
    #get all posts
    userPosts = getUserPosts(username)

    return render_template('user/user.html', posts=userPosts, username=username)
