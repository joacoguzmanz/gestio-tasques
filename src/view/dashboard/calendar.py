import sys
import ctypes
from PyQt5.QtCore import Qt, QEvent, QSize
from PyQt5.QtGui import QIcon, QFontDatabase, QFont, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from view.dashboard.filters_dialog import FiltersDialog
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

class Calendar(QWidget):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont("src/resources/fonts/Inter-4.1/Inter.ttc")
        if font_id == -1:
            print("Error al cargar la fuente")
        else:
            print("Fuente cargada correctamente")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        inter_font = QFont("Inter")

        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #ffffff;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(0)

        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 20, 40, 0)
        filter_layout.setSpacing(15)

        self.filter = QPushButton("Filtros")
        self.filter.setStyleSheet("""
            QPushButton {
            padding: 10px;
            border: none;
            border-radius: 5px; 
            background-color: #ffffff;
            color: #1a1a1a;
            font-size: 20px;
            }
            QPushButton:hover {
            background-color: #e0e0e0;
            }
            QPushButton:pressed {
            background-color: #dadada;
            }
        """)
        self.filter.setFont(inter_font)
        self.filter.setCursor(Qt.PointingHandCursor)
        self.filter.clicked.connect(self.show_filter_dialog)

        filter_icon = QIcon("src/resources/images/today/filter.svg")  # Cambia esto por la ruta real de tu imagen
        self.filter.setIcon(filter_icon)
        self.filter.setIconSize(QSize(30, 30))

        filter_layout.addWidget(self.filter, 0, Qt.AlignRight)

        right_layout.addLayout(filter_layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(140, 95, 0, 0)
        top_layout.setSpacing(0)
        self.title = QLabel("Próximos")
        self.title.setStyleSheet("font-size: 34px; font-weight: bold;")
        self.title.setFont(inter_font)
        top_layout.addWidget(self.title, 0, Qt.AlignTop)
        right_layout.addLayout(top_layout)

        self.layout.addWidget(right_widget)

    def show_filter_dialog(self):
        self.filter_dialog = FiltersDialog()
        self.filter_dialog.show()