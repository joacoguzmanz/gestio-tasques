import sys
import ctypes
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

class SideBar(QWidget):
    def __init__(self):
        super().__init__()
        # Asigna directamente el layout a self
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # Crear un widget contenedor para las dos columnas y su layout
        columns_widget = QWidget(self)  # Puedes pasar self como parent
        columns_layout = QHBoxLayout(columns_widget)
        columns_layout.setContentsMargins(0, 0, 0, 0)
        columns_layout.setSpacing(0)

        # Widget contenedor para la columna negra
        left_widget = QWidget(columns_widget)
        left_widget.setStyleSheet("background-color: #fcfaf8;")
        left_widget.setFixedWidth(400)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 175, 10, 10)
        left_layout.setSpacing(25)
        left_layout.setAlignment(Qt.AlignTop)

        # Widget contenedor para la columna roja
        right_widget = QWidget(columns_widget)
        right_widget.setStyleSheet("background-color: #ffffff;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)

        # Agregar las columnas al layout de columnas
        columns_layout.addWidget(left_widget)
        columns_layout.addWidget(right_widget)

        # Agregar el widget de columnas al layout principal
        self.layout.addWidget(columns_widget)

        # Ejemplo: Agregar algunos widgets a la columna negra
        left_layout.addWidget(QPushButton("Botón Negro 1"))
        left_layout.addWidget(QPushButton("Botón Negro 2"))

        # Ejemplo: Agregar algunos widgets a la columna roja
        right_layout.addWidget(QPushButton("Botón Rojo 1"))
        right_layout.addWidget(QPushButton("Botón Rojo 2"))
