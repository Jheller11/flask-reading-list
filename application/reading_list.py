from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from application.auth import login_required
from application.db import get_db

bp = Blueprint('reading_list', __name__, url_prefix='/reading_list')


@bp.route('/articles')
def index():
    db = get_db()
    articles = db.execute(
        'SELECT p.id, title, created, author_id, url, read, username'
        ' FROM list_item p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('reading_list/index.html', articles=articles)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    # change this to automatically find article details
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('reading_list.index'))

    return render_template('reading_list/create.html')
