import sys
from PyQt5.QtWidgets import QApplication
from interface import SignalProcessingApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalProcessingApp()
    window.show()
    sys.exit(app.exec_())
