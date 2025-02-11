from PyQt5.QtCore import QObject, pyqtSignal

class SignalBus(QObject):
    _instance = None  # Variable de clase para almacenar la única instancia

    taskAdded = pyqtSignal()
    filtersChanged = pyqtSignal(bool, int, str)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SignalBus, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        if not hasattr(self, "_initialized"):  # Evita múltiples inicializaciones
            print("✅ Instancia de SignalBus creada")
            self._initialized = True

# 🔥 Se crea UNA SOLA instancia aquí
global_signals = SignalBus()
