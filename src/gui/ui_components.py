from PyQt5.QtWidgets import (QLabel, QComboBox, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLineEdit, QFormLayout, QSizePolicy)

def create_signal_column(title, plot_method, save_method, signal_types):
    """
    Creates a signal parameter column with all inputs and controls
    
    Args:
        title: The title of the column
        plot_method: The method to call when the plot button is clicked
        save_method: The method to call when the save button is clicked
        signal_types: List of signal types for the dropdown
        
    Returns:
        tuple: (layout, parameter_inputs_dict)
    """
    col_layout = QVBoxLayout()
    col_layout.setContentsMargins(10, 10, 10, 10)
    col_layout.setSpacing(10)
    
    # Title label with styling
    label = QLabel(title)
    label.setStyleSheet("font-weight: bold; font-size: 14px;")
    col_layout.addWidget(label)
    
    # Signal type selector
    signal_selector = QComboBox()
    signal_selector.addItems(signal_types)
    signal_selector.setMaxVisibleItems(len(signal_types))
    col_layout.addWidget(signal_selector)
    
    # Create form layout for parameters
    form_layout = QFormLayout()
    form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
    form_layout.setContentsMargins(0, 0, 0, 0)
    form_layout.setSpacing(6)  # Spacing between form rows
    
    # Create all parameter inputs
    parameter_inputs = {}
    
    amplitude_input = QLineEdit()
    amplitude_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    form_layout.addRow("Amplituda:", amplitude_input)
    parameter_inputs['amplitude'] = amplitude_input
    
    duration_input = QLineEdit()
    duration_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    form_layout.addRow("Czas trwania [s]:", duration_input)
    parameter_inputs['duration'] = duration_input
    
    t_start_input = QLineEdit()
    t_start_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    form_layout.addRow("Przesunięcie [s]:", t_start_input)
    parameter_inputs['t1'] = t_start_input
    
    sampling_input = QLineEdit()
    sampling_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    form_layout.addRow("Próbkowanie [próbki/s]:", sampling_input)
    parameter_inputs['sampling'] = sampling_input
    
    period_input = QLineEdit()
    period_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    form_layout.addRow("Okres [s]:", period_input)
    parameter_inputs['period'] = period_input

    kw_input = QLineEdit()
    kw_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    form_layout.addRow("Współczynnik wypełnienia:", kw_input)
    parameter_inputs['kw'] = kw_input

    sample_number_input = QLineEdit()
    sample_number_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    form_layout.addRow("Numer próbki:", sample_number_input)
    parameter_inputs['sample_number'] = sample_number_input

    probability_input = QLineEdit()
    probability_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    form_layout.addRow("Prawdopodobieństwo:", probability_input)
    parameter_inputs['probability'] = probability_input

    col_layout.addLayout(form_layout)

    # Create a horizontal layout for the plot button and bins input
    button_row = QHBoxLayout()
    
    # Add plot button to the horizontal layout
    plot_button = QPushButton("Wygeneruj sygnał")
    plot_button.setFixedWidth(120)
    if plot_method:
        plot_button.clicked.connect(plot_method)
    button_row.addWidget(plot_button)

    # Add save button
    save_button = QPushButton("Zapisz sygnał")
    save_button.setFixedWidth(120)
    if save_method:
        save_button.clicked.connect(save_method)
    button_row.addWidget(save_button)
        
    # Add spacing between elements
    button_row.addSpacing(10)
    
    # Add bin number label and input to the horizontal layout
    button_row.addStretch(1)
    button_row.addWidget(QLabel("Liczba przedziałów histogramu:"))
    
    bin_input = QLineEdit()
    bin_input.setText("20")  # Default value
    bin_input.setFixedWidth(80)  # Make it reasonably sized
    button_row.addWidget(bin_input)
    parameter_inputs['bins'] = bin_input
    
    # Add the horizontal layout to the main column layout
    col_layout.addLayout(button_row)
    
    # Set up signal changes to update UI
    signal_selector.currentTextChanged.connect(
        lambda text: update_input_fields(text, parameter_inputs)
    )
    
    # Initialize input fields
    update_input_fields(signal_selector.currentText(), parameter_inputs)
    
    # Store signal_selector as an attribute of the layout for easy access
    col_layout.signal_selector = signal_selector
    
    return col_layout, parameter_inputs

def update_input_fields(signal_type, parameter_inputs):
    """Enable/disable input fields based on signal type"""
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
    for param_name, input_field in parameter_inputs.items():
        if param_name == 'bins':
            continue

        if param_name in needed_params:
            input_field.setEnabled(True)
        else:
            input_field.setEnabled(False)
            input_field.clear()  # Clear the disabled fields