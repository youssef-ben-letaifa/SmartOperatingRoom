
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont

class SplashScreen(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.init_ui()
        
        # 5 Second Timer
        QTimer.singleShot(5000, self.finish_splash)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Container - Pure Black
        container = QLabel(self)
        container.resize(600, 400)
        container.setStyleSheet("background-color: #000000; border-radius: 10px;")
        
        inner_layout = QVBoxLayout(container)
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.setSpacing(20)
        
        # Windows 11 Style Welcome
        welcome = QLabel("Welcome")
        welcome.setStyleSheet("color: #FFFFFF; font-family: 'Segoe UI'; font-size: 54px; font-weight: 300;")
        
        # Subtitle
        sub = QLabel("Smart Operating Room System")
        sub.setStyleSheet("color: #E0E0E0; font-family: 'Segoe UI'; font-size: 18px; margin-top: 10px;")
        
        # Simple spinner or dots could go here, but text is fine
        loading = QLabel("Loading...")
        loading.setStyleSheet("color: #888888; font-size: 12px; margin-top: 40px;")
        
        inner_layout.addWidget(welcome, 0, Qt.AlignmentFlag.AlignHCenter)
        inner_layout.addWidget(sub, 0, Qt.AlignmentFlag.AlignHCenter)
        inner_layout.addWidget(loading, 0, Qt.AlignmentFlag.AlignHCenter)

    def finish_splash(self):
        self.finished.emit()
        self.close()
