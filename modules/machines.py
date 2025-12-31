
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGridLayout, QSlider, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class MachineCard(QFrame):
    def __init__(self, name, image_filename):
        super().__init__()
        self.setObjectName("card")
        self.name = name
        self.image_filename = image_filename
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(self.name)
        title.setObjectName("subheader")
        layout.addWidget(title)

        # Image
        img_label = QLabel()
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_label.setFixedSize(250, 200)
        img_label.setStyleSheet("background-color: #333; border-radius: 8px;") 
        
        # Load Image
        image_path = os.path.join(os.getcwd(), "images", self.image_filename)
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                img_label.setPixmap(pixmap.scaled(240, 190, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                 img_label.setText(f"IMG ERR: {self.image_filename}")
        else:
            img_label.setText("NO IMAGE")
            
        layout.addWidget(img_label)

        # Controls
        controls_layout = QHBoxLayout()
        
        # Power Toggle
        self.power_btn = QPushButton("OFF")
        self.power_btn.setCheckable(True)
        self.power_btn.setObjectName("machine_toggle")
        self.power_btn.setFixedSize(80, 40)
        self.power_btn.clicked.connect(self.handle_toggle) 
        
        controls_layout.addWidget(QLabel("Power:"))
        controls_layout.addWidget(self.power_btn)
        
        layout.addLayout(controls_layout)

        # Dummy Slider
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Level:"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setEnabled(False)
        slider_layout.addWidget(self.slider)
        
        layout.addLayout(slider_layout)

    def handle_toggle(self):
        # V5: Remove confirmation, direct toggle
        is_turning_on = self.power_btn.isChecked()
        
        if is_turning_on:
            self.power_btn.setText("ON")
            self.slider.setEnabled(True)
        else:
            self.power_btn.setText("OFF")
            self.slider.setEnabled(False)


class MachinesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        header = QLabel("Device Control Center")
        header.setObjectName("header")
        main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;") 
        
        content_widget = QWidget()
        self.grid = QGridLayout(content_widget)
        self.grid.setSpacing(20)

        # V5: Devices reduced to only Monitor and Ventilator
        machines = [
            ("Patient Monitor", "Patient Monitoring Device.png"),
            ("Ventilator", "Ventilator.png")
        ]

        row = 0
        col = 0
        for name, img_file in machines:
            card = MachineCard(name, img_file)
            self.grid.addWidget(card, row, col)
            col += 1 # Just grid logic, though with 2 items it's simple
            if col > 1:
                col = 0
                row += 1

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        main_layout.addStretch()
