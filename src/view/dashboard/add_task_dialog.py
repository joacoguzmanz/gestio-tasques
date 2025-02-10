import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QSizePolicy,
    QGraphicsDropShadowEffect, QWidget, QLineEdit, QFrame, QComboBox, QHBoxLayout, QCalendarWidget
)
from PyQt5.QtCore import Qt, QPoint, QLocale, QDate, QSize
from PyQt5.QtGui import QColor, QFontDatabase, QFont, QIcon
import random

# from managers.task_manager import TaskManager

class AddTaskDialog(QDialog):
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
        container_width, container_height = 800, 275
        self.setGeometry(550, 100, 450, 725)
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
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(10)

        self.text_container = QVBoxLayout()
        self.text_container.setContentsMargins(0, 0, 0, 0)
        self.text_container.setSpacing(5)
        self.text_container.setAlignment(Qt.AlignTop)
        
        self.title_input = QLineEdit(self.container)
        placeholder_texts = [
            "Revisar la tesis mañana a la mañana",
            "Comprar ingredientes para la cena",
            "Llamar al médico para una cita",
            "Enviar el informe semanal",
            "Preparar la presentación del proyecto",
            "Estudiar para el examen de matemáticas",
            "Limpiar la casa el fin de semana",
            "Actualizar el currículum vitae",
            "Leer el libro de desarrollo personal",
            "Hacer ejercicio en el gimnasio",
            "Planificar las vacaciones de verano",
            "Organizar la fiesta de cumpleaños",
            "Pagar las facturas mensuales",
            "Revisar y responder correos electrónicos",
            "Asistir a la reunión de equipo",
            "Desarrollar nuevas funcionalidades para el proyecto",
            "Realizar una copia de seguridad de los datos",
            "Aprender un nuevo idioma",
            "Cocinar una receta nueva",
            "Meditar durante 20 minutos",
            "Hacer una lista de objetivos para el mes",
            "Visitar a la familia el domingo",
            "Reparar el coche",
            "Ir de compras para el hogar",
            "Escribir un artículo para el blog",
            "Actualizar el software del ordenador",
            "Hacer una llamada de seguimiento a un cliente",
            "Asistir a un seminario web",
            "Investigar sobre nuevas tendencias del mercado",
            "Realizar una auditoría interna",
            "Configurar el nuevo dispositivo móvil",
            "Planificar la estrategia de marketing",
            "Revisar el código fuente del proyecto",
            "Hacer una limpieza de primavera",
            "Organizar los documentos importantes",
            "Preparar el almuerzo para la semana",
            "Hacer una donación a una organización benéfica",
            "Participar en un evento de networking",
            "Actualizar el perfil de LinkedIn",
            "Revisar las finanzas personales",
            "Hacer una lista de compras",
            "Asistir a una clase de yoga",
            "Revisar el contrato de trabajo",
            "Hacer una encuesta de satisfacción a los clientes",
            "Planificar una salida con amigos",
            "Revisar el plan de estudios",
            "Hacer una revisión médica anual",
            "Organizar el escritorio de trabajo",
            "Actualizar la página web del proyecto"
        ]
        self.title_input.setPlaceholderText(random.choice(placeholder_texts))
        self.title_input.setStyleSheet("border: none; border-radius: 5px; padding: 15px; font-size: 24px;")
        self.title_input.setFont(inter_font)
        self.title_input.textChanged.connect(self.add_task_button_available)
        self.text_container.addWidget(self.title_input)

        self.description_input = QLineEdit(self.container)
        self.description_input.setPlaceholderText("Descripción")
        self.description_input.setStyleSheet("border: none; border-radius: 5px; padding-left: 15px; font-size: 14px;")
        self.description_input.setFont(inter_font)
        self.text_container.addWidget(self.description_input)

        container_layout.addLayout(self.text_container)
        
        # Layout para el botón de calendario y el combobox
        combo_layout = QHBoxLayout()
        combo_layout.setAlignment(Qt.AlignLeft)
        
        self.calendar_button = QPushButton(" Hoy", self.container)  # Añadir espacio antes del texto
        self.calendar_button.setFixedWidth(110)  # Ajustar el ancho del botón
        self.calendar_button.setFixedHeight(54)
        self.calendar_button.clicked.connect(self.show_calendar)

        icon = QIcon("src/resources/images/add_task/green_date.svg")  # Cambia esto por la ruta real de tu imagen
        self.calendar_button.setIcon(icon)
        self.calendar_button.setIconSize(QSize(24, 24))

        self.calendar_button.setStyleSheet("""
            QPushButton {
            border: 1px solid #ccc; 
            border-radius: 5px; 
            padding: 10px; 
            font-size: 18px;
            color: #058527;
            }
            QPushButton:hover {
            background-color: #e0e0e0;
            }
        """)
        self.calendar_button.setFont(inter_font)
        self.calendar_button.setCursor(Qt.PointingHandCursor)
        combo_layout.addWidget(self.calendar_button)

        # Crear un QFrame flotante para el calendario
        self.calendar_frame = QFrame(self)
        self.calendar_frame.setStyleSheet("background-color: transparent; border: none;")
        self.calendar_frame.setFixedSize(600, 480)  # Ajustar tamaño del calendario
        self.calendar_frame.hide()  # Ocultarlo inicialmente
        
        # Crear el calendario dentro del frame
        self.calendar = QCalendarWidget(self.calendar_frame)
        self.calendar.setFirstDayOfWeek(Qt.Monday)
        self.calendar.setLocale(QLocale(QLocale.Spanish, QLocale.Spain))
        today = QDate.currentDate()
        self.calendar.setMinimumDate(today)
        self.calendar.setFixedSize(600, 480)  # Tamaño completo del calendario
        self.calendar.setCursor(Qt.PointingHandCursor)
        self.calendar.setStyleSheet("""
            QWidget {
            background-color: white;
            color: #333;
            font-family: 'Inter';
            outline: none;
            }

            QCalendarWidget QWidget#qt_calendar_navigationbar {
            background-color: #f5f5f5;
            color: black;
            outline: none;
            }

            QCalendarWidget QToolButton {
            color: black;
            background-color: transparent;
            font-size: 14px;
            font-weight: bold;
            border: none;
            outline: none;
            }

            QCalendarWidget QToolButton:hover {
            background-color: #e9e9e9;
            outline: none;
            }

            QCalendarWidget QToolButton#qt_calendar_prevmonth {
            qproperty-icon: url('src/resources/images/add_task/prev_arrow.svg');
            }

            QCalendarWidget QToolButton#qt_calendar_nextmonth {
            qproperty-icon: url('src/resources/images/add_task/next_arrow.svg');
            }

            QCalendarWidget QAbstractItemView {
            selection-background-color: #e0e0e0;
            selection-color: black;
            border-radius: 3px;
            outline: none;
            }

            QCalendarWidget QAbstractItemView::item:disabled {
            background-color: #f0f0f0;  /* Color gris claro para los días anteriores */
            color: #d3d3d3;  /* Gris claro para el texto de los días anteriores */
            }
                
            QCalendarWidget QAbstractItemView::item:hover {
            background-color: #e0e0e0;
            color: black;
            border-radius: 3px;
            outline: none;
            }

            QCalendarWidget QAbstractItemView:enabled {
            color: #333;
            background-color: white;
            gridline-color: #ccc;
            outline: none;
            }

            QCalendarWidget QAbstractItemView:disabled {
            color: #aaa;
            outline: none;
            }

            QCalendarWidget QSpinBox {
            background-color: white;
            color: black;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px;
            outline: none;
            }

            QCalendarWidget QSpinBox::up-button, 
            QCalendarWidget QSpinBox::down-button {
            background-color: transparent;
            border: none;
            color: white;
            outline: none;
            }

            QCalendarWidget QSpinBox::up-button:hover, 
            QCalendarWidget QSpinBox::down-button:hover {
            background-color: transparent;
            outline: none;
            }
                        
            QCalendarWidget QSpinBox::down-button {
            width: 0px;
            height: 0px;
            border: none;
            background: transparent;
            qproperty-icon: none;
            }
                                    
            QCalendarWidget QSpinBox::drop-down {
            width: 0px;
            height: 0px;
            border: none;
            background: transparent;
            qproperty-icon: none;
        }

            QCalendarWidget QSpinBox::up-button {
            width: 0px;
            height: 0px;
            border: none;
            background: transparent;
            qproperty-icon: none;
            }
        """)
        self.calendar.selectionChanged.connect(self.day_selected)

        self.combo_box2 = QComboBox(self.container)
        self.combo_box2.addItem(QIcon("src/resources/images/add_task/red_flag.svg"), "Prioridad 1")
        self.combo_box2.addItem(QIcon("src/resources/images/add_task/orange_flag.svg"), "Prioridad 2")
        self.combo_box2.addItem(QIcon("src/resources/images/add_task/blue_flag.svg"), "Prioridad 3")
        self.combo_box2.addItem(QIcon("src/resources/images/add_task/white_flag.svg"), "Prioridad 4")
        self.combo_box2.setCurrentIndex(3)  # Establecer la prioridad 4 como predeterminada
        self.combo_box2.setFixedHeight(54)
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
        self.category_text.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.category_text.textChanged.connect(self.ensure_hashtag)
        combo_layout.addWidget(self.category_text)

        container_layout.addLayout(combo_layout)  # Agrega los elementos en una fila
        
        # Botón de cerrar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignRight)
        
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
        
        self.add_task_button = QPushButton("Añadir tarea", self.container)
        self.add_task_button.setStyleSheet("""
            QPushButton {
            background-color: #eda59e;
            color: #fff;
            padding: 10px;
            border-radius: 5px;
            }
        """)
        self.add_task_button.setFont(inter_font)
        self.add_task_button.setCursor(Qt.ForbiddenCursor)
        button_layout.addWidget(self.add_task_button, alignment=Qt.AlignRight)
        
        container_layout.addLayout(button_layout)
        
        # Agrega el contenedor al layout principal centrado
        main_layout.addWidget(self.container, alignment=Qt.AlignCenter)

    def add_task_button_available(self):
        if self.title_input.text():  # Si hay texto en el input
            self.add_task_button.setStyleSheet("""
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
            self.add_task_button.setCursor(Qt.PointingHandCursor)
            # self.task_manager = TaskManager()
            # self.add_task_button.clicked.connect(self.project.add_task)
        else:  # Si no hay texto en el input
            self.add_task_button.setStyleSheet("""
                QPushButton {
                    background-color: #eda59e;
                    color: #fff;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
            self.add_task_button.setCursor(Qt.ForbiddenCursor)

    def show_calendar(self):
        if self.calendar_frame.isVisible():
            self.calendar_frame.hide()
        else:
            # Convertir el QFrame en una ventana popup
            self.calendar_frame.setParent(None)
            self.calendar_frame.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
            # Posicionar el popup en la posición global, justo debajo del botón
            button_pos = self.calendar_button.mapToGlobal(QPoint(0, self.calendar_button.height()))
            self.calendar_frame.move(button_pos)
            self.calendar_frame.show()

    def day_selected(self):
        # Obtener la fecha seleccionada
        selected_date = self.calendar.selectedDate().toString("dd/MM/yyyy")
        day, month, year = selected_date.split('/')
        months = {
            '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr',
            '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago',
            '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'
        }
        new_selected_date = f" {day} {months[month]}"
        
        # Actualizar el texto del botón con la fecha seleccionada
        self.calendar_button.setFixedWidth(100)
        if year != str(QDate.currentDate().year()):
            new_selected_date += f" {year}"

        if len(new_selected_date) > 7:
            self.calendar_button.setFixedWidth(170)
        else:
            self.calendar_button.setFixedWidth(115)

        if selected_date == QDate.currentDate().toString("dd/MM/yyyy"):
            new_selected_date = " Hoy"
            self.calendar_button.setStyleSheet("""
                QPushButton {
                border: 1px solid #ccc; 
                border-radius: 5px; 
                padding: 10px; 
                font-size: 18px;
                color: #058527;
                }
                QPushButton:hover {
                background-color: #e0e0e0;
                }
            """)
            icon = QIcon("src/resources/images/add_task/green_date.svg")  # Cambia esto por la ruta real de tu imagen
            self.calendar_button.setIcon(icon)
            self.calendar_button.setIconSize(QSize(24, 24))
        elif selected_date == QDate.currentDate().addDays(1).toString("dd/MM/yyyy"):
            new_selected_date = " Mañana"
            self.calendar_button.setFixedWidth(145)
            self.calendar_button.setStyleSheet("""
                QPushButton {
                border: 1px solid #ccc; 
                border-radius: 5px; 
                padding: 10px; 
                font-size: 18px;
                color: #eb8909;
                }
                QPushButton:hover {
                background-color: #e0e0e0;
                }
            """)
            icon = QIcon("src/resources/images/add_task/orange_date.svg")  # Cambia esto por la ruta real de tu imagen
            self.calendar_button.setIcon(icon)
            self.calendar_button.setIconSize(QSize(24, 24))
        elif selected_date == QDate.currentDate().addDays(2).toString("dd/MM/yyyy"):
            new_selected_date = " Pasado mañana"
            self.calendar_button.setFixedWidth(190)
            self.calendar_button.setStyleSheet("""
                QPushButton {
                border: 1px solid #ccc; 
                border-radius: 5px; 
                padding: 10px; 
                font-size: 18px;
                color: #692ec2;
                }
                QPushButton:hover {
                background-color: #e0e0e0;
                }
            """)
            icon = QIcon("src/resources/images/add_task/purple_date.svg")  # Cambia esto por la ruta real de tu imagen
            self.calendar_button.setIcon(icon)
            self.calendar_button.setIconSize(QSize(24, 24))
        else:
            self.calendar_button.setStyleSheet("""
                QPushButton {
                border: 1px solid #ccc; 
                border-radius: 5px; 
                padding: 10px; 
                font-size: 18px;
                color: #808080;
                }
                QPushButton:hover {
                background-color: #e0e0e0;
                }
            """)
            icon = QIcon("src/resources/images/add_task/black_date.svg")  # Cambia esto por la ruta real de tu imagen
            self.calendar_button.setIcon(icon)
            self.calendar_button.setIconSize(QSize(24, 24))
            
        self.calendar_button.setText(new_selected_date)
        
        # Ocultar el calendario
        self.calendar_frame.hide()

    def ensure_hashtag(self):
        text = self.category_text.text()
        if text and not text.startswith("#"):
            self.category_text.setText("#" + text.lstrip("#"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = AddTaskDialog()
    popup.exec_()
    sys.exit(0)