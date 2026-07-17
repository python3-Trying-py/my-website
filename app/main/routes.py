from flask import render_template, request, url_for, current_app
from app import db
from app.models import Post
import sqlalchemy as sa
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():

    page = request.args.get('page', 1, type=int)

    if current_app.debug:
        query = sa.select(Post).order_by(Post.id.desc())
    else:
        query = sa.select(Post).where(Post.post_type != "Test").order_by(Post.id.desc())
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
    books = [{"type": "book", "title": "The Prince of Milk", "color": "#58e060", "page_count": 352},
             {"type": "book", "title": "Blade Runner", "color": "#c78be6", "page_count": 240},
             {"type": "series", "title": "Hyperion", "color": "#f5c23e", "page_count": 2230, "book_count": 4},
             {"type": "book", "title": "Warbreaker", "color": "#e76ebc", "page_count": 592},
             {"type": "series", "title": "The Stromlight Archive", "color": "#ed4c4c", "page_count": 6200, "book_count": 5}
             ]
    return render_template("extra/library.html",books=books)