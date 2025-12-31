
import sys
from PyQt6.QtWidgets import QApplication
from ui.splash import SplashScreen
from ui.mainwindow import MainWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        # Load Stylesheet
        try:
            with open("style.qss", "r") as f:
                self.app.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: style.qss not found.")

        self.start_splash()

    def start_splash(self):
        self.splash = SplashScreen()
        self.splash.finished.connect(self.start_main)
        self.splash.show()

    def start_main(self):
        self.main_window = MainWindow()
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    controller = AppController()
    controller.run()
