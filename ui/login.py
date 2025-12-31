from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal


class LoginScreen(QWidget):
    login_successful = pyqtSignal(str) # Emits role name

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OR System - Authentication")
        self.resize(1024, 768)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(40)

        # Logo / Title area
        title = QLabel("Smart OR Access Control")
        title.setObjectName("header")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Role Grid
        grid_frame = QFrame()
        grid = QGridLayout(grid_frame)
        grid.setSpacing(30)
        
        roles = [
            ("Lead Surgeon", "#1565C0"),
            ("Anesthetist", "#00695C"),
            ("Head Nurse", "#AD1457"),
            ("Technician", "#F9A825")
        ]
        
        row, col = 0, 0
        for role, color in roles:
            btn = QPushButton(role)
            btn.setFixedSize(250, 150)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: none;
                    border-radius: 15px;
                    font-size: 24px;
                    color: white;
                }}
                QPushButton:hover {{
                    border: 4px solid white;
                }}
            """)
            btn.clicked.connect(lambda checked, r=role: self.attempt_login(r))
            grid.addWidget(btn, row, col)
            
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        main_layout.addWidget(grid_frame)

        # Emergency Button
        emergency_btn = QPushButton("EMERGENCY VIEW ONLY")
        emergency_btn.setFixedSize(400, 60)
        emergency_btn.setStyleSheet("""
            background-color: transparent;
            border: 2px solid #D32F2F;
            color: #D32F2F;
            font-size: 18px;
        """)
        emergency_btn.clicked.connect(lambda: self.attempt_login("Emergency View"))
        main_layout.addWidget(emergency_btn, 0, Qt.AlignmentFlag.AlignHCenter)

    def attempt_login(self, role):
        # Mock authentication simple pass-through for now
        self.login_successful.emit(role)
        self.close()
