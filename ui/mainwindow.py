
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QLabel, QPushButton, QButtonGroup, QStackedWidget
)
from PyQt6.QtCore import Qt

from modules.patient import PatientWidget
from modules.doctor import DoctorWidget
from modules.monitor import MonitorWidget
from modules.machines import MachinesWidget
from modules.environment import EnvironmentWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart OR System V6")
        self.showFullScreen() 
        self.init_ui()
        
        # Gesture State for Toggles
        self.last_gesture = 0

    def init_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)
        
        main_h_layout = QHBoxLayout(central_widget)
        main_h_layout.setContentsMargins(0, 0, 0, 0)
        main_h_layout.setSpacing(0)

        # 1. Sidebar (Environment + AI Camera)
        self.sidebar = EnvironmentWidget()
        self.sidebar.gesture_signal.connect(self.handle_gesture)
        main_h_layout.addWidget(self.sidebar)

        # 2. Right Content
        right_area = QWidget()
        right_layout = QVBoxLayout(right_area)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # A. Top Bar
        self.top_bar = QWidget()
        self.top_bar.setObjectName("top_bar")
        self.top_bar.setFixedHeight(70)
        
        tb_layout = QHBoxLayout(self.top_bar)
        # MacOS Spec: 12px from left. Top margin simulated by layout padding or widget alignment.
        # We'll use 12px left margin.
        tb_layout.setContentsMargins(12, 0, 30, 0)
        tb_layout.setSpacing(20)

        # MacOS Big Sur Window Controls (Moved to Left)
        win_controls = QHBoxLayout()
        win_controls.setSpacing(8) # Spec: 8px apart
        
        # Close (Red)
        btn_close = QPushButton("×") # Use text "×"
        btn_close.setObjectName("win_btn")
        # Apply specific ID for color. Note: stylesheet uses objectName #win_close
        btn_close.setObjectName("win_close") 
        # Need to set both generic class for size and specific for color?
        # PyQt stylesheets handle multiple IDs tricky. 
        # Better: set objectName to "win_close" and generic props in #win_close too or use property.
        # Let's use property or direct style in QSS for ID. 
        # I updated QSS to use #win_close/min/max for colors, AND #win_btn logic?
        # Wait, QSS doesn't support multiple IDs on one widget.
        # I will set objectName "win_close" and ensure QSS selector matches logic.
        # QSS: QPushButton#win_close { ... } AND QPushButton[class="win_btn"]? No classes.
        # I'll set a property.
        btn_close.setProperty("class", "win") # Need to re-polish?
        # Simpler: Just put style directly or rely on correct QSS selectors.
        # My QSS has `QPushButton#win_close`. But also `QPushButton#win_btn`.
        # I will set objectName to specific, and duplicate the generic styles in QSS or use a merge?
        # Actually, in QSS I should just use `QPushButton[accessibleName="win_btn"]` or similar if I could.
        # Let's try explicit styling here to be safe or update QSS to target specific IDs with shared properties.
        # I'll update QSS in the next revised QSS file if needed, but for now I'll just rely on:
        # objectName="win_close", and QSS having `#win_close` with size/border props copied or shared.
        # Re-reading my QSS update: I defined `#win_btn` but the buttons need specific IDs for colors.
        # Strategy: Set objectName to "win_btn" (for size/shape) and use setStyleSheet for specific color?
        # No, that overrides QSS.
        # Best: Update QSS to share styles.
        # I'll set objectName to "win_close", "win_min", "win_max". 
        # AND I will update QSS to apply the shared "Big Sur Shape" to all 3 IDs.
        
        btn_close.setObjectName("win_close")
        btn_close.clicked.connect(self.close)
        
        # Minimize (Yellow)
        btn_min = QPushButton("−") # Minus
        btn_min.setObjectName("win_min")
        btn_min.clicked.connect(self.showMinimized)
        
        # Maximize (Green)
        btn_max = QPushButton("+") # Plus (or arrows)
        btn_max.setObjectName("win_max")
        btn_max.clicked.connect(self.toggle_fullscreen)

        win_controls.addWidget(btn_close)
        win_controls.addWidget(btn_min)
        win_controls.addWidget(btn_max)
        
        tb_layout.addLayout(win_controls)
        
        tb_layout.addSpacing(20)

        # Title
        title = QLabel("OR COMMAND (AI ACTIVE)")
        title.setStyleSheet("font-size: 20px; font-weight: 900; color: #FFF; letter-spacing: 1px;")
        tb_layout.addWidget(title)
        
        tb_layout.addStretch()
        
        # Navigation
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        
        btn_names = ["PATIENT", "SURGEON", "MONITOR", "DEVICES"]
        self.nav_buttons = []
        
        for i, name in enumerate(btn_names):
            btn = QPushButton(name)
            btn.setObjectName("nav_btn")
            btn.setCheckable(True)
            self.nav_group.addButton(btn, i)
            tb_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        self.nav_group.idClicked.connect(self.display_page)
        
        tb_layout.addStretch() # Spacer to push settings right
        tb_layout.addWidget(QPushButton("⚙settings", styleSheet="color: #888; border: none;"))
        
        right_layout.addWidget(self.top_bar)

        # B. Stack
        self.stack = QStackedWidget()
        self.patient_page = PatientWidget()
        self.doctor_page = DoctorWidget()
        self.monitor_page = MonitorWidget()
        self.machines_page = MachinesWidget()
        
        self.stack.addWidget(self.patient_page)
        self.stack.addWidget(self.doctor_page)
        self.stack.addWidget(self.monitor_page)
        self.stack.addWidget(self.machines_page)
        
        right_layout.addWidget(self.stack)
        main_h_layout.addWidget(right_area)

        # Default
        self.nav_buttons[2].setChecked(True)
        self.stack.setCurrentIndex(2)

    def display_page(self, index):
        self.stack.setCurrentIndex(index)
        self.nav_buttons[index].setChecked(True)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def handle_gesture(self, finger_count):
        if finger_count == 0:
            self.last_gesture = 0
            return

        # NAVIGATION
        if finger_count == 1:
            if self.stack.currentIndex() != 0: self.display_page(0)
        elif finger_count == 2:
            if self.stack.currentIndex() != 1: self.display_page(1)
        elif finger_count == 3:
            if self.stack.currentIndex() != 2: self.display_page(2)
        elif finger_count == 4:
            if self.stack.currentIndex() != 3: self.display_page(3)
        
        # ENVIRONMENT
        elif finger_count == 5:
            self.sidebar.light_slider['slider'].setValue(40)
        elif finger_count == 6:
            self.sidebar.light_slider['slider'].setValue(100)
            
        # DEVICES
        if finger_count != self.last_gesture:
            self.last_gesture = finger_count
            target_machine = None
            should_turn_on = False
            
            if finger_count == 7:
                target_machine = "Patient Monitor"
                should_turn_on = True
            elif finger_count == 8:
                target_machine = "Patient Monitor"
                should_turn_on = False
            elif finger_count == 9:
                target_machine = "Ventilator"
                should_turn_on = True
            elif finger_count == 10:
                target_machine = "Ventilator"
                should_turn_on = False
                
            if target_machine:
                 self.toggle_machine(target_machine, should_turn_on)

    def toggle_machine(self, name, turn_on):
        grid = self.machines_page.grid
        for i in range(grid.count()):
            widget = grid.itemAt(i).widget()
            if hasattr(widget, 'name') and widget.name == name:
                current_state = widget.power_btn.isChecked()
                if current_state != turn_on:
                   widget.power_btn.click()
