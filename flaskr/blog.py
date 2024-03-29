from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    reviews = db.execute(
        'SELECT mr.id, movie_name, actors, director, length, genre, rating, review, mr.created, mr.author_id, username'
        ' FROM movie_review mr JOIN user u ON mr.author_id = u.id'
        ' ORDER BY mr.created DESC'
    ).fetchall()
    return render_template('blog/index.html', reviews=reviews)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        actors = request.form['actors']
        director = request.form['director']
        length = request.form['length']
        genre = request.form['genre']
        rating = request.form['rating']
        review = request.form['review']
        error = None

        if not movie_name:
            error = 'Movie name is required.'

        if not review:
            error = 'Review is required.' if error is None else error

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO movie_review (movie_name, actors, director, length, genre, rating, review, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (movie_name, actors, director, int(length), genre, int(rating), review, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_movie_review(id, check_author=True): # TODO make sure get_post is not used somewhere els
    movie_review = get_db().execute(
        'SELECT mr.id, movie_name, actors, director, length, genre, rating, review, mr.created, mr.author_id, username'
        ' FROM movie_review mr JOIN user u ON mr.author_id = u.id'
        ' WHERE mr.id = ?',
        (id,)
    ).fetchone()

    if movie_review is None:
        abort(404, f"Movie review id {id} doesn't exist.")

    if check_author and movie_review['author_id'] != g.user['id']:
        abort(403)

    return movie_review


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    review = get_movie_review(id)

    if request.method == 'POST':
        movie_name = request.form['movie_name']
        actors = request.form['actors']
        director = request.form['director']
        length = request.form['length']
        genre = request.form['genre']
        rating = request.form['rating']
        review_text = request.form['review']
        error = None

        if not movie_name:
            error = 'Movie name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE movie_review SET movie_name = ?, actors = ?, director = ?, length = ?, genre = ?, rating = ?,' \
                'review = ?'
                ' WHERE id = ?',
                (movie_name, actors, director, length, genre, rating, review_text, id)
            ) # TODO make sure the above \ doesn't create any issues
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', review=review)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_movie_review(id)
    db = get_db()
    db.execute('DELETE FROM movie_review WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
