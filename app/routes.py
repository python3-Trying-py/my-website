from flask import render_template
from app import app, db
from app.models import Post
import sqlalchemy as sa

@app.route('/')
@app.route('/index')
def index():

    query = sa.select(Post).order_by(Post.id)
    posts = db.session.scalars(query).all()

    return render_template("index.html", title='Home Page', posts=posts)