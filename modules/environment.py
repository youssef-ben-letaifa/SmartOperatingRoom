
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSlider, QFrame, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
import cv2
import mediapipe as mp
import time

class CameraWidget(QLabel):
    # Signal: emits total finger count
    gesture_detected = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setFixedSize(280, 210)
        self.setStyleSheet("background-color: #000; border: 2px solid #333; margin-top: 10px;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Initializing AI...")
        
        # Camera Setup
        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        
        # Mediapipe Setup
        self.mp_hands = mp.solutions.hands
        # Min detection confidence 0.7 for stability
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        
        # Debouncing Logic
        self.last_count = -1
        self.stable_frames = 0
        self.REQUIRED_STABLE_FRAMES = 10 # ~300ms at 30fps
        
        self.start_camera()

    def start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.timer.start(30)
            else:
                self.setText("NO CAMERA")
        except Exception as e:
            self.setText("CAM ERR")

    def count_fingers(self, hand_landmarks, handedness):
        # Tips identifiers
        finger_tips = [8, 12, 16, 20]
        # Thumb is 4
        count = 0
        
        lm = hand_landmarks.landmark
        
        # 1. Thumb: Check x relative to IP joint (3)
        # Depends on Left/Right hand. 
        # Left Hand: Thumb Tip x > IP x means open? No, depends on palm facing.
        # Simple heuristic: If tip is "outside" relative to palm center.
        # Generic heuristic often used: compare Tip x to IP x. 
        # For 'Right' hand: Tip x < IP x is open. For 'Left': Tip x > IP x.
        # Handedness label needed.
        label = handedness.classification[0].label
        
        if label == "Right":
            if lm[4].x < lm[3].x: count += 1
        else:
            if lm[4].x > lm[3].x: count += 1
            
        # 2. Fingers
        # Tip y < PIP y (Up is lower y)
        for tip in finger_tips:
            if lm[tip].y < lm[tip-2].y:
                count += 1
                
        return count

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # 1. Process
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(frame_rgb)
                
                total_fingers = 0
                
                # 2. Draw & Count
                if results.multi_hand_landmarks:
                    for idx, hand_lms in enumerate(results.multi_hand_landmarks):
                        # Draw landmarks
                        self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                        
                        # Count fingers for this hand
                        # Need handedness info
                        if results.multi_handedness:
                            h_label = results.multi_handedness[idx]
                            total_fingers += self.count_fingers(hand_lms, h_label)
                
                # 3. Debouncing
                if total_fingers == self.last_count:
                    self.stable_frames += 1
                else:
                    self.stable_frames = 0
                    self.last_count = total_fingers
                
                # Trigger action if stable (and > 0)
                detected_state = 0
                if self.stable_frames > self.REQUIRED_STABLE_FRAMES:
                    detected_state = total_fingers
                    # Emit only once per stable state change? 
                    # User wants continuous control or one-shot? 
                    # Navigation is one-shot. Lights might be set. 
                    # We emit every frame it's stable, Main Window handles logic (e.g. toggle only on change)
                    self.gesture_detected.emit(detected_state)
                
                # 4. Overlay Text
                cv2.putText(frame, f"Fingers: {total_fingers}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                if detected_state > 0:
                     cv2.putText(frame, f"ACTION: {detected_state}", (10, 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                # 5. Display
                # Convert back to RGB for Qt display (frame was BGR for drawing)
                # Drawing was done on 'frame' (BGR).
                frame_disp = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_disp = cv2.resize(frame_disp, (280, 210))
                h, w, ch = frame_disp.shape
                bytes_per_line = ch * w
                q_img = QImage(frame_disp.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        if self.cap:
            self.cap.release()
        super().closeEvent(event)

class EnvironmentWidget(QWidget):
    # Bubble up signal
    gesture_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(320)
        self.setStyleSheet("background-color: #1A1A1A; border-right: 1px solid #333;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(25)
        
        header = QLabel("ENVIRONMENT")
        header.setStyleSheet("color: #2196F3; font-weight: bold; font-size: 18px; letter-spacing: 2px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Controls
        # Store slider refs to control them via AI
        self.temp_slider = self.create_slider("Temperature", "°C", 16, 26, 20, "#FF7043")
        self.hum_slider = self.create_slider("Humidity", "%", 30, 60, 45, "#42A5F5")
        self.light_slider = self.create_slider("Lighting", "%", 0, 100, 80, "#FFCA28")
        self.press_slider = self.create_slider("Pressure", "Pa", 10, 25, 15, "#66BB6A")

        layout.addLayout(self.temp_slider['layout'])
        layout.addLayout(self.hum_slider['layout'])
        layout.addLayout(self.light_slider['layout'])
        layout.addLayout(self.press_slider['layout'])

        layout.addStretch()
        
        # Camera
        cam_label = QLabel("AI GESTURE CAM")
        cam_label.setStyleSheet("color: #AAA; font-weight: bold; font-size: 12px;")
        layout.addWidget(cam_label)
        
        self.camera = CameraWidget()
        self.camera.gesture_detected.connect(self.on_gesture)
        layout.addWidget(self.camera, 0, Qt.AlignmentFlag.AlignHCenter)

    def on_gesture(self, count):
        self.gesture_signal.emit(count)
        # Verify: could flash UI or something here

    def create_slider(self, title, unit, min_val, max_val, default, color):
        l = QVBoxLayout()
        l.setSpacing(5)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #EEE; font-size: 14px;")
        
        val_label = QLabel(f"{default}{unit}")
        val_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px;")
        val_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        top_row = QHBoxLayout()
        top_row.addWidget(lbl_title)
        top_row.addStretch()
        top_row.addWidget(val_label)
        l.addLayout(top_row)
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 4px;
                background: #333;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {color};
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }}
        """)
        slider.valueChanged.connect(lambda v: val_label.setText(f"{v}{unit}"))
        l.addWidget(slider)
        
        # Return dict to access slider later
        return {'layout': l, 'slider': slider, 'label': val_label, 'unit': unit}
