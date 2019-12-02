# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""The main window for the program."""

from PySide2.QtCore import QSize
from PySide2.QtWidgets import (QApplication, QMainWindow, QPushButton,
                               QTabWidget)

from tfg.gui.mainwindow.mainmenubar import MainMenuBar
from tfg.gui.widgets.log import LoggerDialog
from tfg.gui.widgets.windows import DatasetsWindow
from tfg.utils import log


class MainWindow(QMainWindow):
    """
    The main window for the program.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__main_menu_bar = MainMenuBar(self)
        self.__tabs_widget = QTabWidget(self)

        self.__setup_ui()

        log.mainwindow.info("Program Initialized")

    def __setup_ui(self):
        # Widget configuration
        self.setWindowTitle("TFG")

        self.setMenuBar(self.__main_menu_bar)
        self.setStatusBar(self.statusBar())

        # self.statusBar().addPermanentWidget(QPushButton("Log"))

        self.setCentralWidget(self.__tabs_widget)

        # Tab widget
        self.__tabs_widget.addTab(DatasetsWindow(self), "Datasets")

        # Connections
        self.__main_menu_bar.quit.connect(QApplication.quit)
        self.__main_menu_bar.toggle_log_window.connect(self.__toggle_log_window)

    def sizeHint(self):
        return QSize(800, 600)

    def __toggle_log_window(self):
        dialog = LoggerDialog(self)

        dialog.show()