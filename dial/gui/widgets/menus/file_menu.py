# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAction, QMenu

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class FileMenu(QMenu):
    """The class FileMenu provides a configured menu for the basic File operations
    (Open/Close/Save projects, exit program...)."""

    def __init__(self, parent: "QWidget" = None):
        super().__init__("&File", parent)

        # Add actions
        self._new_project_act = QAction("New project", self)
        self._new_project_act.setShortcut(QKeySequence.New)

        self._open_project_act = QAction("Open project", self)
        self._open_project_act.setShortcut(QKeySequence.Open)

        self._save_project_act = QAction("Save project", self)
        self._save_project_act.setShortcut(QKeySequence.Save)

        self._save_project_as_act = QAction("Save project as...", self)

        self._quit_act = QAction("Quit", self)
        self._quit_act.setShortcut(QKeySequence.Quit)

        # Configure menu
        self.addAction(self._new_project_act)
        self.addAction(self._open_project_act)
        self.addAction(self._save_project_act)
        self.addAction(self._save_project_as_act)
        self.addSeparator()
        self.addAction(self._quit_act)