from PyQt5.QtWidgets import QMessageBox, QFileDialog
from plots import plot_signal, plot_points
from filesRW import FileRW

def generate_signal(selected_signal, signal_functions, parameter_inputs):
    """Generate a signal based on UI parameters"""
    signal_function = signal_functions.get(selected_signal)
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
        input_field = parameter_inputs.get(ui_param)
        if input_field and input_field.isEnabled() and input_field.text():
            try:
                params[func_param] = float(input_field.text())
            except ValueError:
                pass
    
    # Call the signal function with parameters
    return signal_function(**params)
    
def plot_on_canvas(signal_obj, canvas, num_bins=20):
    """Plot a signal on a canvas with histograms"""
    if not signal_obj:
        return
        
    sig, time = signal_obj.signal, signal_obj.time
    
    if signal_obj.discrete_signal:
        fig = plot_points(sig, time, bins_no=num_bins)
    else:
        fig = plot_signal(sig, time, bins_no=num_bins)
    
    canvas.figure.clear()
    canvas.figure = fig
    canvas.draw()

def save_signal_to_file(parent_widget, signal_obj):
    """Save a signal object to a file with UI feedback"""
    if not signal_obj:
        QMessageBox.warning(
            parent_widget,
            "Brak sygnału do zapisania",
            "Nie wygenerowano jeszcze sygnału do zapisania.",
            QMessageBox.Ok
        )
        return
    
    # Open file dialog to select save location
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getSaveFileName(
        parent_widget, 
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
        if FileRW.write_signal_to_file(signal_obj, filename):
            QMessageBox.information(
                parent_widget,
                "Sygnał zapisany",
                f"Sygnał został zapisany w: {filename}",
                QMessageBox.Ok
            )
        else:
            QMessageBox.critical(
                parent_widget,
                "Błąd zapisu sygnału",
                "Wystąpił błąd podczas zapisu sygnału.",
                QMessageBox.Ok
            )