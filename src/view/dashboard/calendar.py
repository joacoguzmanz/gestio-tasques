import sys
import ctypes
from PyQt5.QtCore import Qt, QEvent, QSize, QDate
from PyQt5.QtGui import QIcon, QFontDatabase, QFont, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox

from view.dashboard.filters_dialog import FiltersDialog

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

        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(140, 96, 0, 20)  # Reduce the top margin to decrease space
        top_layout.setSpacing(0)

        self.title = QLabel("Próximas tareas")
        self.title.setStyleSheet("font-size: 34px; font-weight: bold;")
        self.title.setFont(inter_font)
        top_layout.addWidget(self.title, 0, Qt.AlignTop)

        today = QDate.currentDate()
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        month = months[today.month() - 1]
        self.description = QLabel(today.toString(f"dddd, d 'de' {month} 'de' yyyy"))
        self.description.setFont(inter_font)
        top_layout.addWidget(self.description, 0, Qt.AlignTop)

        header_widget = QWidget()
        header_widget.setLayout(top_layout)
        header_widget.setFixedHeight(250)

        right_layout.addWidget(header_widget)

        self.tasks_layout = QVBoxLayout()
        self.tasks_layout.setContentsMargins(0, 0, 0, 350)
        self.tasks_layout.setSpacing(15)
        self.tasks_layout.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap("src/resources/images/today/not_tasks.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.no_tasks_image = QLabel()
        self.no_tasks_image.setPixmap(pixmap)
        self.no_tasks_image.setAlignment(Qt.AlignCenter)
        self.tasks_layout.addWidget(self.no_tasks_image)

        self.no_tasks_text = QLabel("No hay tareas para hoy")
        self.no_tasks_text.setStyleSheet("font-size: 24px;")
        self.no_tasks_text.setFont(inter_font)
        self.no_tasks_text.setAlignment(Qt.AlignCenter)
        self.tasks_layout.addWidget(self.no_tasks_text)

        self.no_tasks_description = QLabel("Puedes agregar tareas desde la opción de\nagregar tareas en la barra lateral")
        self.no_tasks_description.setStyleSheet("color: grey; font-size: 16px;")
        self.no_tasks_description.setFont(inter_font)
        self.no_tasks_description.setAlignment(Qt.AlignCenter)
        self.tasks_layout.addWidget(self.no_tasks_description)

        right_layout.addLayout(self.tasks_layout)

        self.layout.addWidget(right_widget)

    def show_filter_dialog(self):
        self.filter_dialog = FiltersDialog()
        self.filter_dialog.show()