import sys
import ctypes
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QFontDatabase, QFont, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from view.dashboard.add_task_dialog import AddTaskDialog
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal

class SideBar(QWidget):
    switch_to_calendar = pyqtSignal()
    switch_to_today = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setFixedWidth(400)

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
        self.columns_widget = QWidget(self)  # Puedes pasar self como parent
        self.columns_layout = QHBoxLayout(self.columns_widget)
        self.columns_layout.setContentsMargins(0, 0, 0, 0)
        self.columns_layout.setSpacing(0)

        # Widget contenedor para la columna negra
        left_widget = QWidget(self.columns_widget)
        left_widget.setStyleSheet("background-color: #fcfaf8;")
        left_widget.setFixedWidth(400)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(20, 20, 10, 10)
        left_layout.setSpacing(20)
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Widget contenedor para la columna roja

        # Agregar las columnas al layout de columnas
        self.columns_layout.addWidget(left_widget)

        self.selected_option = "today"

        # Agregar el widget de columnas al layout principal
        self.layout.addWidget(self.columns_widget)

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
        user_button_pixmap = user_button_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation)

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
        user_button_label.setPixmap(user_button_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Set the size of the pixmap

        user_button_layout.addWidget(user_button_label)
        user_button_layout.addSpacing(10)  # Reduce the space between the image and the text
        user_button_layout.addWidget(user_button)

        left_layout.addWidget(user_button_container)

        # add Task 
        add_task_button_layout = QHBoxLayout()
        add_task_button_layout.setAlignment(Qt.AlignLeft)
        add_task_button_layout.setContentsMargins(0, 0, 180, 0)
        
        self.add_task_button_container = QWidget()
        self.add_task_button_container.setStyleSheet("""
            QWidget {
            background-color: transparent;
            border-radius: 10px;
            padding: 10px; /* Aumenta el área de interacción */
            }
            QWidget:hover {
            background-color: #e0e0e0; /* Color grisáceo */
            }
        """)
        self.add_task_button_container.setCursor(Qt.PointingHandCursor)
        self.add_task_button_container.setLayout(add_task_button_layout)
        self.add_task_button_container.mousePressEvent = self.add_task_button_pressed
        self.add_task_button_container.mouseReleaseEvent = self.add_task_button_clicked
        
        add_task_button = QLabel("Añadir Tarea")
        add_task_button.setStyleSheet("color: #a81f00; border: none; font-size: 18px; font-weight: bold;")
        add_task_button.setFont(inter_font)

        add_task_button_pixmap = QPixmap("src/resources/images/sidebar/addTask.svg")
        add_task_button_label = QLabel()
        add_task_button_label.setPixmap(add_task_button_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Set the size of the pixmap

        add_task_button_layout.addWidget(add_task_button_label)
        add_task_button_layout.addSpacing(-15)  # Reduce the space between the image and the text
        add_task_button_layout.addWidget(add_task_button)

        left_layout.addWidget(self.add_task_button_container)

        # today

        self.today_button_layout = QHBoxLayout()
        self.today_button_layout.setAlignment(Qt.AlignLeft)
        self.today_button_layout.setContentsMargins(0, 0, 200, 0)
        # self.today_button_layout.mousePressEvent = self.today_clicked

        self.today_button_container = QWidget()
        self.today_button_container.setStyleSheet("""
            QWidget {
                background-color: #ffefe5;
                border-radius: 10px;
                padding: 10px; /* Aumenta el área de interacción */
            }
        """)
        self.today_button_container.setCursor(Qt.PointingHandCursor)
        self.today_button_container.setLayout(self.today_button_layout) 
        self.today_button_container.mousePressEvent = self.today_button_pressed
        self.today_button_container.mouseReleaseEvent = self.today_button_clicked

        self.today_button = QLabel("Hoy")
        self.today_button.setStyleSheet("color: #a81f00; border: none; font-size: 18px;")
        self.today_button.setFont(inter_font)

        self.today_button_pixmap = QPixmap("src/resources/images/sidebar/today_selected.svg")
        self.today_button_label = QLabel()
        self.today_button_label.setPixmap(self.today_button_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.today_button_layout.addWidget(self.today_button_label)
        self.today_button_layout.addSpacing(-15)  # Reduce the space between the image and the text
        self.today_button_layout.addWidget(self.today_button)

        left_layout.addWidget(self.today_button_container)

        # calendar
        
        self.calendar_button_layout = QHBoxLayout()
        self.calendar_button_layout.setAlignment(Qt.AlignLeft)
        self.calendar_button_layout.setContentsMargins(0, 0, 200, 0)
        # self.calendar_button_layout.mousePressEvent = self.calendar_clicked

        self.calendar_button_container = QWidget()
        self.calendar_button_container.setStyleSheet("""
            QWidget {
            background-color: transparent;
            border-radius: 10px;
            padding: 10px; /* Aumenta el área de interacción */
            }
            QWidget:hover {
            background-color: #e0e0e0; /* Color grisáceo */
            }
        """)
        self.calendar_button_container.setCursor(Qt.PointingHandCursor)
        self.calendar_button_container.setLayout(self.calendar_button_layout)
        self.calendar_button_container.mousePressEvent = self.calendar_button_pressed
        self.calendar_button_container.mouseReleaseEvent = self.calendar_button_clicked 

        self.calendar_button = QLabel("Próximos")
        self.calendar_button.setStyleSheet("color: black; border: none; font-size: 18px;")
        self.calendar_button.setFont(inter_font)

        self.calendar_button_pixmap = QPixmap("src/resources/images/sidebar/calendar.svg")
        self.calendar_button_label = QLabel()
        self.calendar_button_label.setPixmap(self.calendar_button_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Set the size of the pixmap

        self.calendar_button_layout.addWidget(self.calendar_button_label)
        self.calendar_button_layout.addSpacing(-15)  # Reduce the space between the image and the text
        self.calendar_button_layout.addWidget(self.calendar_button)

        left_layout.addWidget(self.calendar_button_container)

    def add_task_button_pressed(self, event):
        if event.button() == Qt.LeftButton:
            self.add_task_button_container.setStyleSheet("""
                QWidget {
                    background-color: #dadada;
                    border-radius: 10px;
                    padding: 10px; /* Aumenta el área de interacción */
                }
            """)

    def add_task_button_clicked(self, event):
        if event.button() == Qt.LeftButton:
            print("Add task clicked")
            self.add_task_button_container.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border-radius: 10px;
                    padding: 10px; /* Aumenta el área de interacción */
                }
                QWidget:hover {
                    background-color: #e0e0e0; /* Color grisáceo */
                }
            """)
            self.add_task_dialog = AddTaskDialog()
            self.add_task_dialog.show()

    def today_button_pressed(self, event):
        if event.button() == Qt.LeftButton:
            if self.selected_option != "today":
                self.today_button_container.setStyleSheet("""
                    QWidget {
                        background-color: #dadada;
                        border-radius: 10px;
                        padding: 10px; /* Aumenta el área de interacción */
                    }
                """)

    def today_button_clicked(self, event):
        if event.button() == Qt.LeftButton:
            print("today changed")
            self.today_button_container.setStyleSheet("""
                QWidget {
                    background-color: #ffefe5;
                    border-radius: 10px;
                    padding: 10px; /* Aumenta el área de interacción */
                }
            """)
            self.calendar_button_container.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border-radius: 10px;
                    padding: 10px; /* Aumenta el área de interacción */
                }
                QWidget:hover {
                    background-color: #e0e0e0; /* Color grisáceo */
                }
            """)
            self.calendar_button_pixmap = QPixmap("src/resources/images/sidebar/calendar.svg")
            self.calendar_button_label.setPixmap(self.calendar_button_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.today_button_pixmap = QPixmap("src/resources/images/sidebar/today_selected.svg")
            self.today_button_label.setPixmap(self.today_button_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.calendar_button.setStyleSheet("color: black; border: none; font-size: 18px;")
            self.today_button.setStyleSheet("color: #a81f00; border: none; font-size: 18px;")
            self.selected_option = "today"
            self.switch_to_today.emit()

    def calendar_button_pressed(self, event):
        if event.button() == Qt.LeftButton:
            if self.selected_option != "calendar":
                self.calendar_button_container.setStyleSheet("""
                    QWidget {
                        background-color: #dadada;
                        border-radius: 10px;
                        padding: 10px; /* Aumenta el área de interacción */
                    }
                """)

    def calendar_button_clicked(self, event):
        if event.button() == Qt.LeftButton:
            print("Add task clicked")
            self.calendar_button_container.setStyleSheet("""
                QWidget {
                    background-color: #ffefe5;
                    border-radius: 10px;
                    padding: 10px; /* Aumenta el área de interacción */
                }
            """)
            self.today_button_container.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border-radius: 10px;
                    padding: 10px; /* Aumenta el área de interacción */
                }
                QWidget:hover {
                    background-color: #e0e0e0; /* Color grisáceo */
                }
            """)
            self.today_button_pixmap = QPixmap("src/resources/images/sidebar/today.svg")
            self.today_button_label.setPixmap(self.today_button_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.calendar_button_pixmap = QPixmap("src/resources/images/sidebar/calendar_selected.svg")
            self.calendar_button_label.setPixmap(self.calendar_button_pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.today_button.setStyleSheet("color: black; border: none; font-size: 18px;")
            self.calendar_button.setStyleSheet("color: #a81f00; border: none; font-size: 18px;")
            self.selected_option = "calendar"
            self.switch_to_calendar.emit()