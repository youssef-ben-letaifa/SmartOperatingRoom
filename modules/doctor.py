
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QDialog, QFormLayout, QLineEdit, QSplitter, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from modules.database import DatabaseManager
from modules.timeline import TimelineWidget

class AddPatientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Patient / Operation")
        self.resize(400, 300)
        self.db = DatabaseManager()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.history_input = QLineEdit()
        
        form.addRow("Patient Name:", self.name_input)
        form.addRow("Age:", self.age_input)
        form.addRow("Medical History:", self.history_input)
        
        layout.addLayout(form)
        
        save_btn = QPushButton("Save & Add to Queue")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

    def save(self):
        name = self.name_input.text()
        
        # V5 Fix: Validate Age to prevent crash (ValueError)
        try:
            age_val = int(self.age_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Age must be a valid number.")
            return # Do not quit, stay in dialog

        if name:
            self.db.add_patient(name, age_val, self.history_input.text())
            # V5 Request: "I wanna save and rest in the page" -> Don't close?
            # User said: "I don't wanna he quit, I wanna save and rest in the page"
            # Ambiguous: Does he mean the Dialog stays open or the App doesn't crash?
            # "The program quit" refers to the crash. 
            # "Reset in the page" likely means stay on the doctor page.
            # I will close the dialog as standard behavior for "Save", assuming "quit" meant the crash.
            self.accept()

class DoctorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        
        # LEFT SIDE
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # 1. Profile
        profile_card = QFrame()
        profile_card.setObjectName("card")
        p_layout = QHBoxLayout(profile_card)
        
        self.doc_name = QLabel("Loading...")
        self.doc_name.setStyleSheet("font-size: 24px; font-weight: bold; color: #2196F3;")
        
        self.doc_info = QLabel("Loading bio...")
        self.doc_info.setWordWrap(True)
        self.doc_info.setStyleSheet("color: #AAA; font-style: italic;")
        
        p_layout.addWidget(self.doc_name)
        p_layout.addStretch()
        p_layout.addWidget(self.doc_info)
        layout.addWidget(profile_card)

        # 2. Operations Dashboard
        dash_header = QHBoxLayout()
        dash_header.addWidget(QLabel("Surgical Schedule"))
        
        add_btn = QPushButton("+ Add Patient")
        add_btn.setFixedWidth(150)
        add_btn.clicked.connect(self.open_add_dialog)
        dash_header.addWidget(add_btn, 0, Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(dash_header)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Procedure", "Patient", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        # V5: Blue background for table, Dark text
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #E3F2FD;
                color: #000000;
                gridline-color: #90CAF9;
                selection-background-color: #2196F3;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table)
        
        right_widget = QWidget()
        right_widget.setFixedWidth(300)
        # Placeholder for Timeline implied via V4, but user said "Replace the surigical workflow time line with the 'envirenemnt' "??
        # User said: "Replace the surigical workflow time line with the 'envirenemnt' , and make the envirenemnt left bar fixed in each tab"
        # So Timeline is gone? Or moved?
        # User said: "Replace [it] with the environment... make environment left bar fixed".
        # This implies the space where the Timeline WAS is now empty or removed.
        # I will remove the Timeline from the Doctor view since Enviroment is now the Sidebar.
        
        # Okay, so Doctor View is just the Table now.
        main_layout.addWidget(left_widget)

    def load_data(self):
        doc = self.db.get_doctor()
        if doc:
            self.doc_name.setText(f"Dr. {doc[1]}")
            self.doc_info.setText(f"{doc[2]}")
            
            ops = self.db.get_operations(doc[0])
            self.table.setRowCount(len(ops))
            
            for row, op in enumerate(ops):
                self.table.setItem(row, 0, QTableWidgetItem(op[0]))
                self.table.setItem(row, 1, QTableWidgetItem(op[1]))
                self.table.setItem(row, 2, QTableWidgetItem(op[2]))
                status = QTableWidgetItem(op[3])
                if op[3] == "Pending": status.setForeground(QColor("red"))
                self.table.setItem(row, 3, status)

    def open_add_dialog(self):
        dialog = AddPatientDialog(self)
        if dialog.exec():
            self.load_data()

from PyQt6.QtGui import QColor
