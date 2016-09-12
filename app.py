import os
import sys
import logging

from moonreader_tools.handlers import FilesystemDownloader


from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QAction,
    QFileDialog,
    QTextEdit,
    QMainWindow,
)

logger = logging.getLogger('GUI')

HOME_DIR = os.path.expanduser('~')


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.books = []
        self.initUI()

    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Moonreader editor')

        self.show()

    def showDialog(self):
        search_dir = QFileDialog.getExistingDirectory(self, 'Open dir', HOME_DIR)
        print(search_dir)
        handler = FilesystemDownloader()
        self.books = [b for b in handler.get_books(path=search_dir)]

        book_titles = "\n".join(b.title for b in self.books)
        self.textEdit.setText(book_titles)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    sys.exit(app.exec_())
