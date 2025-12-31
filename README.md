<div align="center">

# 🏥 Smart Operating Room with Hand Gesture and Computer Vision 

### Next-Generation Operating Room Control System

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="40" height="40"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/qt/qt-original.svg" alt="Qt" width="40" height="40"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/opencv/opencv-original.svg" alt="OpenCV" width="40" height="40"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" alt="SQLite" width="40" height="40"/>
</p>

**Smart Operating Room Controller** is a sophisticated desktop application designed to revolutionize the surgical environment. Combining real-time patient monitoring, environmental controls, and AI-powered gesture recognition into a unified, touch-friendly interface for the modern operating room.

[Features](#-features) • [Installation](#-installation) • [Usage](#️-usage) • [Demo](#-demo) • [Contributing](#-contributing)

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

</div>

---

## ✨ Features

### 🤖 AI-Powered Gesture Control

Revolutionary contact-free control system powered by **MediaPipe** and **OpenCV** for maintaining sterile environments:

| Gesture | Fingers | Function |
|---------|---------|----------|
| 👆 **Navigation** | 1-4 fingers | Switch between Patient, Surgeon, Monitor, and Devices tabs |
| ✋ **Environment** | 5-6 fingers | Adjust lighting intensity automatically |
| 🖐️ **Device Control** | 7-10 fingers | Toggle critical machinery (Monitor, Ventilator) hands-free |

**Benefits:**
- Zero physical contact - maintain sterile environment
- Real-time gesture recognition with low latency
- Intuitive hand-based navigation
- Customizable gesture mappings

### 📊 Advanced Patient Monitor

Professional-grade monitoring dashboard with hospital-quality visualizations:

#### Real-Time ECG Monitoring
- **6-Lead ECG Display**: Smooth, physiology-based waveforms
- **P-QRS-T Complex**: Accurate cardiac cycle simulation
- **High Refresh Rate**: 60+ FPS for fluid visualization
- **Configurable Scales**: Adjustable amplitude and time base

#### Comprehensive Vital Signs
- 💓 **Heart Rate (HR)**: Real-time pulse monitoring with trend analysis
- 🫁 **SpO2**: Oxygen saturation with alarm thresholds
- 🌡️ **Temperature**: Body temperature tracking
- 💉 **NIBP**: Non-invasive blood pressure (Systolic/Diastolic/MAP)
- ⚠️ **EWS Score**: Early Warning Score calculation and visualization

#### Professional UI Design
- **Dark Mode**: "Charcoal" and "Glassmorphism" themes for low-light OR environments
- **High Contrast**: Optimized for quick visual assessment
- **Alarm Integration**: Color-coded alerts for critical values
- **Trend Graphs**: Historical data visualization

### 🌡️ Environmental Control System

Complete OR environment management:

- **Temperature Control**: Precise climate regulation (18°C - 26°C)
- **Humidity Management**: Optimal moisture levels (30% - 70%)
- **Lighting System**: 
  - Adjustable intensity (0-100%)
  - Multiple zones support
  - Gesture-controlled dimming
- **Pressure Monitoring**: Positive/negative pressure control
- **Air Quality**: Filtration status and air changes per hour

### 👨‍⚕️ Surgical Team Dashboard

- **Surgeon Profiles**: Team member information and credentials
- **Procedure Tracking**: Current operation details and timeline
- **Tool Management**: Surgical instrument tracking
- **Role Assignment**: Clear team hierarchy and responsibilities

### 🔌 Medical Device Integration

Centralized control for OR equipment:

- **Patient Monitor**: Power control and status monitoring
- **Anesthesia Machine**: System status and alarms
- **Ventilator**: Operating modes and parameters
- **Surgical Lights**: Intensity and position control
- **Imaging Systems**: C-Arm, X-Ray integration
- **Status Dashboard**: Real-time equipment health monitoring

### 📋 Patient Management

- **Digital Records**: Comprehensive patient information
- **Procedure Timeline**: Real-time surgical progress tracking
- **Medical History**: Quick access to relevant patient data
- **Allergy Alerts**: Critical safety information display

### 🎨 Modern User Experience

- **MacOS-Inspired Design**: Clean, professional interface
- **Smooth Animations**: Fluid transitions and interactions
- **Touch-Friendly**: Optimized for touchscreen displays
- **Fullscreen Mode**: Immersive OR experience
- **Responsive Layout**: Adapts to different screen sizes
- **Keyboard Shortcuts**: Quick access to key functions

---

## 🛠️ Technology Stack

<div align="center">

### Core Technologies

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="60" height="60"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/qt/qt-original.svg" alt="PyQt6" width="60" height="60"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/opencv/opencv-original.svg" alt="OpenCV" width="60" height="60"/>
  <img src="https://www.vectorlogo.zone/logos/google/google-icon.svg" alt="MediaPipe" width="60" height="60"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" alt="SQLite" width="60" height="60"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" alt="NumPy" width="60" height="60"/>
</p>

</div>

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.8+ | Core application logic |
| **GUI Framework** | PyQt6 | Modern desktop interface |
| **Computer Vision** | OpenCV 4.x | Video capture and processing |
| **AI/ML** | MediaPipe | Hand gesture recognition |
| **Database** | SQLite | Patient data management |
| **Graphics** | QPainter | Custom ECG rendering |
| **Data Processing** | NumPy | Signal processing |

---

## 📦 Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager)
- **Webcam** (for gesture control features)
- **Display**: 1920x1080 or higher recommended

### Step-by-Step Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/youssef-ben-letaifa/smart-or-controller.git
   cd smart-or-controller
   ```

2. **Create Virtual Environment** (Recommended)

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Or manually install core packages:

   ```bash
   pip install PyQt6 opencv-python mediapipe numpy
   ```

4. **Verify Installation**

   ```bash
   python --version  # Should be 3.8+
   pip list          # Check installed packages
   ```

5. **Setup Resources**

   Ensure these files are present:
   - `style.qss` - Application stylesheet
   - `SmartOR.desktop` - Linux desktop shortcut (optional)

---

## 🖥️ Usage

### Starting the Application

Run the main application:

```bash
python main.py
```

### First Launch

1. **Splash Screen**: Displays while initializing system components
2. **System Check**: Verifies all modules and dependencies
3. **Camera Detection**: Checks for webcam availability
4. **AI Initialization**: Loads gesture recognition models

### Navigation

**Keyboard Shortcuts:**
- `F11` - Toggle fullscreen mode
- `Ctrl + Q` - Quit application
- `Tab` - Cycle through main tabs
- `Esc` - Exit fullscreen

**Gesture Control:**
- Ensure adequate lighting for camera
- Position hand 30-60cm from camera
- Hold gesture for 1-2 seconds for recognition
- Watch for visual feedback on screen

### Configuration

Edit `config.ini` to customize:
- Camera device index
- Gesture sensitivity
- Alarm thresholds
- Display preferences
- Language settings

---

## 📂 Project Structure

```
smart-or-controller/
│
├── main.py                 # Application Entry Point
├── style.qss              # Global Stylesheet
├── SmartOR.desktop        # Linux Desktop Shortcut
├── requirements.txt       # Python Dependencies
│
├── modules/               # Core Logic Modules
│   ├── environment.py     # Camera & Sliders
│   ├── monitor.py         # ECG & Vitals Rendering
│   ├── machines.py        # Device Control
│   ├── patient.py         # Patient Data Management
│   └── surgeon.py         # Surgeon Dashboard
│
└── ui/                    # UI Components
    ├── mainwindow.py      # Main Window Layout
    └── splash.py          # Boot Animation
```

---

## 🎬 Demo

<div align="center">

### Application Screenshots

| Main Dashboard | Patient Monitor | Environment Control | Application Launch |
|:--------------:|:---------------:|:-------------------:|:------------------:|
| ![Dashboard](Main%20Dashboard.png) | ![Monitor](Patient%20Monitor.png) | ![Environment](Environment%20Control.png) | ![Launch](app%20lunching.png) |


</div>

---

## 🎯 Roadmap

- [x] AI Gesture Recognition
- [x] Real-time ECG Monitoring
- [x] Environmental Controls
- [x] Device Management
- [x] Dark Mode UI
- [ ] Cloud Synchronization
- [ ] Mobile Companion App
- [ ] Voice Commands Integration
- [ ] DICOM Image Viewer
- [ ] Multi-language Support (Arabic, French, English)
- [ ] Remote Monitoring Dashboard
- [ ] Advanced Analytics & Reporting
- [ ] Integration with Hospital Information Systems (HIS)
- [ ] VR/AR Surgical Planning Module

---

## 🔧 Configuration

### Camera Setup

Adjust in `config.ini`:

```ini
[Camera]
device_id = 0
resolution_width = 1280
resolution_height = 720
fps = 30
```

### Gesture Sensitivity

```ini
[Gestures]
detection_confidence = 0.7
tracking_confidence = 0.5
gesture_hold_time = 1.5
```

### Alarm Thresholds

```ini
[Alarms]
hr_low = 50
hr_high = 120
spo2_low = 90
temp_low = 35.5
temp_high = 38.5
```

---

## 🐛 Troubleshooting

### Common Issues

**Camera Not Detected:**
```bash
# Check available cameras
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

**PyQt6 Import Error:**
```bash
pip uninstall PyQt6
pip install PyQt6
```

**Gesture Recognition Not Working:**
- Ensure adequate lighting
- Check camera permissions
- Verify MediaPipe installation
- Update graphics drivers

**Performance Issues:**
- Reduce ECG refresh rate in settings
- Disable gesture control if not needed
- Close other resource-intensive applications

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute

1. **Fork the Repository**
   ```bash
   git clone https://github.com/youssef-ben-letaifa/smart-or-controller.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make Your Changes**
   - Follow PEP 8 style guidelines
   - Add comments for complex logic
   - Update documentation

4. **Test Your Changes**
   ```bash
   python -m pytest tests/
   ```

5. **Commit and Push**
   ```bash
   git commit -m "Add: Your feature description"
   git push origin feature/YourFeatureName
   ```

6. **Create Pull Request**

### Development Guidelines

- Write clear, descriptive commit messages
- Add unit tests for new features
- Update documentation as needed
- Follow existing code structure
- Test on multiple platforms if possible

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🌍 Translations
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations

---

## 📜 License

MIT License

Copyright (c) 2024 Youssef BEN LETAIFA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 👨‍💻 Author

**Youssef BEN LETAIFA**

- GitHub: [@youssef-ben-letaifa](https://github.com/youssef-ben-letaifa)
- LinkedIn: [Youssef Ben Letaifa](https://www.linkedin.com/in/youssefbenletaifa/)
- Portfolio: [youssef-ben-letaifa.github.io](https://youssef-ben-letaifa.github.io/ben.letaifa.youssef/)
- Email: youssef.benletaifa@intek.u-jendouba.tn
---



## ⚠️ Disclaimer

This software is intended for **educational and research purposes only**. It is **NOT certified for clinical use** and should not be used in actual medical procedures without proper validation, testing, and regulatory approval.

Always consult qualified medical professionals and follow established medical protocols.

---

<div align="center">

### 💙 If you find this project useful, please give it a ⭐!

**Built for the Future of Healthcare**

![GitHub stars](https://img.shields.io/github/stars/youssef-ben-letaifa/smart-or-controller?style=social)
![GitHub forks](https://img.shields.io/github/forks/youssef-ben-letaifa/smart-or-controller?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/youssef-ben-letaifa/smart-or-controller?style=social)

**Version 6.0** | Last Updated: December 2024

</div>
