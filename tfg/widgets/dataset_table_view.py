# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHeaderView, QStyleOptionViewItem, QTableView


class DatasetTableView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)