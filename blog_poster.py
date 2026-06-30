import sys
import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QComboBox, QGridLayout, QWidget

from app import db
from app.models import Post
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.exc import IntegrityError


'''
I quickly cobbled this together, so its quite bad
'''

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        basedir = os.path.abspath(os.path.dirname(__file__))
        engine = sa.create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))
        self.Session = so.sessionmaker(bind=engine)

        self.setWindowTitle("Blog Poster")

        self.title_label = QLabel("Title")
        self.title_entry = QLineEdit()

        self.post_label = QLabel("Content")
        self.post_entry = QLineEdit()

        self.post_type = QComboBox()
        self.post_type.addItem("Test")
        self.post_type.addItem("General")
        self.post_type.addItem("Website Update")

        self.post_button = QPushButton("Post")
        self.post_button.clicked.connect(self.submit_post)

        master_layout = QGridLayout()
        master_layout.addWidget(self.title_label, 0, 0)
        master_layout.addWidget(self.title_entry, 0, 1)
        master_layout.addWidget(self.post_label, 1, 0)
        master_layout.addWidget(self.post_entry, 1, 1)
        master_layout.addWidget(self.post_type, 2, 0)
        master_layout.addWidget(self.post_button, 3, 0)

        # Set the central widget of the Window.
        master_widget = QWidget()
        master_widget.setLayout(master_layout)
        self.setCentralWidget(master_widget)

    def submit_post(self) -> None:
        
        new_post = Post(title = self.title_entry.text(), body = self.post_entry.text(), post_type = self.post_type.currentText())

        try:
            with self.Session() as session:
                session.add(new_post)
                session.commit()

        except IntegrityError:
            session.rollback()
            print("Insert failed — likely a constraint violation")

        print(f"{self.title_entry.text()} ({self.post_type.currentText()})\n\n{self.post_entry.text()}")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()