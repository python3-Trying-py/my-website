from flask import render_template, request, url_for, current_app
from app import db
from app.models import Post, Library
import sqlalchemy as sa
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():

    page = request.args.get('page', 1, type=int)

    if current_app.debug:
        query = sa.select(Post).order_by(Post.post_id.desc())
    else:
        query = sa.select(Post).where(Post.post_type != "Test").order_by(Post.post_id.desc())
    posts = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template("index.html", title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/links')
def links():
    return render_template("links.html")

@bp.route('/about_me')
def about_me():
    return render_template("about_me.html")

@bp.route('/library')
def library():
    series_query = sa.select(Library.title).where(Library.library_type == "series").order_by(Library.library_ID.desc())
    series_list = db.session.scalars(series_query).all()

    books_query = sa.select(Library).where(
        (Library.library_type == "series") | ((Library.library_type == "book") & (Library.series.not_in(series_list) | Library.series.is_(None)))
        ).order_by(Library.library_ID.asc())
    books = db.session.scalars(books_query).all()

    print(series_list)
    print(books)

    return render_template("extra/library.html",books=books)