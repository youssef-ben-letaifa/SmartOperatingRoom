
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QScrollArea, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt

class PatientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("Patient Profile")
        header.setObjectName("header")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        add_btn = QPushButton("+ Add New")
        add_btn.setStyleSheet("background-color: #2196F3;")
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)

        # Profile Card for "Touhami"
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border: 1px solid #333;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        cl = QVBoxLayout(card) # Main Card Layout
        
        # Identity Row
        id_row = QHBoxLayout()
        name_lbl = QLabel("El Touhami")
        name_lbl.setStyleSheet("font-size: 32px; font-weight: bold; color: #2196F3;")
        
        status_lbl = QLabel("STATUS: PRE-OP")
        status_lbl.setStyleSheet("background-color: #FF9800; color: black; font-weight: bold; padding: 5px 10px; border-radius: 4px;")
        
        id_row.addWidget(name_lbl)
        id_row.addStretch()
        id_row.addWidget(status_lbl)
        cl.addLayout(id_row)
        
        cl.addSpacing(20)
        
        # Details Grid
        grid = QGridLayout()
        grid.setSpacing(20)
        
        def add_field(label, value, r, c):
            l_lbl = QLabel(label)
            l_lbl.setStyleSheet("color: #888; font-size: 14px;")
            v_lbl = QLabel(value)
            v_lbl.setStyleSheet("color: #EEE; font-size: 18px; font-weight: 500;")
            v_layout = QVBoxLayout()
            v_layout.addWidget(l_lbl)
            v_layout.addWidget(v_lbl)
            grid.addLayout(v_layout, r, c)

        add_field("Patient ID", "859-22-11", 0, 0)
        add_field("Age / Gender", "54 / Male", 0, 1)
        add_field("Blood Type", "O+", 0, 2)
        add_field("Admission Date", "2024-12-17", 0, 3)
        
        cl.addLayout(grid)
        cl.addSpacing(20)
        
        # Medical Folder
        folder_lbl = QLabel("Medical Folder / History")
        folder_lbl.setStyleSheet("color: #2196F3; font-weight: bold; font-size: 16px; margin-bottom: 5px;")
        cl.addWidget(folder_lbl)
        
        history_text = QLabel(
            "• Chronic Hypertension (Managed - Lisinopril)\n"
            "• Type 2 Diabetes (HbA1c: 6.8%)\n"
            "• Allergies: Peanuts (Anaphylaxis), Penicillin\n"
            "• Previous Surgeries: Appendectomy (2018), Tonsillectomy (Childhood)\n"
            "• Current Meds: Metformin 500mg, Lisinopril 10mg."
        )
        history_text.setStyleSheet("color: #CCC; font-size: 15px; line-height: 140%; background-color: #263238; padding: 15px; border-radius: 5px;")
        history_text.setWordWrap(True)
        cl.addWidget(history_text)
        
        cl.addStretch()
        
        layout.addWidget(card)
        layout.addStretch()
