"""
Smart Dictator — AI Voice Accessibility Application
SIH 2026 Project

Entry point. Run with:
    pip install PySide6
    python main.py
"""
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Smart Dictator")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SIH 2026")

    # Set a clean, readable default font
    app.setFont(QFont("Segoe UI", 10))

    from ui.main_window import MainWindow
    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
