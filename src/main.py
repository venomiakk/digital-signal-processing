from signals import sin_signal
from interface import SignalProcessingApp
from PyQt5.QtWidgets import QApplication

def main():
    #sin_signal()
    app = QApplication([])
    ex = SignalProcessingApp()
    app.exec_()


if __name__ == "__main__":
    main()
