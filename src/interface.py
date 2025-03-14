from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QComboBox, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLineEdit, QTabWidget, 
                            QFormLayout, QSizePolicy, QFileDialog, QMessageBox,
                            QSplitter, QGroupBox, QTableWidget, QHeaderView,
                            QTextEdit, QTableWidgetItem)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from signals import *
from plots import plot_signal
from filesRW import FileRW

# TODO: 
#* w operations_tab.py:
#* - przesunięcie, czas trwania, próbkowanie powinny być ustalane dla obu sygnałów jednocześnie
#* wypisywanie "statystyk" (rms, avg itd) sygnału np. pod wykresem



class SignalProcessingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_signal = None
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

        self.tab_widget = QTabWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tab_widget)

        self.create_signal_tab()
        self.create_operations_tab()
        self.create_file_tab()

        self.show()

    def create_signal_tab(self):
        signal_tab = QWidget()
        layout = QVBoxLayout()
        signal_tab.setLayout(layout)

        self.signal_col = self.create_signal_column("Parametry sygnału", self.plot_signal, self.load_signal_for_tab)

        layout.addLayout(self.signal_col)

        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        layout.addWidget(self.canvas)

        self.tab_widget.addTab(signal_tab, "Sygnały")

    def create_operations_tab(self):
        operations_tab = QWidget()
        layout = QVBoxLayout()
        operations_tab.setLayout(layout)

        # Create horizontal layout for signal selectors and operation selector
        signals_layout = QHBoxLayout()
        
        # Create first signal column with specific plot and load methods
        self.signal1_col = self.create_signal_column("Sygnał 1", self.plot_signal1, self.load_signal1)
        signals_layout.addLayout(self.signal1_col)
        
        # Create operation selector in the middle
        op_layout = QVBoxLayout()
        op_label = QLabel("Operacja")
        op_layout.addWidget(op_label)
        
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
        signals_layout.addLayout(op_layout)
        
        # Create second signal column with specific plot and load methods
        self.signal2_col = self.create_signal_column("Sygnał 2", self.plot_signal2, self.load_signal2)
        signals_layout.addLayout(self.signal2_col)
        
        # Add the signals layout to the main layout
        layout.addLayout(signals_layout)
        
        # Create canvases for plotting
        plots_layout = QHBoxLayout()
        
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
        
        layout.addLayout(plots_layout)
        
        self.tab_widget.addTab(operations_tab, "Operacje")
        
    def execute_operation(self):
        # Check if signals are available (either generated or loaded)
        signal1 = getattr(self, 'signal1', None)
        signal2 = getattr(self, 'signal2', None)
        
        # If signals aren't loaded, try to generate them from UI
        if not signal1:
            signal1 = self.generate_signal_from_column(self.signal1_col)
        if not signal2:
            signal2 = self.generate_signal_from_column(self.signal2_col)
        
        if not signal1 or not signal2:
            QMessageBox.warning(
                self,
                "Brak sygnału",
                "Proszę upewnić się, że oba sygnały są dostępne (wygenerowane lub wczytane z pliku).",
                QMessageBox.Ok
            )
            return
        
        # Plot both input signals
        self.plot_on_canvas(signal1, self.canvas_signal1)
        self.plot_on_canvas(signal2, self.canvas_signal2)
        
        # Perform selected operation
        operation = self.operation_selector.currentText()
        if operation == "Dodawanie":
            result = SignalOperations.add_signals(signal1, signal2)
        elif operation == "Odejmowanie":
            result = SignalOperations.subtract_signals(signal1, signal2)
        elif operation == "Mnożenie":
            result = SignalOperations.multiply_signals(signal1, signal2)
        elif operation == "Dzielenie":
            result = SignalOperations.divide_signals(signal1, signal2)
        
        if result:
            # Store the result signal
            self.result_signal = result
            # Plot the result
            self.plot_on_canvas(result, self.canvas_result)
        else:
            QMessageBox.warning(
                self,
                "Błąd operacji",
                "Nie udało się wykonać operacji na sygnałach.",
                QMessageBox.Ok
            )

    def generate_signal_from_column(self, col_layout):
        signal_selector = col_layout.itemAt(0).widget()
        selected_signal = signal_selector.currentText()
        signal_function = self.signal_functions.get(selected_signal)
        
        if not signal_function:
            return None
            
        # Map UI parameter names to function parameter names
        param_mapping = {
            'amplitude': 'A',
            'duration': 'd',
            't1': 't_start',
            'period': 'T',
            'sampling': 'sampling_rate',
            'kw': 'kw',
            'sample_number': 'n_spike',
            'probability': 'p'
        }
        
        # Get values from enabled input fields
        params = {}
        for ui_param, func_param in param_mapping.items():
            input_field = self.parameter_inputs.get(ui_param)
            if input_field and input_field.isEnabled() and input_field.text():
                try:
                    params[func_param] = float(input_field.text())
                except ValueError:
                    pass
        
        # Call the signal function with parameters
        return signal_function(**params)

    def plot_on_canvas(self, signal_obj, canvas):
        if not signal_obj:
            return
            
        sig, time = signal_obj.signal, signal_obj.time
        
        try:
            num_bins = int(self.parameter_inputs['bins'].text())
        except (ValueError, TypeError):
            num_bins = 20
        
        if signal_obj.discrete_signal:
            fig = plot_points(sig, time, bins_no=num_bins)
        else:
            fig = plot_signal(sig, time, bins_no=num_bins)
        
        canvas.figure.clear()
        canvas.figure = fig
        canvas.draw()

    def save_result(self):
        if not hasattr(self, 'result_signal') or self.result_signal is None:
            QMessageBox.warning(
                self,
                "Brak sygnału do zapisania",
                "Nie wykonano jeszcze operacji. Wykonaj operację, aby uzyskać sygnał do zapisania.",
                QMessageBox.Ok
            )
            return
        
        # Open file dialog to select save location
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Zapisz wynik operacji", 
            "", 
            "Signal Files (*.pkl);;All Files (*)", 
            options=options
        )
        
        if filename:
            # Add .pkl extension if not provided
            if not filename.endswith('.pkl'):
                filename += '.pkl'
            
            # Save the signal using FileRW
            if FileRW.write_signal_to_file(self.result_signal, filename):
                QMessageBox.information(
                    self,
                    "Sygnał zapisany",
                    f"Wynikowy sygnał został zapisany w: {filename}",
                    QMessageBox.Ok
                )
            else:
                QMessageBox.critical(
                    self,
                    "Błąd zapisu sygnału",
                    "Wystąpił błąd podczas zapisu wynikowego sygnału.",
                    QMessageBox.Ok
                )

    def create_signal_column(self, title, plot_method, load_method=None):
        col_layout = QVBoxLayout()
        # col_layout.setSpacing(0)
        # label = QLabel(title)
        # col_layout.addWidget(label)
        # col_layout.addSpacing(5)
        signal_selector = QComboBox()
        signal_selector.addItems(self.types_of_signal)
        # Set maximum visible items to show all signals without scrolling
        signal_selector.setMaxVisibleItems(len(self.types_of_signal))
        # Connect the signal selector to update input fields
        signal_selector.currentTextChanged.connect(self.update_input_fields)
        col_layout.addWidget(signal_selector)

        # Create form layout for parameters
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        amplitude_input = QLineEdit()
        amplitude_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow("Amplituda:", amplitude_input)
        
        duration_input = QLineEdit()
        duration_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow("Czas trwania [s]:", duration_input)
        
        t_start_input = QLineEdit()
        t_start_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow("Przesunięcie [s]:", t_start_input)
        
        sampling_input = QLineEdit()
        sampling_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow("Próbkowanie [próbki/s]:", sampling_input)
        
        period_input = QLineEdit()
        period_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow("Okres [s]:", period_input)

        kw_input = QLineEdit()
        kw_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow("Współczynnik wypełnienia:", kw_input)

        sample_number_input = QLineEdit()
        sample_number_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow("Numer próbki:", sample_number_input)

        probability_input = QLineEdit()
        probability_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout.addRow("Prawdopodobieństwo:", probability_input)

        col_layout.addLayout(form_layout)

        # Create a horizontal layout for buttons
        button_row = QHBoxLayout()
        
        # Add plot button to the horizontal layout
        plot_button = QPushButton("Wygeneruj sygnał")
        plot_button.setFixedWidth(100)
        plot_button.clicked.connect(plot_method)
        button_row.addWidget(plot_button)

        # Add save button
        save_button = QPushButton("Zapisz sygnał")
        save_button.setFixedWidth(100)
        save_button.clicked.connect(self.save_signal)
        button_row.addWidget(save_button)
        
        # Add load from file button
        load_button = QPushButton("Wczytaj z pliku")
        load_button.setFixedWidth(100)
        if load_method:
            load_button.clicked.connect(load_method)
        button_row.addWidget(load_button)
            
        # Add spacing between elements
        button_row.addSpacing(10)
        
        # Add bin number label and input to the horizontal layout
        button_row.addStretch(1)
        button_row.addWidget(QLabel("Liczba przedziałów histogramu:"))
        
        bin_input = QLineEdit()
        bin_input.setText("20")  # Default value
        bin_input.setFixedWidth(80)  # Make it reasonably sized
        button_row.addWidget(bin_input)
        
        # Add the horizontal layout to the main column layout
        col_layout.addLayout(button_row)
        
        # Store references to all inputs
        self.parameter_inputs = {
            'amplitude': amplitude_input,
            'duration': duration_input,
            't1': t_start_input,
            'sampling': sampling_input,
            'period': period_input,
            'kw': kw_input,
            'sample_number': sample_number_input,
            'probability': probability_input,
            'bins': bin_input  # Add the new input to parameter dictionary
        }

        # Save reference to the signal selector
        self.signal_selector = signal_selector
        
        # Set initial state of input fields
        self.update_input_fields(signal_selector.currentText())
        
        return col_layout

    def update_input_fields(self, signal_type):
        # Define which parameters are needed for each signal type
        param_mapping = {
            "szum o rozkładzie jednostajnym": ['amplitude', 'duration', 'sampling'],
            "szum gaussowski": ['amplitude', 'duration', 'sampling'],
            "sygnał sinusoidalny": ['amplitude', 'duration', 't1', 'sampling', 'period'],
            "sygnał sinusoidalny wyprostowany jednopołówkowo": ['amplitude', 'duration', 't1', 'sampling', 'period'],
            "sygnał sinusoidalnym wyprostowany dwupołówkowo": ['amplitude', 'duration', 't1', 'sampling', 'period'],
            "sygnał prostokątny": ['amplitude', 'duration', 't1', 'sampling', 'period', 'kw'],
            "sygnał prostokątny symetryczny": ['amplitude', 'duration', 't1', 'sampling', 'period', 'kw'],
            "sygnał trójkątny": ['amplitude', 'duration', 't1', 'sampling', 'period', 'kw'],
            "skok jednostkowy": ['amplitude', 'duration', 't1', 'sampling'],
            "impuls jednostkowy": ['amplitude', 'duration', 'sampling', 'sample_number'],
            "szum impulsowy": ['amplitude', 'duration', 'sampling', 'probability']
        }
        
        # Get the parameters needed for the selected signal type
        needed_params = param_mapping.get(signal_type, [])
        
        # Enable/disable input fields based on the needed parameters
        for param_name, input_field in self.parameter_inputs.items():
            
            if param_name == 'bins':
                continue

            if param_name in needed_params:
                input_field.setEnabled(True)
            else:
                input_field.setEnabled(False)
                input_field.clear()  # Clear the disabled fields

    def create_input_field(self, label_text, layout):
        label = QLabel(label_text)
        layout.addWidget(label)
        line_edit = QLineEdit()
        layout.addWidget(line_edit)
        return line_edit
    
    def save_signal(self):
        if not hasattr(self, 'current_signal') or self.current_signal is None:
            # Show warning dialog instead of printing to console
            QMessageBox.warning(
                self,
                "Brak sygnału do zapisania",
                "Nie wygenerowano jeszcze żadnego sygnału do zapisania.",
                QMessageBox.Ok
            )
            return
        
        # Open file dialog to select save location
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Zapisz sygnał", 
            "", 
            "Signal Files (*.pkl);;All Files (*)", 
            options=options
        )
        
        if filename:
            # Add .pkl extension if not provided
            if not filename.endswith('.pkl'):
                filename += '.pkl'
            
            # Save the signal using FileRW
            if FileRW.write_signal_to_file(self.current_signal, filename):
                QMessageBox.information(
                    self,
                    "Sygnał zapisany",
                    f"Sygnał został zapisany w: {filename}",
                    QMessageBox.Ok
                )
            else:
                QMessageBox.critical(
                    self,
                    "Błąd zapisu sygnału",
                    "Wystąpił błąd podczas zapisu sygnału.",
                    QMessageBox.Ok
                )

    def plot_signal(self):
        self.plot(self.signal_col, self.canvas)

    def plot(self, col_layout, canvas):
        signal_selector = col_layout.itemAt(0).widget()
        selected_signal = signal_selector.currentText()
        signal_function = self.signal_functions.get(selected_signal)
        if signal_function:
            # Collect and convert parameters from input fields
            params = {}
            
            # Map UI parameter names to function parameter names
            param_mapping = {
                'amplitude': 'A',
                'duration': 'd',
                't1': 't_start',
                'period': 'T',
                'sampling': 'sampling_rate',
                'kw': 'kw',
                'sample_number': 'n_spike',
                'probability': 'p'
            }
            
            # Get values from enabled input fields
            for ui_param, func_param in param_mapping.items():
                input_field = self.parameter_inputs.get(ui_param)
                if input_field and input_field.isEnabled() and input_field.text():
                    try:
                        params[func_param] = float(input_field.text())
                    except ValueError:
                        # Use default if conversion fails
                        pass
            
            # Call the signal function with parameters
            sigObj = signal_function(**params)
            sig, time = sigObj.signal, sigObj.time
            self.current_signal = sigObj

            try:
                num_bins = int(self.parameter_inputs['bins'].text())
            except (ValueError, TypeError):
                num_bins = 20  # Default if invalid input
            
            if sigObj.discrete_signal:
                fig = plot_points(sig, time, bins_no=num_bins)
            else:
                fig = plot_signal(sig, time, bins_no=num_bins)
            canvas.figure.clear()
            canvas.figure = fig
            canvas.draw()

    def plot_signal1(self):
        # Generate signal from first column and plot on first canvas
        signal = self.generate_signal_from_column(self.signal1_col)
        if signal:
            self.plot_on_canvas(signal, self.canvas_signal1)
            self.current_signal = signal  # Store for potential saving

    def plot_signal2(self):
        # Generate signal from second column and plot on second canvas
        signal = self.generate_signal_from_column(self.signal2_col)
        if signal:
            self.plot_on_canvas(signal, self.canvas_signal2)
            self.current_signal = signal  # Store for potential saving

    def create_file_tab(self):
        file_tab = QWidget()
        layout = QVBoxLayout()
        file_tab.setLayout(layout)
        
        # File selection area
        file_section = QHBoxLayout()
        
        # Add file loading button
        load_button = QPushButton("Wczytaj sygnał z pliku")
        load_button.setFixedWidth(170)
        load_button.clicked.connect(self.load_signal_from_file)
        file_section.addWidget(load_button)
        
        # Add filename display
        self.file_path_label = QLabel("Nie wybrano pliku")
        file_section.addWidget(self.file_path_label)
        file_section.addStretch(1)
        
        layout.addLayout(file_section)
        
        # Create splitter for signal info and plot
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter, 1)  # Stretch to fill available space
        
        # Top section: Signal attributes and values
        info_widget = QWidget()
        info_layout = QHBoxLayout(info_widget)
        
        # Left side: Signal attributes
        attrs_group = QGroupBox("Atrybuty sygnału")
        attrs_layout = QVBoxLayout(attrs_group)
        self.attrs_table = QTableWidget(0, 2)
        self.attrs_table.setHorizontalHeaderLabels(["Nazwa", "Wartość"])
        self.attrs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.attrs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        attrs_layout.addWidget(self.attrs_table)
        info_layout.addWidget(attrs_group)
        
        # Right side: Signal values
        values_group = QGroupBox("Wartości sygnału")
        values_layout = QVBoxLayout(values_group)
        self.values_text = QTextEdit()
        self.values_text.setReadOnly(True)
        values_layout.addWidget(self.values_text)
        info_layout.addWidget(values_group)
        
        splitter.addWidget(info_widget)
        
        # Bottom section: Signal plot
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        
        # Plot controls
        plot_controls = QHBoxLayout()
        plot_layout.addLayout(plot_controls)
        
        # Add bins selection for histogram
        plot_controls.addWidget(QLabel("Liczba przedziałów histogramu:"))
        self.file_bins_input = QLineEdit()
        self.file_bins_input.setText("20")  # Default value
        self.file_bins_input.setFixedWidth(80)
        plot_controls.addWidget(self.file_bins_input)
        
        # Add plot button
        plot_button = QPushButton("Odśwież wykres")
        plot_button.clicked.connect(self.update_file_plot)
        plot_controls.addWidget(plot_button)
        
        plot_controls.addStretch(1)
        
        # Create canvas for plotting
        self.file_canvas = FigureCanvas(Figure(figsize=(10, 6)))
        plot_layout.addWidget(self.file_canvas)
        
        splitter.addWidget(plot_widget)
        
        # Set initial splitter sizes (40% for info, 60% for plot)
        splitter.setSizes([400, 600])
        
        self.tab_widget.addTab(file_tab, "Plik")

    def load_signal_from_file(self):
        # Open file dialog to select file
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Wczytaj sygnał", 
            "", 
            "Signal Files (*.pkl);;All Files (*)", 
            options=options
        )
        
        if filename:
            # Load signal from file
            signal_obj = FileRW.read_signal_from_file(filename)
            
            if signal_obj:
                # Store the loaded signal
                self.file_signal = signal_obj
                
                # Update file path label
                self.file_path_label.setText(filename)
                
                # Display signal attributes
                self.display_signal_attributes(signal_obj)
                
                # Display signal values
                self.display_signal_values(signal_obj)
                
                # Plot the signal
                self.update_file_plot()
            else:
                QMessageBox.critical(
                    self,
                    "Błąd odczytu",
                    f"Nie udało się wczytać sygnału z pliku: {filename}",
                    QMessageBox.Ok
                )

    def display_signal_attributes(self, signal_obj):
        # Clear the attributes table
        self.attrs_table.setRowCount(0)
        
        # Create a mapping from technical names to human-readable names
        attr_name_mapping = {
            # Signal parameters
            'A': 'Amplituda',
            'T': 'Okres [s]',
            'd': 'Czas trwania [s]',
            't_start': 'Przesunięcie czasowe [s]',
            'sampling_rate': 'Częstotliwość próbkowania [próbki/s]',
            'kw': 'Współczynnik wypełnienia',
            'n_start': 'Początkowy indeks',
            'n_spike': 'Numer próbki impulsu',
            'p': 'Prawdopodobieństwo',
            'discrete_signal': 'Sygnał dyskretny',
            
            # Calculated signal properties
            'mean_value': 'Wartość średnia',
            'abs_mean_value': 'Średnia wartość bezwzględna',
            'rms_value': 'Wartość skuteczna (RMS)',
            'variance': 'Wariancja',
            'avg_power': 'Średnia moc sygnału'
        }
        
        # Get all attributes that are not None and are not signal/time
        for attr_name in dir(signal_obj):
            # Skip private attributes, methods, and signal/time
            if (attr_name.startswith('_') or 
                callable(getattr(signal_obj, attr_name)) or 
                attr_name in ['signal', 'time']):
                continue
            
            attr_value = getattr(signal_obj, attr_name)
            
            # Skip None values
            if attr_value is None or attr_value == True or attr_value == False:
                continue
            
            # Add row to table
            row = self.attrs_table.rowCount()
            self.attrs_table.insertRow(row)
            
            # Get human-readable name or use original if not in mapping
            display_name = attr_name_mapping.get(attr_name, attr_name)
            
            # Set attribute name
            name_item = QTableWidgetItem(display_name)
            self.attrs_table.setItem(row, 0, name_item)
            
            # Format the value based on type
            if isinstance(attr_value, bool):
                value_str = "Tak" if attr_value else "Nie"
            elif isinstance(attr_value, (int, float)):
                value_str = f"{attr_value:.6g}"  # Format numbers nicely
            else:
                value_str = str(attr_value)
            
            # Set attribute value
            value_item = QTableWidgetItem(value_str)
            self.attrs_table.setItem(row, 1, value_item)
        
        # Sort the table by attribute name for better readability
        self.attrs_table.sortItems(0)

    def display_signal_values(self, signal_obj):
        # Clear the text display
        self.values_text.clear()
        
        # Format signal and time values as text
        text = "Indeks\tCzas\t\tWartość\n"
        text += "="*40 + "\n"
        
        for i, (t, v) in enumerate(zip(signal_obj.time, signal_obj.signal)):
            text += f"{i}\t{t:.6f}\t{v:.6f}\n"
        
        # Display in text edit
        self.values_text.setText(text)

    def update_file_plot(self):
        if not hasattr(self, 'file_signal'):
            return
            
        try:
            num_bins = int(self.file_bins_input.text())
        except (ValueError, TypeError):
            num_bins = 20
        
        signal_obj = self.file_signal
        sig, time = signal_obj.signal, signal_obj.time
        
        if signal_obj.discrete_signal:
            fig = plot_points(sig, time, bins_no=num_bins)
        else:
            fig = plot_signal(sig, time, bins_no=num_bins)
        
        self.file_canvas.figure = fig
        self.file_canvas.draw()

    def load_signal_for_tab(self):
        """Load a signal from file for the signal tab"""
        # Open file dialog to select file
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Wczytaj sygnał", 
            "", 
            "Signal Files (*.pkl);;All Files (*)", 
            options=options
        )
        
        if filename:
            # Load signal from file
            signal_obj = FileRW.read_signal_from_file(filename)
            
            if signal_obj:
                # Store the loaded signal
                self.current_signal = signal_obj
                
                # Show notification
                QMessageBox.information(
                    self,
                    "Sygnał wczytany",
                    f"Wczytano sygnał z pliku: {filename}",
                    QMessageBox.Ok
                )
                
                # Plot the signal
                self.plot_on_canvas(signal_obj, self.canvas)
            else:
                QMessageBox.critical(
                    self,
                    "Błąd odczytu",
                    f"Nie udało się wczytać sygnału z pliku: {filename}",
                    QMessageBox.Ok
                )

    def load_signal1(self):
        """Load signal 1 from file for the operations tab"""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Wczytaj sygnał 1", 
            "", 
            "Signal Files (*.pkl);;All Files (*)", 
            options=options
        )
        
        if filename:
            signal_obj = FileRW.read_signal_from_file(filename)
            
            if signal_obj:
                self.signal1 = signal_obj  # Store for operations
                self.plot_on_canvas(signal_obj, self.canvas_signal1)
                QMessageBox.information(
                    self,
                    "Sygnał wczytany",
                    f"Wczytano sygnał 1 z pliku: {filename}",
                    QMessageBox.Ok
                )
            else:
                QMessageBox.critical(
                    self,
                    "Błąd odczytu",
                    f"Nie udało się wczytać sygnału z pliku: {filename}",
                    QMessageBox.Ok
                )

    def load_signal2(self):
        """Load signal 2 from file for the operations tab"""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Wczytaj sygnał 2", 
            "", 
            "Signal Files (*.pkl);;All Files (*)", 
            options=options
        )
        
        if filename:
            signal_obj = FileRW.read_signal_from_file(filename)
            
            if signal_obj:
                self.signal2 = signal_obj  # Store for operations
                self.plot_on_canvas(signal_obj, self.canvas_signal2)
                QMessageBox.information(
                    self,
                    "Sygnał wczytany",
                    f"Wczytano sygnał 2 z pliku: {filename}",
                    QMessageBox.Ok
                )
            else:
                QMessageBox.critical(
                    self,
                    "Błąd odczytu",
                    f"Nie udało się wczytać sygnału z pliku: {filename}",
                    QMessageBox.Ok
                )