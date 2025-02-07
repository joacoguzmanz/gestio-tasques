import sys
import ctypes
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QFontDatabase, QFont, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from view.dashboard.add_task_dialog import AddTaskDialog

class SideBar(QWidget):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont("src/resources/fonts/Inter-4.1/Inter.ttc")
        if font_id == -1:
            print("Error al cargar la fuente")
        else:
            print("Fuente cargada correctamente")

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
        left_layout.setContentsMargins(20, 50, 10, 10)
        left_layout.setSpacing(20)
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

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

        # Fuente usada
        inter_font = QFont("Inter")

        # user
        user_button_layout = QHBoxLayout()
        user_button_layout.setAlignment(Qt.AlignLeft)
        user_button_layout.setContentsMargins(0, 0, 0, 50)
        
        user_button_container = QWidget()
        user_button_container.setStyleSheet("background-color: transparent; border-radius: 10px;")  # Color de fondo con bordes redondeados
        user_button_container.setLayout(user_button_layout) 
        # user_button_container.mousePressEvent = self.add_task_clicked
        
        user_button = QLabel("Ignacio López Aylagas")
        user_button.setStyleSheet("color: black; border: none; font-size: 18px;")
        user_button.setFont(inter_font)

        user_button_pixmap = QPixmap("src/resources/images/sidebar/user.jpg")
        user_button_pixmap = user_button_pixmap.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Create a circular mask
        mask = QPixmap(user_button_pixmap.size())
        mask.fill(Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.drawEllipse(0, 0, mask.width(), mask.height())
        painter.end()

        # Apply the mask to the pixmap
        user_button_pixmap.setMask(mask.createMaskFromColor(Qt.transparent, Qt.MaskInColor))
        user_button_label = QLabel()
        user_button_label.setPixmap(user_button_pixmap.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Set the size of the pixmap

        user_button_layout.addWidget(user_button_label)
        user_button_layout.addSpacing(10)  # Reduce the space between the image and the text
        user_button_layout.addWidget(user_button)

        left_layout.addWidget(user_button_container)

        # add Task 
        add_task_button_layout = QHBoxLayout()
        add_task_button_layout.setAlignment(Qt.AlignLeft)
        add_task_button_layout.setContentsMargins(0, 0, 0, 0)
        
        add_task_button_container = QWidget()
        add_task_button_container.setStyleSheet("""
            QWidget {
            background-color: transparent;
            border-radius: 10px;
            padding: 10px 45px; /* Aumenta el área de interacción */
            }
            QWidget:hover {
            background-color: #e0e0e0; /* Color grisáceo */
            }
            QWidget:pressed {
            background-color: #c0c0c0; /* Color al mantener el click izquierdo */
            }
        """)
        add_task_button_container.setCursor(Qt.PointingHandCursor)
        add_task_button_container.setLayout(add_task_button_layout) 
        add_task_button_container.mouseReleaseEvent = self.add_task_clicked
        
        add_task_button = QLabel("Añadir Tarea")
        add_task_button.setStyleSheet("color: #a81f00; border: none; font-size: 18px; font-weight: bold;")
        add_task_button.setFont(inter_font)

        add_task_button_pixmap = QPixmap("src/resources/images/sidebar/addTask.png")
        add_task_button_label = QLabel()
        add_task_button_label.setPixmap(add_task_button_pixmap.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Set the size of the pixmap

        add_task_button_layout.addWidget(add_task_button_label)
        add_task_button_layout.addSpacing(10)  # Reduce the space between the image and the text
        add_task_button_layout.addWidget(add_task_button)

        left_layout.addWidget(add_task_button_container)

        # today

        today_button_layout = QHBoxLayout()
        today_button_layout.setAlignment(Qt.AlignLeft)
        today_button_layout.setContentsMargins(0, 0, 0, 0)
        # today_button_layout.mousePressEvent = self.today_clicked

        today_button_container = QWidget()
        today_button_container.setStyleSheet("""
            QWidget {
            background-color: transparent;
            border-radius: 10px;
            padding: 10px 45px; /* Aumenta el área de interacción */
            }
            QWidget:hover {
            background-color: #e0e0e0; /* Color grisáceo */
            }
            QWidget:pressed {
            background-color: #c0c0c0; /* Color al mantener el click izquierdo */
            }
        """)
        today_button_container.setLayout(today_button_layout) 

        today_button = QLabel("Hoy")
        today_button.setStyleSheet("color: black; border: none; font-size: 18px;")
        today_button.setFont(inter_font)

        today_button_pixmap = QPixmap("src/resources/images/sidebar/today.png")
        today_button_label = QLabel()
        today_button_label.setPixmap(today_button_pixmap.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Set the size of the pixmap

        today_button_layout.addWidget(today_button_label)
        today_button_layout.addSpacing(10)  # Reduce the space between the image and the text
        today_button_layout.addWidget(today_button)

        left_layout.addWidget(today_button_container)

        # calendar
        
        calendar_button_layout = QHBoxLayout()
        calendar_button_layout.setAlignment(Qt.AlignLeft)
        calendar_button_layout.setContentsMargins(0, 0, 0, 0)
        # calendar_button_layout.mousePressEvent = self.calendar_clicked

        calendar_button_container = QWidget()
        calendar_button_container.setStyleSheet("""
            QWidget {
            background-color: transparent;
            border-radius: 10px;
            padding: 10px 45px; /* Aumenta el área de interacción */
            }
            QWidget:hover {
            background-color: #e0e0e0; /* Color grisáceo */
            }
            QWidget:pressed {
            background-color: #c0c0c0; /* Color al mantener el click izquierdo */
            }
        """)
        calendar_button_container.setLayout(calendar_button_layout) 

        calendar_button = QLabel("Calendario")
        calendar_button.setStyleSheet("color: black; border: none; font-size: 18px;")
        calendar_button.setFont(inter_font)

        calendar_button_pixmap = QPixmap("src/resources/images/sidebar/calendar.png")
        calendar_button_label = QLabel()
        calendar_button_label.setPixmap(calendar_button_pixmap.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Set the size of the pixmap

        calendar_button_layout.addWidget(calendar_button_label)
        calendar_button_layout.addSpacing(10)  # Reduce the space between the image and the text
        calendar_button_layout.addWidget(calendar_button)

        left_layout.addWidget(calendar_button_container)

        # Ejemplo: Agregar algunos widgets a la columna roja
        right_layout.addWidget(QPushButton("Botón Rojo 1"))
        right_layout.addWidget(QPushButton("Botón Rojo 2"))


    def add_task_clicked(self, event):
        if event.button() == Qt.LeftButton:
            print("Add task clicked")
            self.add_task_dialog = AddTaskDialog()
            self.add_task_dialog.show()