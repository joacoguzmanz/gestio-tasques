import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QSizePolicy,
    QGraphicsDropShadowEffect, QWidget, QLineEdit, QFrame, QComboBox, QHBoxLayout, QCalendarWidget, QCheckBox
)
from PyQt5.QtCore import Qt, QPoint, QLocale, QDate, QSize
from PyQt5.QtGui import QColor, QFontDatabase, QFont, QIcon
import random

class TaskDetailsDialog(QDialog):
    def __init__(self, parent=None, task_id=0):
        super().__init__(parent)

        font_id = QFontDatabase.addApplicationFont("src/resources/fonts/Inter-4.1/Inter.ttc")
        if font_id == -1:
            print("Error al cargar la fuente")
        else:
            print("Fuente cargada correctamente")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Configuración principal del layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)  # Margen para la sombra
        main_layout.setSpacing(0)
        
        # Contenedor principal
        self.container = QWidget()
        self.container.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 30px;
        """)
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Efecto de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.container.setGraphicsEffect(shadow)
        
        # Layout interno del contenedor
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(15)
        
        # Fuente personalizada
        inter_font = QFont("Inter")
        
        # Título
        self.order_label = QLabel("Tarea 1")
        self.order_label.setStyleSheet("font-size: 24px;")
        self.order_label.setFont(inter_font)

        self.close_dialog = QPushButton("✕")
        self.close_dialog.setStyleSheet("""
            QPushButton {
            color: grey;
            border: none;
            background-color: transparent;
            font-size: 24px;
            }
            QPushButton:hover {
            color: black;
            }
        """)
        self.close_dialog.setCursor(Qt.PointingHandCursor)
        self.close_dialog.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.close_dialog.setMaximumWidth(30)
        self.close_dialog.setMaximumHeight(30)
        self.close_dialog.clicked.connect(self.close)

        self.titlebar = QHBoxLayout()
        self.titlebar.setContentsMargins(0, 0, 0, 0)
        self.titlebar.addWidget(self.order_label)
        self.titlebar.addWidget(self.close_dialog)
        container_layout.addLayout(self.titlebar)
        
        # Descripción
        self.show_only_label = QLabel(
            "Esta es una descripción de la tarea que es bastante larga para probar cómo se comporta el texto cuando es demasiado grande para caber en la ventana."
        )
        self.show_only_label.setStyleSheet("color: grey; font-size: 18px;")
        self.show_only_label.setFont(inter_font)
        self.show_only_label.setWordWrap(True)
        self.show_only_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        container_layout.addWidget(self.show_only_label)
        
        # Añadir contenedor al layout principal
        main_layout.addWidget(self.container)

        # Ajustar tamaño mínimo basado en el contenido
        self.adjustSize()

    def ensure_hashtag(self):
        text = self.category_text.text()
        if text and not text.startswith("#"):
            self.category_text.setText("#" + text.lstrip("#"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = TaskDetailsDialog()
    popup.exec_()
    sys.exit(0)