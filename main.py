# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("DayZ Reward Editor")

    # 🖤 Dark Theme Styling
    dark_style = """
    QWidget {
        background-color: #121212;
        color: #e0e0e0;
        font-family: Segoe UI;
        font-size: 10pt;
    }

    QLineEdit, QSpinBox, QListWidget, QTabWidget {
        background-color: #1e1e1e;
        border: 1px solid #333;
        padding: 4px;
        color: #f0f0f0;
    }

    QPushButton {
        background-color: #2e2e2e;
        border: 1px solid #555;
        padding: 6px;
        color: #f0f0f0;
    }

    QPushButton:hover {
        background-color: #444;
    }

    QLabel {
        color: #bbbbbb;
    }

    QStatusBar {
        background-color: #1c1c1c;
        color: #aaaaaa;
    }

    QTabBar::tab {
        background-color: #1e1e1e;
        color: #cccccc;
        padding: 6px 12px;
        border: 1px solid #444;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }

    QTabBar::tab:selected {
        background-color: #2a2a2a;
        border-color: #666;
        color: #ffffff;
        font-weight: normal;
    }

    QTabWidget::pane {
        border-top: 1px solid #444;
        top: -1px;
    }
    """
    app.setStyleSheet(dark_style)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
