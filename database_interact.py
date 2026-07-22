import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from modules import blog_poster, library_addition

import sqlalchemy as sa
import sqlalchemy.orm as so


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

        self.setWindowTitle("Database Interact")

        self.blog_poster = blog_poster(self.Session)
        self.library_addition = library_addition(self.Session)

        self.master_layout = QGridLayout()
        self.master_layout.addWidget(self.blog_poster, 0, 0)
        self.master_layout.addWidget(self.library_addition, 0, 1)

        container = QWidget()
        container.setLayout(self.master_layout)
        self.setCentralWidget(container)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()