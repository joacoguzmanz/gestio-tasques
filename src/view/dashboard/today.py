import sys
import ctypes
from PyQt5.QtCore import Qt, QEvent, QSize, QDate
from PyQt5.QtGui import QIcon, QFontDatabase, QFont, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QScrollArea

from view.dashboard.filters_dialog import FiltersDialog

class Today(QWidget):
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

        self.title = QLabel("Hoy")
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

#######################################################

        self.no_tasks_image.hide()
        self.no_tasks_text.hide()
        self.no_tasks_description.hide()

        self.tasks_layout.setContentsMargins(140, 0, 0, 529)
        self.tasks_layout.setSpacing(20)
        self.tasks_layout.setAlignment(Qt.AlignLeft)
        self.tasks_layout.setAlignment(Qt.AlignTop)

        prioridad3 = "orange"

        def remove_task(checkbox):
            if checkbox.isChecked():
                checkbox.setParent(None)  # Elimina el widget del layout
                checkbox.deleteLater()  # Elimina el widget de la memoria
                remaining_tasks = 0
                for i in range(self.tasks_layout.count()):
                    widget = self.tasks_layout.itemAt(i).widget()
                    if isinstance(widget, QCheckBox):
                        remaining_tasks += 1
                if remaining_tasks == 0:
                    self.no_tasks_image.show()
                    self.no_tasks_text.show()
                    self.no_tasks_description.show()

        for i in range(1, 12):
            task_checkbox = QCheckBox(f"  Tarea {i}")
            task_checkbox.setFont(inter_font)
            task_checkbox.setStyleSheet(f"""
            QCheckBox::indicator {{
            width: 22.5px;
            height: 22.5px;
            border-radius: 12px;
            }}
            QCheckBox::indicator:unchecked {{
            border: 2px solid {prioridad3};
            background-color: #ffffff;
            }}
            QCheckBox::indicator:unchecked:hover {{
            border: 2px solid {prioridad3};
            background-color: #fbe7ce;
            }}
            """)
            task_checkbox.setCursor(Qt.PointingHandCursor)
            task_checkbox.stateChanged.connect(lambda state, checkbox=task_checkbox: remove_task(checkbox))
            self.tasks_layout.addWidget(task_checkbox)

        # Agregamos el layout de tareas a right_layout
        right_layout.addLayout(self.tasks_layout)

        # 4. Envolvemos todo right_widget en un QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        # Para que la barra aparezca en el lado izquierdo:
        scroll_area.setWidget(right_widget)

        # Agregamos únicamente el scroll_area al layout principal
        self.layout.addWidget(scroll_area)

    def show_filter_dialog(self):
        self.filter_dialog = FiltersDialog()
        self.filter_dialog.show()