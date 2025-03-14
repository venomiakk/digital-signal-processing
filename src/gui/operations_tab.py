from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QComboBox, QPushButton, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from gui.ui_components import create_signal_column
from gui.utils import generate_signal, plot_on_canvas, save_signal_to_file
from signals import SignalOperations

class OperationsTab(QWidget):
    def __init__(self, types_of_signal, signal_functions):
        super().__init__()
        self.types_of_signal = types_of_signal
        self.signal_functions = signal_functions
        self.result_signal = None
        self.parameter_inputs = {}
        self.setupUI()
        
    def setupUI(self):
        main_layout = QVBoxLayout(self)
        
        # Create a vertical splitter to separate parameters from plots
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # Top section: Parameters container
        params_container = QWidget()
        params_layout = QHBoxLayout(params_container)
        
        # Create first signal column
        self.signal1_col, self.parameter_inputs1 = create_signal_column(
            "Sygnał 1", 
            self.plot_signal1,
            self.save_signal1,
            self.types_of_signal
        )
        params_layout.addLayout(self.signal1_col)
        
        # Create operation selector in the middle
        op_container = QWidget()
        op_layout = QVBoxLayout(op_container)
        op_layout.addWidget(QLabel("Operacja"))
        
        self.operation_selector = QComboBox()
        operations = ["Dodawanie", "Odejmowanie", "Mnożenie", "Dzielenie"]
        self.operation_selector.addItems(operations)
        op_layout.addWidget(self.operation_selector)
        
        # Add execute operation button
        execute_button = QPushButton("Wykonaj operację")
        execute_button.clicked.connect(self.execute_operation)
        op_layout.addWidget(execute_button)
        
        # Add save result button
        save_result_button = QPushButton("Zapisz wynik")
        save_result_button.clicked.connect(self.save_result)
        op_layout.addWidget(save_result_button)
        
        op_layout.addStretch(1)
        params_layout.addWidget(op_container)
        
        # Create second signal column
        self.signal2_col, self.parameter_inputs2 = create_signal_column(
            "Sygnał 2", 
            self.plot_signal2,
            self.save_signal2,
            self.types_of_signal
        )
        params_layout.addLayout(self.signal2_col)
        
        # Bottom section: Plots container
        plots_container = QWidget()
        plots_layout = QHBoxLayout(plots_container)
        
        # Signal 1 plot
        signal1_plot_layout = QVBoxLayout()
        signal1_plot_layout.addWidget(QLabel("Sygnał 1"))
        self.canvas_signal1 = FigureCanvas(Figure(figsize=(4, 3)))
        signal1_plot_layout.addWidget(self.canvas_signal1)
        plots_layout.addLayout(signal1_plot_layout)
        
        # Signal 2 plot
        signal2_plot_layout = QVBoxLayout()
        signal2_plot_layout.addWidget(QLabel("Sygnał 2"))
        self.canvas_signal2 = FigureCanvas(Figure(figsize=(4, 3)))
        signal2_plot_layout.addWidget(self.canvas_signal2)
        plots_layout.addLayout(signal2_plot_layout)
        
        # Result plot
        result_plot_layout = QVBoxLayout()
        result_plot_layout.addWidget(QLabel("Wynik operacji"))
        self.canvas_result = FigureCanvas(Figure(figsize=(4, 3)))
        result_plot_layout.addWidget(self.canvas_result)
        plots_layout.addLayout(result_plot_layout)
        
        # Add containers to splitter
        splitter.addWidget(params_container)
        splitter.addWidget(plots_container)
        
        # Set initial splitter sizes (40% for params, 60% for plots)
        splitter.setSizes([400, 600])
    
    def plot_signal1(self):
        """Generate and plot signal 1"""
        signal_selector = self.signal1_col.signal_selector
        selected_signal = signal_selector.currentText()
        
        signal_obj = generate_signal(
            selected_signal,
            self.signal_functions,
            self.parameter_inputs1
        )
        
        if signal_obj:
            self.signal1 = signal_obj  # Store for operations
            try:
                num_bins = int(self.parameter_inputs1['bins'].text())
            except (ValueError, TypeError):
                num_bins = 20
                
            plot_on_canvas(signal_obj, self.canvas_signal1, num_bins)
    
    def plot_signal2(self):
        """Generate and plot signal 2"""
        signal_selector = self.signal2_col.signal_selector
        selected_signal = signal_selector.currentText()
        
        signal_obj = generate_signal(
            selected_signal,
            self.signal_functions,
            self.parameter_inputs2
        )
        
        if signal_obj:
            self.signal2 = signal_obj  # Store for operations
            try:
                num_bins = int(self.parameter_inputs2['bins'].text())
            except (ValueError, TypeError):
                num_bins = 20
                
            plot_on_canvas(signal_obj, self.canvas_signal2, num_bins)
    
    def execute_operation(self):
        """Execute the selected operation on both signals"""
        if not hasattr(self, 'signal1') or not hasattr(self, 'signal2'):
            QMessageBox.warning(
                self,
                "Brak sygnału",
                "Proszę wygenerować oba sygnały przed wykonaniem operacji.",
                QMessageBox.Ok
            )
            return
        
        # Perform selected operation
        operation = self.operation_selector.currentText()
        if operation == "Dodawanie":
            result = SignalOperations.add_signals(self.signal1, self.signal2)
        elif operation == "Odejmowanie":
            result = SignalOperations.subtract_signals(self.signal1, self.signal2)
        elif operation == "Mnożenie":
            result = SignalOperations.multiply_signals(self.signal1, self.signal2)
        elif operation == "Dzielenie":
            result = SignalOperations.divide_signals(self.signal1, self.signal2)
        
        if result:
            # Store the result signal
            self.result_signal = result
            
            # Use bins from first signal (arbitrary choice)
            try:
                num_bins = int(self.parameter_inputs1['bins'].text())
            except (ValueError, TypeError):
                num_bins = 20
                
            # Plot the result
            plot_on_canvas(result, self.canvas_result, num_bins)
        else:
            QMessageBox.warning(
                self,
                "Błąd operacji",
                "Nie udało się wykonać operacji na sygnałach.",
                QMessageBox.Ok
            )
    
    def save_signal1(self):
        if hasattr(self, 'signal1'):
            save_signal_to_file(self, self.signal1)
        else:
            QMessageBox.warning(
                self,
                "Brak sygnału do zapisania",
                "Najpierw wygeneruj sygnał 1.",
                QMessageBox.Ok
            )
    
    def save_signal2(self):
        if hasattr(self, 'signal2'):
            save_signal_to_file(self, self.signal2)
        else:
            QMessageBox.warning(
                self,
                "Brak sygnału do zapisania",
                "Najpierw wygeneruj sygnał 2.",
                QMessageBox.Ok
            )
    
    def save_result(self):
        if hasattr(self, 'result_signal'):
            save_signal_to_file(self, self.result_signal)
        else:
            QMessageBox.warning(
                self,
                "Brak wynikowego sygnału",
                "Najpierw wykonaj operację na sygnałach.",
                QMessageBox.Ok
            )