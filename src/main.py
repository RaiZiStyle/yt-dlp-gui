#!/usr/bin/env python3
# Local import
from PySide6.QtWidgets import QApplication
import sys



        
    

if __name__ == "__main__":
    from GUI import MainWindow
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    app.setStyleSheet("""
        QLineEdit {
            padding: 6px;
        }
        QGroupBox {
            font-weight: bold;
            margin-top: 16px;
            padding-top: 6px;
            border: 1px solid #aaaaaa;
            border-radius: 4px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 4px;
        }
        QPushButton {
            min-height: 32px;
        }

        QProgressBar {
            height: 22px;
        }

        """)

    window = MainWindow()
    window.show()

    print("Taille réelle :", window.size())  # taille en pixels logiques
    print("Scale factor :", app.devicePixelRatio())  # facteur de scaling

    sys.exit(app.exec())
