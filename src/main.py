import sys
import ctypes
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from view.shared.titlebar import TitleBar
from view.shared.sidebar import SideBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Eliminar marco de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(1600, 900)

        self.showMaximized()

        # Configurar la ventana principal
        self.setWindowTitle("Gestió de tasques")
        self.setStyleSheet("background-color: transparent;")
        self.setWindowIcon(QIcon("src/resources/images/taskManagement.ico"))

        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_bar = TitleBar()
        self.layout.addWidget(self.title_bar)  # Agregar la barra de título arriba

        self.side_bar = SideBar()
        self.layout.addWidget(self.side_bar)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.handle_window_state()
        super().changeEvent(event)

    def handle_window_state(self):
        if hasattr(self, "title_bar"):
            if self.isMaximized():
                self.title_bar.maximize_button.hide()
                self.title_bar.restore_button.show()
            else:
                self.title_bar.restore_button.hide()
                self.title_bar.maximize_button.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()  # ¡Aquí se crea la ventana!
    sys.exit(app.exec_())