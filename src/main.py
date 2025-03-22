import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from interface import SignalProcessApp

def interface_new():
    app = QApplication(sys.argv)
    main_window = QMainWindow()  # Renamed the variable to avoid conflict
    ui = SignalProcessApp()      # This now refers to the class, not the instance
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # interface_old()
    interface_new()