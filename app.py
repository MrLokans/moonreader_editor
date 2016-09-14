import os
import sys
import logging

from moonreader_tools.handlers import FilesystemDownloader

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QAction,
    QFileDialog,
    QTextEdit,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QMenu
)

logger = logging.getLogger('GUI')

HOME_DIR = os.path.expanduser('~')
HOME_DIR = '{}/Dropbox/Books/.Moon+/Cache'.format(HOME_DIR)


BOOK_TABLE_COLUMNS = 4
BOOK_TABLE_HEADER = ['title', 'pages', 'percentage', 'notes']


class NumberTableItem(QTableWidgetItem):
    # This class should later be used for custom
    # table item sorting
    def __lt__(self, other):
        if isinstance(other, QTableWidgetItem):
            value = self.data(Qt.EditRole)
            other_value = other.data(Qt.EditRole)
            try:
                return float(value) < float(other_value)
            except (ValueError, TypeError):
                pass
        return super().__lt__(other)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.books = []
        self.initUI()

    def initUI(self):

        self.booksTable = QTableWidget(1, BOOK_TABLE_COLUMNS, parent=self)
        self.booksTable.setHorizontalHeaderLabels(BOOK_TABLE_HEADER)
        self.booksTable.setContextMenuPolicy(Qt.CustomContextMenu)

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.booksTable)
        self.statusBar()

        self.booksTable.customContextMenuRequested.connect(self.saveBookMenu)

        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(450, 450, 450, 400)
        self.setWindowTitle('Moonreader editor')

        self.show()

    def saveBookMenu(self, position):
        menu = QMenu()
        saveAction = menu.addAction("Save book")
        action = menu.exec_(self.booksTable.mapToGlobal(position))
        if action == saveAction:
            bookTableItem = self.booksTable.itemAt(position)
            bookRow = bookTableItem.row()

    def showDialog(self):
        search_dir = QFileDialog.getExistingDirectory(self, 'Open dir', HOME_DIR)
        handler = FilesystemDownloader()
        self.books = [b for b in handler.get_books(path=search_dir)]
        self.booksTable.setSortingEnabled(False)
        for indx, book in enumerate(self.books):
            table_rows = self.booksTable.rowCount()

            if indx >= table_rows:
                self.booksTable.insertRow(table_rows)

            self._fill_book_table_row(self.booksTable, indx, book)
        self.booksTable.setSortingEnabled(True)

    def _fill_book_table_row(self, table, index, book):
        title = QTableWidgetItem(book.title)
        pages = QTableWidgetItem(str(book.pages))
        percentage = QTableWidgetItem(str(book.percentage))
        notes = QTableWidgetItem(str(len(book.notes)))
        table.setItem(index, 0, title)
        table.setItem(index, 1, pages)
        table.setItem(index, 2, percentage)
        table.setItem(index, 3, notes)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    sys.exit(app.exec_())
