from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from gui.signal_tab import SignalTab
from gui.operations_tab import OperationsTab
from signals import SignalGenerator

class SignalProcessingApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Define signal types and mapping to generator functions
        self.types_of_signal = [
            "szum o rozkładzie jednostajnym", "szum gaussowski", "sygnał sinusoidalny",
            "sygnał sinusoidalny wyprostowany jednopołówkowo", "sygnał sinusoidalnym wyprostowany dwupołówkowo",
            "sygnał prostokątny", "sygnał prostokątny symetryczny", "sygnał trójkątny",
            "skok jednostkowy", "impuls jednostkowy", "szum impulsowy"
        ]

        self.signal_functions = {
            "szum o rozkładzie jednostajnym": SignalGenerator.uniformly_distributed_noise,
            "szum gaussowski": SignalGenerator.gaussian_noise,
            "sygnał sinusoidalny": SignalGenerator.sin_signal,
            "sygnał sinusoidalny wyprostowany jednopołówkowo": SignalGenerator.sin_half_signal,
            "sygnał sinusoidalnym wyprostowany dwupołówkowo": SignalGenerator.sin_twohalf_signal,
            "sygnał prostokątny": SignalGenerator.square_signal,
            "sygnał prostokątny symetryczny": SignalGenerator.square_symmetric_signal,
            "sygnał trójkątny": SignalGenerator.triangle_signal,
            "skok jednostkowy": SignalGenerator.step_signal,
            "impuls jednostkowy": SignalGenerator.unit_impulse,
            "szum impulsowy": SignalGenerator.impulse_noise
        }
        
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle("Cyfrowe przetwarzanie sygnału")
        self.setMinimumSize(1200, 800)
        
        # Create main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Add signal tab
        self.signal_tab = SignalTab(self.types_of_signal, self.signal_functions)
        self.tab_widget.addTab(self.signal_tab, "Sygnały")
        
        # Add operations tab
        self.operations_tab = OperationsTab(self.types_of_signal, self.signal_functions)
        self.tab_widget.addTab(self.operations_tab, "Operacje")