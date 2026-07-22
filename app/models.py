from datetime import date
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Post(db.Model):
    post_id: so.Mapped[int] = so.mapped_column("id", primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    date_posted: so.Mapped[date] = so.mapped_column(sa.Date, index=True, default=date.today)
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    post_type: so.Mapped[str] = so.mapped_column(sa.String(16), index=True)

    def __repr__(self) -> None:
        return f"<Post {self.post_id} - {self.title}>"
    
class Library(db.Model):
    __tablename__ = "library"

    library_ID: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    library_type: so.Mapped[str] = so.mapped_column("type", sa.String(16), nullable=False)
    title: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    author: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=False)
    series: so.Mapped[str | None] = so.mapped_column(sa.String(64), nullable=True)
    other_authors: so.Mapped[str | None] = so.mapped_column(sa.String(64), nullable=True)
    genres: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    page_count: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    book_count: so.Mapped[int | None] = so.mapped_column(sa.Integer, nullable=True)
    color: so.Mapped[str] = so.mapped_column(sa.String(7), nullable=False)
    summary: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    rating: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    review: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)

    def __repr__(self):
        return f"<Library(library_ID={self.library_ID}, title={self.title}, author={self.author})>"