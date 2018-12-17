from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from application.auth import login_required
from application.db import get_db
from application.utils import get_data

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
        url = request.form['url']
        data = get_data(url)
        error = None

        if not url:
            error = 'URL is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO list_item (url, title, author_id)'
                ' VALUES (?, ?, ?)',
                (url, data['title'], g.user['id'])
            )
            db.commit()
            return redirect(url_for('reading_list.index'))

    return render_template('reading_list/create.html')


def get_article(id, check_author=True):
    article = get_db().execute(
        'SELECT p.id, title, created, author_id, url, read, username'
        ' FROM list_item p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if article is None:
        abort(404, "Article id {0} doesn't exist.".format(id))

    if check_author and article['author_id'] != g.user['id']:
        abort(403)

    return article


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    article = get_article(id)

    if request.method == 'POST':
        url = request.form['url']
        data = get_data(url)
        error = None

        if not url:
            error = 'URL is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE list_item SET url = ?, title = ?'
                ' WHERE id = ?',
                (url, data['title'], id)
            )
            db.commit()
            return redirect(url_for('reading_list.index'))

    return render_template('reading_list/update.html', article=article)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_article(id)
    db = get_db()
    db.execute('DELETE FROM list_item WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('reading_list.index'))
