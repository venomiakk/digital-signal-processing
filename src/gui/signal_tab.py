from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from gui.ui_components import create_signal_column
from gui.utils import generate_signal, plot_on_canvas, save_signal_to_file

class SignalTab(QWidget):
    def __init__(self, types_of_signal, signal_functions):
        super().__init__()
        self.types_of_signal = types_of_signal
        self.signal_functions = signal_functions
        self.current_signal = None
        self.parameter_inputs = {}
        self.setupUI()
        
    def setupUI(self):
        main_layout = QVBoxLayout(self)
        
        # Create a vertical splitter to separate parameters from plot
        splitter = QSplitter(Qt.Vertical)  # Changed from Qt.Horizontal to Qt.Vertical
        main_layout.addWidget(splitter)
        
        # Top section: Signal parameters container
        params_container = QWidget()
        params_layout = QVBoxLayout(params_container)
        params_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create signal column
        self.signal_col, self.parameter_inputs = create_signal_column(
            "Parametry sygnału", 
            self.plot_signal,
            self.save_signal,
            self.types_of_signal
        )
        params_layout.addLayout(self.signal_col)
        
        # Bottom section: Plot container
        plot_container = QWidget()
        plot_layout = QVBoxLayout(plot_container)
        plot_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add plot header
        plot_header = QLabel("Wizualizacja sygnału")
        plot_header.setStyleSheet("font-weight: bold; font-size: 14px;")
        plot_layout.addWidget(plot_header)
        
        # Create canvas for plotting
        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        plot_layout.addWidget(self.canvas)
        
        # Add containers to splitter
        splitter.addWidget(params_container)
        splitter.addWidget(plot_container)
        
        # Set initial splitter sizes (30% for params, 70% for plot)
        splitter.setSizes([300, 700])
    
    def plot_signal(self):
        # Get signal selector from column
        signal_selector = self.signal_col.signal_selector
        selected_signal = signal_selector.currentText()
        
        # Generate signal based on UI parameters
        signal_obj = generate_signal(
            selected_signal,
            self.signal_functions,
            self.parameter_inputs
        )
        
        if signal_obj:
            # Store current signal
            self.current_signal = signal_obj
            
            # Plot signal on canvas
            try:
                num_bins = int(self.parameter_inputs['bins'].text())
            except (ValueError, TypeError):
                num_bins = 20
                
            plot_on_canvas(signal_obj, self.canvas, num_bins)
    
    def save_signal(self):
        save_signal_to_file(self, self.current_signal)