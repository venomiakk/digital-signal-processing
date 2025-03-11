from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from signals import *
from plots import plot_signal


class SignalProcessingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cyfrowe przetwarzanie sygnału")

        self.types_of_signal = [
            "szum o rozkładzie jednostajnym", "szum gaussowski", "sygnał sinusoidalny",
            "sygnał sinusoidalny wyprostowany jednopołówkowo", "sygnał sinusoidalnym wyprostowany dwupołówkowo",
            "sygnał prostokątny", "sygnał prostokątny symetryczny", "sygnał trójkątny",
            "skok jednostkowy", "impuls jednostkowy", "szum impulsowy"
        ]

        self.signal_functions = {
            "szum o rozkładzie jednostajnym": uniformly_distributed_noise,
            "szum gaussowski": gaussian_noise,
            "sygnał sinusoidalny": sin_signal,
            "sygnał sinusoidalny wyprostowany jednopołówkowo": sin_half_signal,
            "sygnał sinusoidalnym wyprostowany dwupołówkowo": sin_twohalf_signal,
            "sygnał prostokątny": square_signal,
            "sygnał prostokątny symetryczny": square_symmetric_signal,
            "sygnał trójkątny": triangle_signal,
            "skok jednostkowy": step_signal,
            "impuls jednostkowy": unit_impulse,
            "szum impulsowy": impulse_noise
        }

        self.tab_widget = QTabWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tab_widget)

        self.create_signal_tab()
        self.create_operations_tab()

        self.show()

    def create_signal_tab(self):
        signal_tab = QWidget()
        layout = QVBoxLayout()
        signal_tab.setLayout(layout)

        self.signal_col = self.create_signal_column("Parametry sygnału", self.plot_signal)

        layout.addLayout(self.signal_col)

        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        layout.addWidget(self.canvas)

        self.tab_widget.addTab(signal_tab, "Sygnały")

    def create_operations_tab(self):
        operations_tab = QWidget()
        layout = QVBoxLayout()
        operations_tab.setLayout(layout)

        # Add widgets for operations on signals here
        operation_label = QLabel("Operacje na sygnałach")
        layout.addWidget(operation_label)

        self.tab_widget.addTab(operations_tab, "Operacje")

    def create_signal_column(self, title, plot_method):
        col_layout = QVBoxLayout()

        label = QLabel(title)
        col_layout.addWidget(label)

        signal_selector = QComboBox()
        signal_selector.addItems(self.types_of_signal)
        col_layout.addWidget(signal_selector)

        amplitude_input = self.create_input_field("Amplituda:", col_layout)
        duration_input = self.create_input_field("Czas trwania:", col_layout)
        t1_input = self.create_input_field("Czas 1:", col_layout)
        t2_input = self.create_input_field("Czas 2:", col_layout)
        sampling_input = self.create_input_field("Próbkowanie:", col_layout)

        plot_button = QPushButton("Create")
        plot_button.clicked.connect(plot_method)
        col_layout.addWidget(plot_button)

        return col_layout

    def create_input_field(self, label_text, layout):
        label = QLabel(label_text)
        layout.addWidget(label)
        line_edit = QLineEdit()
        layout.addWidget(line_edit)
        return line_edit

    def plot_signal(self):
        self.plot(self.signal_col, self.canvas)

    def plot(self, col_layout, canvas):
        signal_selector = col_layout.itemAt(1).widget()
        selected_signal = signal_selector.currentText()
        signal_function = self.signal_functions.get(selected_signal)
        if signal_function:
            sig, time = signal_function()
            fig = plot_signal(sig, time)
            canvas.figure.clear()
            ax1 = canvas.figure.add_subplot(121)
            ax2 = canvas.figure.add_subplot(122)
            ax1.plot(time, sig)
            ax1.set_xlabel("Time [s]")
            ax1.set_ylabel("Amplitude")
            ax1.set_title("Signal")
            ax1.grid()
            ax2.hist(sig, bins=20)
            ax2.set_title("Histogram")
            ax2.set_xlabel("Amplitude")
            ax2.set_ylabel("Frequency")
            fig.tight_layout()
            canvas.draw()