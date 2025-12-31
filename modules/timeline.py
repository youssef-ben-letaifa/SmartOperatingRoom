
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QCheckBox, QScrollArea, QPushButton, QProgressBar
)
from PyQt6.QtCore import Qt

class TimelineStep(QFrame):
    def __init__(self, step_name, order, callback):
        super().__init__()
        self.step_name = step_name
        self.order = order
        self.callback = callback
        self.is_active = False
        self.is_completed = False
        
        self.init_ui()

    def init_ui(self):
        self.setObjectName("step_card")
        self.setStyleSheet("""
            QFrame#step_card {
                background-color: #1E1E1E;
                border: 1px solid #444;
                border-radius: 5px;
            }
        """)
        
        layout = QHBoxLayout(self)
        
        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self.on_check)
        layout.addWidget(self.checkbox)
        
        # Label
        self.label = QLabel(self.step_name)
        self.label.setStyleSheet("color: #888; font-size: 16px;")
        layout.addWidget(self.label)
        
        layout.addStretch()

    def set_active(self, active):
        self.is_active = active
        if active:
            self.label.setStyleSheet("color: #2196F3; font-weight: bold; font-size: 18px;")
            self.setStyleSheet("""
                QFrame#step_card {
                    background-color: #263238;
                    border: 2px solid #2196F3;
                    border-radius: 5px;
                }
            """)
        else:
            if self.is_completed:
                 self.label.setStyleSheet("color: #4CAF50; font-style: italic; text-decoration: line-through;")
            else:
                 self.label.setStyleSheet("color: #888;")
                 self.setStyleSheet("QFrame#steps_card { border: 1px solid #444; }")

    def on_check(self, state):
        checked = (state == Qt.CheckState.Checked.value)
        self.is_completed = checked
        self.callback(self.order, checked)


class TimelineWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.steps = [
            "Patient Identification Check",
            "Anesthesia Induction",
            "Surgical Site Prep",
            "Incision",
            "Hemostasis",
            "Procedure Execution",
            "Closure",
            "Anesthesia Reversal",
            "Transfer to PACU"
        ]
        self.step_widgets = []
        self.current_step_idx = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("Surgical Workflow Timeline")
        header.setObjectName("subheader")
        layout.addWidget(header)
        
        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setRange(0, len(self.steps))
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)
        layout.addWidget(self.progress)

        # Steps List
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(10)
        
        for i, step in enumerate(self.steps):
            w = TimelineStep(step, i, self.handle_step_change)
            self.content_layout.addWidget(w)
            self.step_widgets.append(w)
            
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.update_ui()

    def handle_step_change(self, order, checked):
        # Enforce sequential logic if desired, or just visual
        if checked:
            self.current_step_idx = order + 1
        else:
            self.current_step_idx = order
            
        self.update_ui()

    def update_ui(self):
        completed_count = 0
        for i, w in enumerate(self.step_widgets):
            if i < self.current_step_idx:
                w.checkbox.blockSignals(True)
                w.checkbox.setChecked(True)
                w.is_completed = True
                w.checkbox.blockSignals(False)
                w.set_active(False)
                completed_count += 1
            elif i == self.current_step_idx:
                w.set_active(True)
                w.checkbox.setChecked(False)
            else:
                w.set_active(False)
                w.checkbox.setChecked(False)
        
        self.progress.setValue(completed_count)
