from app import db
from app.models import Post, Library

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QComboBox, QGridLayout, QWidget, QHBoxLayout, QFrame
from sqlalchemy.exc import IntegrityError

import random as rd

class LabeledEntry(QWidget):
    """
    Custom combination of QLabel and QLineEdit objects
    """
    def __init__(self, label: str, entry: str = "") -> None:
        super().__init__()

        self.label = QLabel(label)
        self.entry = QLineEdit(entry)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.entry)

        self.setLayout(self.layout)

    def text(self) -> str:
        return self.entry.text()

    def __repr__(self) -> str:
        return f"<LabeledEntry {self.label}>"
    
class framed_widget(QWidget):
    """
    I'm tired of adding the frame each time
    """
    def __init__(self) -> None:
        super().__init__()

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)

        self.frame_layout = QGridLayout(self.frame)
        self.frame_layout.setContentsMargins(10, 10, 10, 10)

        self.master_layout = QGridLayout(self)
        self.master_layout.addWidget(self.frame)

class blog_poster(framed_widget):
    def __init__(self, Session) -> None:
        super().__init__()

        self.Session = Session

        self.title = LabeledEntry("Title:")

        self.post = LabeledEntry("Content:")

        self.post_type = QComboBox()
        self.post_type.addItem("Test")
        self.post_type.addItem("General")
        self.post_type.addItem("Website Update")

        self.post_button = QPushButton("Post")
        self.post_button.clicked.connect(self.submit_post)

        self.frame_layout.addWidget(self.title, 0, 0)
        self.frame_layout.addWidget(self.post, 1, 0)
        self.frame_layout.addWidget(self.post_type, 2, 0)
        self.frame_layout.addWidget(self.post_button, 3, 0)     

    def submit_post(self) -> None:
        
        new_post = Post(title = self.title.text(), body = self.post.text(), post_type = self.post_type.currentText())

        try:
            with self.Session() as session:
                session.add(new_post)
                session.commit()
                print(new_post)

        except IntegrityError:
            session.rollback()
            print("Insert failed — likely a constraint violation")

class library_addition(framed_widget):
    def __init__(self, Session) -> None:
        super().__init__()

        self.Session = Session

        self.title = LabeledEntry("Title:")
        self.author = LabeledEntry("Author:")
        self.other_authors = LabeledEntry("Other Authors:")
        self.series = LabeledEntry("Series:")
        self.genres = LabeledEntry("Genres:")
        self.page_count = LabeledEntry("Page Count:")
        self.book_count = LabeledEntry("Book Count:")
        self.summary = LabeledEntry("Summary:")
        self.rating = LabeledEntry("Rating(x/10):")
        self.review = LabeledEntry("Review:")
        self.library_type = QComboBox()
        self.library_type.addItem("book")
        self.library_type.addItem("series")

        self.submit_button = QPushButton("Post")
        self.submit_button.clicked.connect(self.submit)

        self.frame_layout.addWidget(self.title, 0, 0)
        self.frame_layout.addWidget(self.author, 1, 0)
        self.frame_layout.addWidget(self.other_authors, 2, 0)
        self.frame_layout.addWidget(self.series, 3, 0)
        self.frame_layout.addWidget(self.genres, 4, 0)
        self.frame_layout.addWidget(self.page_count, 5, 0)
        self.frame_layout.addWidget(self.book_count, 6, 0)
        self.frame_layout.addWidget(self.summary, 7, 0)
        self.frame_layout.addWidget(self.rating, 8, 0)
        self.frame_layout.addWidget(self.review, 9, 0)
        self.frame_layout.addWidget(self.library_type, 10, 0)
        self.frame_layout.addWidget(self.submit_button, 11, 0)
        

        self.colors = ["#e06058","#f5c23e","#58e060","#346ec9","#6058e0",
                       "#6e4f19","#23085e",
                       "#ffffdd","#222222"]
        self.weights = [7,7,7,7,7,
                        2,2,
                        1,1]
    def get_random_color(self, seed) -> str:
        rd.seed(seed)
        return rd.choices(self.colors, self.weights, k=1)[0]
    
    def submit(self) -> None:

        try:
            series = self.series.text() if self.series.text() else None
            other_authors = self.other_authors.text() if self.other_authors.text() else None
            book_count = int(self.book_count.text()) if self.book_count.text() else None
        except Exception as e:
            print(f"An error was encountered. Double check your entries.\n\n{e}")
            return


        new_entry = Library(library_type = self.library_type.currentText(),
                            title = self.title.text(),
                            author = self.author.text(),
                            series = series,
                            other_authors = other_authors,
                            genres = self.genres.text(),
                            page_count = int(self.page_count.text()),
                            book_count = book_count,
                            color = self.get_random_color(self.title.text()),
                            summary = self.summary.text(),
                            rating = int(self.rating.text()),
                            review = self.review.text()
                            )

        try:
            with self.Session() as session:
                session.add(new_entry)
                session.commit()
                print(new_entry)

        except IntegrityError:
            session.rollback()
            print("Insert failed — likely a constraint violation")        