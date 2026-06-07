from datetime import date
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    date_posted: so.Mapped[date] = so.mapped_column(sa.Date, index=True, default=date.today)
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    post_type: so.Mapped[str] = so.mapped_column(sa.String(16), index=True)

    def __repr__(self):
        return '<Post {} - {}>'.format(self.id, self.title)