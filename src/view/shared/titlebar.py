import ctypes
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QApplication
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent, QPoint

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# from src.controller.titlebar_controller import mousePressEvent, mouseMoveEvent, eventFilter, minimize

class TitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.start_pos = None
        self.is_dragging = False
        self.setMouseTracking(True)

        self.setFixedHeight(50)
        # self.setStyleSheet("background-color: #4CAF50; border-bottom-right-radius: 10px;")

        # Layout de la barra de título
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)  # Establecer márgenes a 0 para que la barra ocupe toda la pantalla
        hbox.setSpacing(0)

        # Imagen (lena.png)
        self.image_label = QLabel()
        pixmap = QPixmap("src/resources/images/taskManagement.ico").scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Cargar y escalar la imagen
        self.image_label.setPixmap(pixmap)

        # Etiqueta de título
        self.title_label = QLabel("Gestió de tasques")
        self.title_label.setStyleSheet(f"color: black; font-size: 18px;")

        hbox.addWidget(self.image_label)
        hbox.addWidget(self.title_label)

        self.spacer = QWidget()
        self.spacer.setStyleSheet(f"background-color: #fcfaf8;")  # Color de la barra
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Hace que el espaciador expanda
        hbox.addWidget(self.spacer)

        # Botones de la barra de título
        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(65, 50)
        self.minimize_button.setStyleSheet(f"color: black; border: none; font-size: 20px; padding-bottom: 5px;")
        self.minimize_button.clicked.connect(self.minimize)
        self.minimize_button.installEventFilter(self)  # Instalar filtro de eventos

        self.maximize_button = QPushButton("🗖")
        self.maximize_button.setFixedSize(65, 50)
        self.maximize_button.setStyleSheet(f"color: black; border: none; font-size: 20px; padding-bottom: 8px;")
        self.maximize_button.clicked.connect(self.change_button)
        self.maximize_button.installEventFilter(self)  # Instalar filtro de eventos

        self.restore_button = QPushButton("🗗")
        self.restore_button.setFixedSize(65, 50)
        self.restore_button.setStyleSheet(f"color: black; border: none; font-size: 20px; padding-bottom: 8px;")
        self.restore_button.clicked.connect(self.change_button)
        self.restore_button.installEventFilter(self)  # Instalar filtro de eventos

        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(65, 50)
        self.close_button.setStyleSheet(f"color: black; border: none; font-size: 20px; padding-bottom: 5px;")
        self.close_button.clicked.connect(self.close)
        self.close_button.installEventFilter(self)  # Instalar filtro de eventos

        # Añadir botones a la barra de título
        hbox.addWidget(self.minimize_button)
        hbox.addWidget(self.maximize_button)
        hbox.addWidget(self.restore_button)
        hbox.addWidget(self.close_button)
        
        self.maximize_button.hide()

        self.setStyleSheet(f"""
            QWidget {{
                background-color: #fcfaf8;
            }}
            QLabel {{
                padding-left: 10px;
            }}
        """)

        self.start = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Convertir hwnd a entero
            hwnd = int(self.window().winId())
            
            # Activar movimiento nativo
            ctypes.windll.user32.ReleaseCapture()
            ctypes.windll.user32.SendMessageW(hwnd, 0xA1, 0x2, 0)
            
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        # Maximizar/restaurar con doble clic como en Windows
        self.change_button()
        super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def change_button(self):
        if self.window().isMaximized():
            self.window().showNormal()
            self.restore_button.hide()
            self.maximize_button.show()
        else:
            self.window().showMaximized()
            self.maximize_button.hide()
            self.restore_button.show()

    def eventFilter(self, source, event):
        if source in (self.minimize_button, self.maximize_button, self.restore_button, self.close_button):
            padding = "8px" if source in (self.maximize_button, self.restore_button) else "5px"

            if event.type() == QEvent.Enter:
                source.setStyleSheet(f"background-color: #edebe9; color: black; border: none; font-size: 20px; padding-bottom: {padding};")
            elif event.type() == QEvent.Leave:
                source.setStyleSheet(f"background-color: #fcfaf8; color: black; border: none; font-size: 20px; padding-bottom: {padding};")
            elif event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    source.setStyleSheet(f"background-color: #dedcda; color: black; border: none; font-size: 20px; padding-bottom: {padding};")
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    source.setStyleSheet(f"background-color: #fcfaf8; color: black; border: none; font-size: 20px; padding-bottom: {padding};")
                    if source == self.minimize_button:
                        self.minimize()
                    elif source == self.close_button:
                        self.window().close()

        return super().eventFilter(source, event)

    def minimize(self):
        self.window().showMinimized()

    def nativeEvent(self, eventType, message):
        from PyQt5.sip import unwrapinstance
        msg = unwrapinstance(message)

        if msg.message == 0x007B:  # WM_CONTEXTMENU
            hwnd = int(self.window().winId())  # <--- Convertir a entero
            pos = msg.lParam
            x = pos & 0xFFFF
            y = (pos >> 16) & 0xFFFF
            ctypes.windll.user32.SendMessageW(hwnd, 0x0313, 0, (y << 16) | x)
            return True, 0

        return False, 0