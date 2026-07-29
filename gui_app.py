import sys
import os
import cv2
import subprocess
import time
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedLayout, QMessageBox, QSplashScreen
)
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer

import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GestureSync UI")
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon(resource_path("assets/app_icon.ico")))

        self.hand_process = None
        self.head_process = None

        # Webcam feed setup
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Central layout
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.main_layout = QHBoxLayout()
        self.sidebar = QVBoxLayout()
        self.pages = QStackedLayout()

        # Sidebar buttons
        self.home_btn = QPushButton("🏠  Home")
        self.hand_btn = QPushButton("🖐  Hand Mode")
        self.head_btn = QPushButton("🧠  Head Mode")
        self.stop_btn = QPushButton("🛑  Stop Tracking")

        for btn in [self.home_btn, self.hand_btn, self.head_btn, self.stop_btn]:
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                      stop:0 #444, stop:1 #666);
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #0078D7;
                }
            """)

        self.sidebar.addWidget(self.home_btn)
        self.sidebar.addWidget(self.hand_btn)
        self.sidebar.addWidget(self.head_btn)
        self.sidebar.addWidget(self.stop_btn)
        self.sidebar.addStretch()

        # --------------------------
        # Home Page with Splash Cards
        # --------------------------
        self.home_page = QWidget()
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFixedHeight(300)

        self.card_layout = QHBoxLayout()

        def create_card(icon_path, title, handler):
            card = QWidget()
            vbox = QVBoxLayout()

            icon = QLabel()
            icon.setPixmap(QPixmap(icon_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon.setAlignment(Qt.AlignCenter)

            label = QLabel(title)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")

            button = QPushButton("Open")
            button.clicked.connect(handler)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #0078D7;
                    color: white;
                    border-radius: 8px;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background-color: #005A9E;
                }
            """)

            vbox.addWidget(icon)
            vbox.addWidget(label)
            vbox.addWidget(button)
            card.setLayout(vbox)
            card.setStyleSheet("background-color: #333; border-radius: 15px; padding: 15px;")
            return card

        self.card_layout.addWidget(create_card("assets/hand_icon.png", "Hand Tracking", self.run_hand_tracking))
        self.card_layout.addWidget(create_card("assets/head_icon.png", "Head Tracking", self.run_head_tracking))
        self.card_layout.addWidget(create_card("assets/cam_icon.png", "Live Preview", self.show_home))

        card_container = QWidget()
        card_container.setLayout(self.card_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.preview_label)
        layout.addWidget(card_container)
        self.home_page.setLayout(layout)

        self.home_page.setStyleSheet("""
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #50c9c3, stop:0.5 #96deda, stop:1 #50c9c3
            );
        """)

        # --------------------------
        # Other Pages
        # --------------------------
        self.hand_page = QLabel("🖐 Hand tracking running...\nUse hand gestures to control.")
        self.hand_page.setAlignment(Qt.AlignCenter)
        self.head_page = QLabel("🧠 Head tracking running...\nUse facial expressions and head movement.")
        self.head_page.setAlignment(Qt.AlignCenter)

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.hand_page)
        self.pages.addWidget(self.head_page)

        # Button actions
        self.home_btn.clicked.connect(self.show_home)
        self.hand_btn.clicked.connect(self.run_hand_tracking)
        self.head_btn.clicked.connect(self.run_head_tracking)
        self.stop_btn.clicked.connect(self.stop_tracking)

        # Layout assembly
        self.main_layout.addLayout(self.sidebar, 1)
        self.main_layout.addLayout(self.pages, 4)
        self.container.setLayout(self.main_layout)

        # Start on home with preview
        self.pages.setCurrentWidget(self.home_page)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.preview_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def show_home(self):
        self.stop_tracking()  # Make sure tracking is stopped
        self.pages.setCurrentWidget(self.home_page)
        if not self.capture.isOpened():
            self.capture = cv2.VideoCapture(0)
        self.timer.start(30)

    def run_hand_tracking(self):
        self.stop_tracking()
        self.pages.setCurrentWidget(self.hand_page)
        self.timer.stop()
        self.capture.release()
        self.hand_process = subprocess.Popen([sys.executable, "Gesture_controller_2.py"])
        self.log_activity("Hand Tracking Started")

    def run_head_tracking(self):
        self.stop_tracking()
        self.pages.setCurrentWidget(self.head_page)
        self.timer.stop()
        self.capture.release()
        self.head_process = subprocess.Popen([sys.executable, "livetrack.py"])
        self.log_activity("Head Tracking Started")

    def stop_tracking(self):
        stopped = False
        if self.hand_process and self.hand_process.poll() is None:
            self.hand_process.terminate()
            self.hand_process.wait()
            self.hand_process = None
            self.log_activity("Hand Tracking Stopped")
            stopped = True

        if self.head_process and self.head_process.poll() is None:
            self.head_process.terminate()
            self.head_process.wait()
            self.head_process = None
            self.log_activity("Head Tracking Stopped")
            stopped = True

        if not self.capture.isOpened():
            self.capture = cv2.VideoCapture(0)

        if stopped:
            QMessageBox.information(self, "GestureSync", "Tracking stopped.")

        self.timer.start(30)
        self.pages.setCurrentWidget(self.home_page)

    def log_activity(self, message):
        with open("gesture_log.txt", "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

    def closeEvent(self, event):
        self.capture.release()
        self.stop_tracking()
        event.accept()


# ----------------------
# Splash Screen Launch
# ----------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash_pix = QPixmap(resource_path("assets/splash_image.png"))
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    time.sleep(2)  # Simulated loading

    window = MainWindow()
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())
