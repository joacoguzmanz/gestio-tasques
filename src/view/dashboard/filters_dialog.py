import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QSizePolicy,
    QGraphicsDropShadowEffect, QWidget, QLineEdit, QFrame, QComboBox, QHBoxLayout, QCalendarWidget, QCheckBox
)
from PyQt5.QtCore import Qt, QPoint, QLocale, QDate, QSize
from PyQt5.QtGui import QColor, QFontDatabase, QFont, QIcon
import random

class FiltersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        font_id = QFontDatabase.addApplicationFont("src/resources/fonts/Inter-4.1/Inter.ttc")
        if font_id == -1:
            print("Error al cargar la fuente")
        else:
            print("Fuente cargada correctamente")

        # Configura el diálogo sin marco y con fondo transparente
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Tamaño del contenedor (contenido real) y márgenes para la sombra
        container_width, container_height = 300, 340
        self.setGeometry(1550, 100, 450, 725)
        self.setStyleSheet("background: transparent;")
        margin = 40  # Espacio para la sombra en cada lado
        self.resize(container_width + 2 * margin, container_height + 2 * margin)
        
        inter_font = QFont("Inter")
        
        # Layout principal del diálogo con márgenes
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(margin, margin, margin, margin)
        main_layout.setSpacing(0)
        
        # Crea el contenedor que tendrá el fondo blanco y border-radius
        self.container = QWidget(self)
        self.container.setFixedSize(container_width, container_height)
        self.container.setStyleSheet("background-color: #ffffff; border-radius: 30px;")
        
        # Aplica efecto de sombra al contenedor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.container.setGraphicsEffect(shadow)
        
        # Layout interno del contenedor (con márgenes internos)
        container_layout = QVBoxLayout(self.container)
        container_layout.setAlignment(Qt.AlignTop)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(10)
        
        self.order_label = QLabel("Ordenar por:", self.container)
        self.order_label.setStyleSheet("border: none; border-radius: 5px; padding: 0px; font-size: 15px;")
        self.order_label.setFont(inter_font)
        self.order_label.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.order_label)

        self.priority_checkbox = QCheckBox("Prioridad", self.container)
        self.priority_checkbox.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px; font-size: 18px;")
        self.priority_checkbox.setFont(inter_font)
        self.priority_checkbox.setFixedHeight(54)
        self.priority_checkbox.setFixedWidth(250)
        container_layout.addWidget(self.priority_checkbox)

        self.show_only_label = QLabel("Mostrar solo:", self.container)
        self.show_only_label.setStyleSheet("border: none; border-radius: 5px; padding: 0px; font-size: 15px;")
        self.show_only_label.setFont(inter_font)
        self.show_only_label.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.show_only_label)
        
        # Layout para el botón de calendario y el combobox
        combo_layout = QVBoxLayout()
        combo_layout.setAlignment(Qt.AlignLeft)
        
        self.combo_box2 = QComboBox(self.container)
        self.combo_box2.addItem(QIcon("src/resources/images/add_task/red_flag.svg"), "Prioridad 1")
        self.combo_box2.addItem(QIcon("src/resources/images/add_task/orange_flag.svg"), "Prioridad 2")
        self.combo_box2.addItem(QIcon("src/resources/images/add_task/blue_flag.svg"), "Prioridad 3")
        self.combo_box2.addItem(QIcon("src/resources/images/add_task/white_flag.svg"), "Prioridad 4")
        self.combo_box2.addItem(QIcon("src/resources/images/add_task/black_flag.svg"), "Todas")
        self.combo_box2.setCurrentIndex(4)  # Establecer la prioridad 4 como predeterminada
        self.combo_box2.setFixedHeight(54)
        self.combo_box2.setFixedWidth(250)
        self.combo_box2.setStyleSheet("""
            QComboBox {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            font-size: 18px;
            }
            QComboBox:hover {
                background-color: #f0f0f0;
            }
            QComboBox QAbstractItemView {
                background-color: #7F8C8D;  /* Color de fondo del menú desplegable */
                color: #ECF0F1;  /* Color del texto en el menú */
                selection-background-color: #2C3E50;
                selection-color: #ECF0F1;  /* Color del texto del elemento seleccionado */
                border-radius: 5px;  /* Bordes redondeados */
                outline: none;  /* Evitar el contorno */
                padding: 5px;
                spacing: 10px;  /* Espaciado entre las opciones */
            }
            QComboBox QAbstractItemView::item {
                padding-left: 15px;  /* Espaciado interno izquierdo */
                padding-right: 15px;  /* Espaciado interno derecho */
                padding-top: 10px;  /* Espaciado interno superior */
                padding-bottom: 10px;  /* Espaciado interno inferior */
            }
            QComboBox::drop-down {
                border: 0px;
            }
        """)
        self.combo_box2.setCursor(Qt.PointingHandCursor)
        self.combo_box2.setFont(inter_font)
        combo_layout.addWidget(self.combo_box2)

        self.category_text = QLineEdit(self.container)
        category_placeholders = [
            "#Universidad", "#Trabajo", "#Personal", "#Salud", "#Finanzas",
            "#Hogar", "#Compras", "#Viajes", "#Deportes", "#Ocio",
            "#Familia", "#Amigos", "#Estudios", "#Proyecto", "#Reunión",
            "#Cita", "#Evento", "#Tarea", "#Recordatorio", "#Meta"
        ]
        self.category_text.setPlaceholderText(random.choice(category_placeholders))
        self.category_text.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px; font-size: 18px;")
        self.category_text.setFont(inter_font)
        self.category_text.setFixedHeight(54)
        self.category_text.setFixedWidth(250)
        self.category_text.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.category_text.textChanged.connect(self.ensure_hashtag)
        combo_layout.addWidget(self.category_text)

        container_layout.addLayout(combo_layout)  # Agrega los elementos en una fila
        
        # Botón de cerrar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignRight)
        button_layout.setContentsMargins(0, 0, 10, 0)  # Agrega padding right de 5px
        
        self.close_button = QPushButton("Cancelar", self.container)
        self.close_button.setStyleSheet("""
            QPushButton {
            background-color: #f5f5f5;
            color: #4d4d4d;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            }
            QPushButton:hover {
            background-color: #e0e0e0;
            }
            QPushButton:pressed {
            background-color: #dadada;
            }
        """)
        self.close_button.setFont(inter_font)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button, alignment=Qt.AlignRight)
        
        self.apply_button = QPushButton("Aplicar", self.container)
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #c53b3d;
                color: #fff;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #b43334;
            }
            QPushButton:pressed {
                background-color: #a32a2b;
            }
        """)
        self.apply_button.setFont(inter_font)
        self.apply_button.setCursor(Qt.PointingHandCursor)
        # self.apply_button.clicked.connect()
        button_layout.addWidget(self.apply_button, alignment=Qt.AlignRight)
        
        container_layout.addLayout(button_layout)
        
        # Agrega el contenedor al layout principal centrado
        main_layout.addWidget(self.container, alignment=Qt.AlignCenter)

    def ensure_hashtag(self):
        text = self.category_text.text()
        if text and not text.startswith("#"):
            self.category_text.setText("#" + text.lstrip("#"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = FiltersDialog()
    popup.exec_()
    sys.exit(0)
