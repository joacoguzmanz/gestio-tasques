import sys
import ctypes
from PyQt5.QtCore import Qt, QEvent, QSize, QDate
from PyQt5.QtGui import QIcon, QFontDatabase, QFont, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QScrollArea

from view.dashboard.filters_dialog import FiltersDialog
# from view.dashboard.task_details_dialog import TaskDetailsDialog
from controller.task_manager_controller import remove_task_from_project_controller, get_task_due_today_controller, get_task_details_controller, get_tasks_by_priority_controller, get_project_id_by_name_controller, get_tasks_by_project_controller
from src.view.dashboard.signal_bus import global_signals

class Today(QWidget):
    def __init__(self):
        super().__init__()
        
        global_signals.taskAdded.connect(self.task_added)
        global_signals.filtersChanged.connect(self.filters_changed)
        
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
        right_layout.setAlignment(Qt.AlignTop)
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

    # def description_button_clicked(self, i):
    #     task_id = i
    #     self.task_details_dialog = TaskDetailsDialog(task_id=task_id)
    #     self.task_details_dialog.show()
    
    def clear_tasks_layout(self):
        # Mientras haya elementos en el layout...
        while self.tasks_layout.count() > 0:
            # Toma el primer elemento del layout
            item = self.tasks_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                # Solo eliminamos las tareas, no los widgets estáticos
                if widget != self.no_tasks_image and widget != self.no_tasks_text and widget != self.no_tasks_description:
                    widget.setParent(None)
                    widget.deleteLater()

    def task_added(self):
        self.clear_tasks_layout()

        ids_task_to_show = get_task_due_today_controller()
        if not ids_task_to_show:
            return
        inter_font = QFont("Inter")
        self.no_tasks_image.hide()
        self.no_tasks_text.hide()
        self.no_tasks_description.hide()

        self.tasks_layout.setContentsMargins(140, 0, 0, 100)
        self.tasks_layout.setSpacing(20)
        self.tasks_layout.setAlignment(Qt.AlignLeft)
        self.tasks_layout.setAlignment(Qt.AlignTop)

        def remove_task(checkbox, container, task_id):
            if checkbox.isChecked():
                # success = remove_task_from_project_controller(checkbox.text().strip(), checkbox)
                container.setParent(None)
                container.deleteLater()  # Elimina el widget de la memoria
                remaining_tasks = 0
                for i in range(self.tasks_layout.count()):
                    widget = self.tasks_layout.itemAt(i).widget()
                    # Supongamos que tus contenedores de tareas tienen un nombre o propiedad
                    if widget and widget.property("isTaskContainer"):
                        remaining_tasks += 1
                task_details  = get_task_details_controller(task_id)
                project_id = task_details["project_uuid"]
                uuid = task_details["uuid"]
                title = task_details["title"]
                description = task_details["description"]
                priority = task_details["priority"]

                remove_task_from_project_controller(project_id, task_id)
                if remaining_tasks == 0:
                    self.no_tasks_image.show()
                    self.no_tasks_text.show()
                    self.no_tasks_description.show()

        for i in (ids_task_to_show):
            single_task_container = QWidget()
            single_task_container.setProperty("isTaskContainer", True)
            container_layout = QVBoxLayout(single_task_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(2)

            task_details  = get_task_details_controller(i)
            project = task_details["project"]
            uuid = task_details["uuid"]
            title = task_details["title"]
            description = task_details["description"]
            priority = task_details["priority"]
            secondary_color = ""
            if priority == 1:
                priority = "red"
                secondary_color = "#f8d7da"
            elif priority == 2:
                priority = "orange"
                secondary_color = "#fbe7ce"
            elif priority == 3:
                priority = "blue"
                secondary_color = "#d1ecf1"
            elif priority == 4:
                priority = "black"
                secondary_color = "#d6d8d9"
            state = task_details["state"]
            due_date = task_details["due_date"]
            created_at = task_details["created_at"]

            task_checkbox = QCheckBox(title)
            task_checkbox.setFont(inter_font)
            task_checkbox.setStyleSheet(f"""
            QCheckBox::indicator {{
            width: 22.5px;
            height: 22.5px;
            border-radius: 12px;
            }}
            QCheckBox::indicator:unchecked {{
            border: 2px solid {priority};
            background-color: #ffffff;
            }}
            QCheckBox::indicator:unchecked:hover {{
            border: 2px solid {priority};
            background-color: {secondary_color};
            }}
            """)
            task_checkbox.setCursor(Qt.PointingHandCursor)
            task_checkbox.stateChanged.connect(
                lambda state, cb=task_checkbox, container=single_task_container, task_id=i: remove_task(cb, container, task_id=task_id)
            )

            self.checkbox_container = QHBoxLayout()
            self.checkbox_container.setContentsMargins(0, 0, 0, 0)
            self.checkbox_container.setSpacing(0)
            self.checkbox_container.setAlignment(Qt.AlignLeft)

            self.project = QLabel(project)
            self.project.setStyleSheet("font-size: 14px; color: grey; padding-left: 10px;")

            self.descripcion = QLabel(description)
            self.descripcion.setStyleSheet("font-size: 14px; color: grey; padding-left: 32px;")
            self.descripcion.setCursor(Qt.PointingHandCursor)
            # self.descripcion.mouseReleaseEvent = lambda event, i=i: self.description_button_clicked(i)

            self.checkbox_container.addWidget(task_checkbox)
            self.checkbox_container.addWidget(self.project)

            container_layout.addLayout(self.checkbox_container)
            container_layout.addWidget(self.descripcion)

            self.tasks_layout.addWidget(single_task_container)

    def filters_changed(self, priority_checked, priority_index, category_text):
        # Verifica si el checkbox de prioridad está activado
        ids_filtred = []
        ids_task_to_show = get_task_due_today_controller()
        if priority_checked:
            ids_filtred += get_tasks_by_priority_controller(0)
            ids_filtred += get_tasks_by_priority_controller(1)
            ids_filtred += get_tasks_by_priority_controller(2)
            ids_filtred += get_tasks_by_priority_controller(3)
            ids_filtred += get_tasks_by_priority_controller(4)
        priority_index = int(priority_index)
        if priority_index != 4:
            try:
                priority_index = int(priority_index)
            except ValueError:
                print("Error: priority_index no es un entero válido")
                return
            ids_filtred = get_tasks_by_priority_controller(priority_index + 1)
            ids_task_to_show = [task_id for task_id in ids_task_to_show if task_id in ids_filtred]
            # return get_tasks_by_priority_controller(priority_index)
        # Clicada la de mostrar solo proyecto X
        if category_text:
            id_project = get_project_id_by_name_controller(category_text)
            ids_filtred = get_tasks_by_project_controller(id_project)
            ids_task_to_show = [task_id for task_id in ids_task_to_show if task_id in ids_filtred]

        # if not priority_checked and not priority_index and not category_text:
        #     return

        self.clear_tasks_layout()

        # Filtrar las tareas que no están en ids_filtred
        if priority_checked:
            ids_task_to_show = [task_id for task_id in ids_filtred if task_id in get_task_due_today_controller()]
            
        if not ids_task_to_show:
            return
        inter_font = QFont("Inter")
        self.no_tasks_image.hide()
        self.no_tasks_text.hide()
        self.no_tasks_description.hide()

        self.tasks_layout.setContentsMargins(140, 0, 0, 100)
        self.tasks_layout.setSpacing(20)
        self.tasks_layout.setAlignment(Qt.AlignLeft)
        self.tasks_layout.setAlignment(Qt.AlignTop)

        def remove_task(checkbox, container, task_id):
            if checkbox.isChecked():
                # success = remove_task_from_project_controller(checkbox.text().strip(), checkbox)
                container.setParent(None)
                container.deleteLater()  # Elimina el widget de la memoria
                remaining_tasks = 0
                for i in range(self.tasks_layout.count()):
                    widget = self.tasks_layout.itemAt(i).widget()
                    # Supongamos que tus contenedores de tareas tienen un nombre o propiedad
                    if widget and widget.property("isTaskContainer"):
                        remaining_tasks += 1
                task_details  = get_task_details_controller(task_id)
                project_id = task_details["project_uuid"]
                uuid = task_details["uuid"]
                title = task_details["title"]
                description = task_details["description"]
                priority = task_details["priority"]

                remove_task_from_project_controller(project_id, task_id)
                if remaining_tasks == 0:
                    self.no_tasks_image.show()
                    self.no_tasks_text.show()
                    self.no_tasks_description.show()

        for i in (ids_task_to_show):
            single_task_container = QWidget()
            single_task_container.setProperty("isTaskContainer", True)
            container_layout = QVBoxLayout(single_task_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(2)

            task_details  = get_task_details_controller(i)
            project = task_details["project"]
            uuid = task_details["uuid"]
            title = task_details["title"]
            description = task_details["description"]
            priority = task_details["priority"]
            secondary_color = ""
            if priority == 1:
                priority = "red"
                secondary_color = "#f8d7da"
            elif priority == 2:
                priority = "orange"
                secondary_color = "#fbe7ce"
            elif priority == 3:
                priority = "blue"
                secondary_color = "#d1ecf1"
            elif priority == 4:
                priority = "black"
                secondary_color = "#d6d8d9"
            state = task_details["state"]
            due_date = task_details["due_date"]
            created_at = task_details["created_at"]

            task_checkbox = QCheckBox(title)
            task_checkbox.setFont(inter_font)
            task_checkbox.setStyleSheet(f"""
            QCheckBox::indicator {{
            width: 22.5px;
            height: 22.5px;
            border-radius: 12px;
            }}
            QCheckBox::indicator:unchecked {{
            border: 2px solid {priority};
            background-color: #ffffff;
            }}
            QCheckBox::indicator:unchecked:hover {{
            border: 2px solid {priority};
            background-color: {secondary_color};
            }}
            """)
            task_checkbox.setCursor(Qt.PointingHandCursor)
            task_checkbox.stateChanged.connect(
                lambda state, cb=task_checkbox, container=single_task_container, task_id=i: remove_task(cb, container, task_id=task_id)
            )

            self.checkbox_container = QHBoxLayout()
            self.checkbox_container.setContentsMargins(0, 0, 0, 0)
            self.checkbox_container.setSpacing(0)
            self.checkbox_container.setAlignment(Qt.AlignLeft)

            self.project = QLabel(project)
            self.project.setStyleSheet("font-size: 14px; color: grey; padding-left: 10px;")

            self.descripcion = QLabel(description)
            self.descripcion.setStyleSheet("font-size: 14px; color: grey; padding-left: 32px;")
            self.descripcion.setCursor(Qt.PointingHandCursor)
            # self.descripcion.mouseReleaseEvent = lambda event, i=i: self.description_button_clicked(i)

            self.checkbox_container.addWidget(task_checkbox)
            self.checkbox_container.addWidget(self.project)

            container_layout.addLayout(self.checkbox_container)
            container_layout.addWidget(self.descripcion)

            self.tasks_layout.addWidget(single_task_container)