
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QGridLayout, QPushButton, QProgressBar, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QRect, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient, QBrush, QPolygon

# --- UTILS ---

class ModernCard(QFrame):
    def __init__(self, color_accent="#333", bg_color="#1E1E1E"):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 15px;
                border: 1px solid #333;
            }}
        """)

class RecessedLabel(QLabel):
    def __init__(self, text, suffix=""):
        super().__init__()
        self.val = text
        self.suff = suffix
        self.setStyleSheet("background-color: transparent;")
        self.setFixedSize(100, 50)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw Recessed Box
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#111")) # Very dark background
        painter.drawRoundedRect(0, 15, self.width(), 35, 5, 5)
        
        # Draw Value
        painter.setPen(QColor("#FFF"))
        font = QFont("Arial", 18, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(QRect(0, 15, self.width()-30, 35), Qt.AlignmentFlag.AlignCenter, self.val)
        
        # Draw Suffix
        painter.setPen(QColor("#888"))
        font_sm = QFont("Arial", 10)
        painter.setFont(font_sm)
        painter.drawText(QRect(self.width()-30, 25, 25, 25), Qt.AlignmentFlag.AlignLeft, self.suff)

# --- GRAPHS ---

class MultiLeadECG(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: transparent;")
        self.data = [ [0]*200 for _ in range(6) ] # 6 Leads, wider buffer for high-res
        self.phases = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25] # Float phases
        self.labels = ["I", "II", "III", "aVR", "aVL", "aVF"]
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_wave)
        self.timer.start(10) # 100 FPS for smooth QRS

    def update_wave(self):
        import math, random, time
        
        # Physics: 60 BPM = 1 beat/sec
        # dt per frame at 100fps = 0.01s
        dt = 0.01 
        
        for i in range(6):
            self.phases[i] += dt
            if self.phases[i] > 1.0: self.phases[i] -= 1.0
            
            t = self.phases[i] # 0.0 to 1.0 seconds (since 60bpm)
            
            # Get Pure Signal
            signal = self.get_precise_ecg(t, i)
            
            # Baseline Wander (Respiration ~0.25 Hz)
            baseline = 1.5 * math.sin(2 * math.pi * 0.25 * time.time())
            
            # Noise (Micro-tremors)
            noise = random.uniform(-0.5, 0.5)
            
            val = signal + baseline + noise
            
            self.data[i].pop(0)
            self.data[i].append(val)
            
        self.update()

    def get_precise_ecg(self, t, lead_idx):
        import math
        
        # --- MEDICAL PARAMETERS (Normal Sinus Rhythm) ---
        # 1. P Wave: Atrial Depol. (0.08s - 0.10s) -> Round, small
        # 2. PR Segment: AV Delay (Isoelectric)
        # 3. QRS: Ventricular Depol. (0.06s - 0.10s) -> Sharp, Tall
        # 4. ST Segment: Plateau (Isoelectric)
        # 5. T Wave: Ventricular Repol. (Asymmetric)
        
        val = 0.0
        
        def gaussian(x, mean, amp, width):
            return amp * math.exp(-((x - mean)**2) / (2 * width**2))
        
        # P Wave (0.15s peak)
        val += gaussian(t, 0.15, 4.0, 0.02)
        
        # Q Wave (0.23s) - Small dip
        val += gaussian(t, 0.23, -3.0, 0.005)
        
        # R Wave (0.25s) - Tall Spike
        val += gaussian(t, 0.25, 35.0, 0.007)
        
        # S Wave (0.27s) - Sharp dip
        val += gaussian(t, 0.27, -8.0, 0.007)
        
        # ST Segment is naturally flat between S (0.28) and T (0.40) due to lack of gaussians
        
        # T Wave (0.50s) - Asymmetric (Slower rise, steeper drop)
        # Modeled as sum of two gaussians or skewed
        val += gaussian(t, 0.48, 6.0, 0.06) # Main body
        val += gaussian(t, 0.52, 3.0, 0.04) # Skew
        
        # Lead Projections
        # Standard 12-lead vectors
        if lead_idx == 0:   # I (Lateral)
            val *= 0.7
        elif lead_idx == 1: # II (Inferior - Classic View)
            val *= 1.0      # Reference
        elif lead_idx == 2: # III (Inferior)
            # III sees less R, more S sometimes, T can be inverted
            val *= 0.6
            val -= gaussian(t, 0.25, 5.0, 0.01) # Reduce R
        elif lead_idx == 3: # aVR (Right Arm)
            val *= -0.9     # INVERTED
        elif lead_idx == 4: # aVL (Left Arm)
            val *= 0.6
            val -= gaussian(t, 0.15, 2.0, 0.02) # Smaller P
        elif lead_idx == 5: # aVF (Foot)
            val *= 0.8

        return val

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # ECG Grid (Small Squares = 1mm = 0.04s)
        painter.setPen(QPen(QColor("#1B331B"), 1))
        
        # Dynamically calc refined step
        # If w = 1 sec (ideally), then 25 large squares?
        # Let's stick to visual grid
        grid_step = 15
        for x in range(0, w, grid_step): painter.drawLine(x, 0, x, h)
        for y in range(0, h, grid_step): painter.drawLine(0, y, w, y)
        
        # Watermark
        painter.setPen(QPen(QColor(255,255,255,20), 1))
        painter.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "NSR")
        
        row_h = h / 6
        
        for i in range(6):
            base_y = (row_h * i) + (row_h / 2) + 15
            
            # Label
            painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            painter.setPen(QPen(QColor("#4CAF50"), 1))
            painter.drawText(8, int(base_y - row_h/4), self.labels[i])
            
            # Draw Wave
            painter.setPen(QPen(QColor("#00E676"), 2))
            pts = []
            
            # Draw all 200 points to scan across width
            # Scale x to fit width
            step_x = w / 200
            for j, val in enumerate(self.data[i]):
                x = int(j * step_x)
                y = int(base_y - val)
                pts.append(QPoint(x, y))
                
            painter.drawPolyline(pts)




# --- MAIN MODULE ---

class MonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Charcoal Background #121212
        self.setStyleSheet("background-color: #121212; font-family: 'Roboto Condensed', 'Arial Narrow', sans-serif;") 
        self.init_ui()

    def init_ui(self):
        # Master Layout: [Nav Sidebar Right] is requested? "System Sidebar runs vertically along the far right edge"
        # My App Architecture has Left Sidebar (Environment). The request asks for "Navigation Sidebar" on Right.
        # I'll put the Monitor "Content" in a layout, and add the Right Sidebar to it locally within this module.
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        
        # --- CENTRAL DASHBOARD ---
        dashboard = QWidget()
        dash_layout = QVBoxLayout(dashboard)
        dash_layout.setContentsMargins(15, 15, 15, 15)
        dash_layout.setSpacing(10)
        
        # 1. HEADER
        header = QWidget()
        header.setFixedHeight(50)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(0,0,0,0)
        
        # Patient Info Tag
        pat_tag = QFrame()
        pat_tag.setStyleSheet("background-color: #263238; border-radius: 5px;")
        ptl = QHBoxLayout(pat_tag)
        ptl.addWidget(QLabel("🛑 👤 Mark  |  202401181048  |  50 Year", styleSheet="color: #DDD; font-weight: bold;"))
        hl.addWidget(pat_tag)
        
        hl.addStretch()
        
        # Error Pill
        err = QLabel("Forehead thermometer bluetooth disconnected")
        err.setStyleSheet("background-color: #D32F2F; color: white; padding: 5px 15px; border-radius: 15px; font-weight: bold;")
        hl.addWidget(err)
        
        hl.addStretch()
        
        # Status
        hl.addWidget(QLabel("📶 🔋 2024/01/18 10:48", styleSheet="color: #FFF;"))
        
        dash_layout.addWidget(header)
        
        # 2. MAIN GRID
        # Split into Left Panel (NIBP...) and Right Panel (ECG...)
        mid_area = QWidget()
        mid_layout = QHBoxLayout(mid_area)
        mid_layout.setContentsMargins(0,0,0,0)
        mid_layout.setSpacing(10)
        
        # --- LEFT COLUMN (Vitals) ---
        left_col = QWidget()
        left_col.setFixedWidth(320)
        lcl = QVBoxLayout(left_col)
        lcl.setContentsMargins(0,0,0,0)
        lcl.setSpacing(10)
        
        # NIBP Card
        nibp = ModernCard("#FFF")
        nl = QGridLayout(nibp)
        nl.addWidget(QLabel("NIBP", styleSheet="color:#AAA; font-weight:bold; font-size:16px;"), 0, 0)
        nl.addWidget(QLabel("mmHg", styleSheet="color:#666; font-size:10px;"), 0, 1)
        
        # Values
        val_nibp = QLabel("115/77")
        val_nibp.setStyleSheet("color: #FFFFFF; font-size: 56px; font-weight: bold;")
        nl.addWidget(val_nibp, 1, 0, 1, 2)
        
        nl.addWidget(QLabel("MAP: 88", styleSheet="color:#AAA; font-weight:bold;"), 1, 2)
        
        btn_nibp = QPushButton("Start 🩺")
        btn_nibp.setFixedSize(90, 40)
        btn_nibp.setStyleSheet("background-color: #2962FF; color: white; border-radius: 8px; font-weight: bold;")
        nl.addWidget(btn_nibp, 0, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
        
        lcl.addWidget(nibp)
        
        # SpO2 & EWS Row (Split)
        row2 = QWidget()
        r2l = QHBoxLayout(row2)
        r2l.setContentsMargins(0,0,0,0)
        r2l.setSpacing(10)
        
        # SpO2
        spo2 = ModernCard()
        sl = QVBoxLayout(spo2)
        sl.addWidget(QLabel("SpO2 %", styleSheet="color:#00B0FF; font-weight:bold;"))
        sl.addWidget(QLabel("98", styleSheet="color:#00B0FF; font-size: 48px; font-weight: bold;"))
        r2l.addWidget(spo2)
        
        # EWS
        ews = ModernCard()
        el = QVBoxLayout(ews)
        el.addWidget(QLabel("EWS", styleSheet="color:#00B0FF; font-weight:bold;"))
        el.addWidget(QLabel("3", styleSheet="color:#00B0FF; font-size: 48px; font-weight: bold;"))
        r2l.addWidget(ews)
        
        lcl.addWidget(row2)
        
        # Temp & PR Row
        row3 = QWidget()
        r3l = QHBoxLayout(row3)
        r3l.setContentsMargins(0,0,0,0)
        
        # Temp
        temp = ModernCard()
        tl = QVBoxLayout(temp)
        tl.addWidget(QLabel("Temp °C", styleSheet="color:#FF9800; font-weight:bold;"))
        tl.addWidget(QLabel("36.9", styleSheet="color:#FF9800; font-size: 48px; font-weight: bold;"))
        r3l.addWidget(temp)
        
        # PR
        pr = ModernCard()
        pl = QVBoxLayout(pr)
        pl.addWidget(QLabel("PR /min", styleSheet="color:#00E676; font-weight:bold;"))
        pl.addWidget(QLabel("78", styleSheet="color:#00E676; font-size: 48px; font-weight: bold;"))
        r3l.addWidget(pr)
        
        lcl.addWidget(row3)
        lcl.addStretch()
        
        mid_layout.addWidget(left_col)
        
        # --- RIGHT COLUMN (ECG) ---
        right_col = ModernCard(bg_color="#181818")
        rcl = QVBoxLayout(right_col)
        
        # ECG Header
        ecg_head = QHBoxLayout()
        ecg_head.addWidget(QLabel("ECG", styleSheet="color:#DDD; font-size:20px; font-weight:bold;"))
        ecg_head.addWidget(QLabel("60", styleSheet="color:#00E676; font-size:48px; font-weight:bold;"))
        ecg_head.addWidget(QLabel("bpm", styleSheet="color:#AAA; margin-top:15px;"))
        ecg_head.addStretch()
        
        btn_ecg = QPushButton("Start ⚡")
        btn_ecg.setFixedSize(120, 45)
        btn_ecg.setStyleSheet("background-color: #2962FF; color: white; border-radius: 8px; font-weight: bold; font-size: 16px;")
        ecg_head.addWidget(btn_ecg)
        
        rcl.addLayout(ecg_head)
        
        # Graph
        self.ecg_plot = MultiLeadECG()
        rcl.addWidget(self.ecg_plot)
        
        mid_layout.addWidget(right_col)
        
        dash_layout.addWidget(mid_area)
        
        # 3. BOTTOM TICKER
        bottom = QFrame()
        bottom.setStyleSheet("background-color: #202020; border-radius: 12px;")
        bottom.setFixedHeight(80)
        bl = QHBoxLayout(bottom)
        
        metrics = [
            ("Breathing", "28", "rpm"),
            ("Intake", "36", "ml"),
            ("Output", "35", "ml"),
            ("Defecation", "651", ""),
            ("Urine", "36", "ml")
        ]
        
        for k, v, s in metrics:
            cont = QVBoxLayout()
            cont.setSpacing(2)
            lbl = QLabel(k)
            lbl.setStyleSheet("color: #AAA; font-size: 11px; font-weight: bold; text-transform: uppercase;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            cont.addWidget(lbl)
            
            w = RecessedLabel(v, s)
            cont.addWidget(w)
            
            bl.addLayout(cont)
            
        dash_layout.addWidget(bottom)
        
        main_layout.addWidget(dashboard)

        # 4. RIGHT SIDEBAR (Navigation)
        # As requested: "System Sidebar runs vertically along the far right edge"
        sidebar = QFrame()
        sidebar.setFixedWidth(80)
        sidebar.setStyleSheet("background-color: #0F0F0F; border-left: 1px solid #333;")
        sl = QVBoxLayout(sidebar)
        sl.setSpacing(30)
        sl.setContentsMargins(0, 30, 0, 30)
        
        menu_items = ["Menu", "Review", "Pat. List", "Save"]
        for txt in menu_items:
            # We don't verify images, assume text for now
            btn = QPushButton(txt)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #888;
                    border: 1px solid #333;
                    border-radius: 10px;
                    font-size: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: white;
                    border-color: #666;
                    background-color: #222;
                }
            """)
            sl.addWidget(btn)
            
        sl.addStretch()
        main_layout.addWidget(sidebar)

