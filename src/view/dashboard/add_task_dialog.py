import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, 
    QGraphicsDropShadowEffect, QWidget, QLineEdit, QFrame
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QFontDatabase, QFont
from PyQt5.QtWidgets import QComboBox, QHBoxLayout
from PyQt5.QtWidgets import QCalendarWidget
import random

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
        container_layout.addWidget(self.title_input)
        
        # Layout para el botón de calendario y el combobox
        combo_layout = QHBoxLayout()
        combo_layout.setAlignment(Qt.AlignLeft)
        
        self.calendar_button = QPushButton("Fecha", self.container)
        self.calendar_button.setFixedWidth(100)  # Ajustar el ancho del botón
        self.calendar_button.clicked.connect(self.show_calendar)
        self.calendar_button.setStyleSheet("""
            QPushButton {
            border: 1px solid #ccc; 
            border-radius: 5px; 
            padding: 10px; 
            font-size: 18px;
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
        self.calendar_frame.setFixedSize(220, 180)  # Ajustar tamaño del calendario
        self.calendar_frame.hide()  # Ocultarlo inicialmente
        
        # Crear el calendario dentro del frame
        self.calendar = QCalendarWidget(self.calendar_frame)
        self.calendar.setFixedSize(720, 780)  # Reducir tamaño del calendario
        self.calendar.setStyleSheet("""
            border: 1px solid #555;
            border-radius: 10px;
            background-color: #2B3E50;
            color: white;
        """)

        self.combo_box2 = QComboBox(self.container)
        self.combo_box2.addItems(["Prioridad 1", "Prioridad 2", "Prioridad 3", "Prioridad 4"])
        self.combo_box2.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 18px;
            }
            /* Estilo cuando el ratón pasa por encima */
            QComboBox:hover {
                background-color: #f0f0f0;
            }
        """)
        self.combo_box2.setFont(inter_font)
        self.combo_box2.setCursor(Qt.PointingHandCursor)
        combo_layout.addWidget(self.combo_box2)

        container_layout.addLayout(combo_layout)  # Agrega los elementos en una fila
        
        # Botón de cerrar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        
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
                    background-color: #a32a2b;
                }
            """)
            self.add_task_button.setCursor(Qt.PointingHandCursor)
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
            # Posicionar el calendario justo debajo del botón
            button_pos = self.calendar_button.mapToGlobal(QPoint(0, self.calendar_button.height()))
            self.calendar_frame.move(button_pos)
            self.calendar_frame.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = AddTaskDialog()
    popup.exec_()
    sys.exit(app.exec_())
