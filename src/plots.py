import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def plot_signal(signalobj, bins_no=20, toplot=False):
    signal = signalobj.signal
    time = signalobj.time
    # fig, (plot1, plot2, plot_text) = plt.subplots(1, 3, figsize=(14, 4), gridspec_kw={'width_ratios': [4, 4, 1]})
    fig, (plot1, plot2, plot_text) = plt.subplots(3, 1, figsize=(6, 8), gridspec_kw={'height_ratios': [4, 4, 1]})

    stats_text = "Statystyki:\n"
    stats_text += f"Średnia: {signalobj.mean_value:.4f}\n"
    stats_text += f"Średnia |x|: {signalobj.abs_mean_value:.4f}\n"
    stats_text += f"RMS: {signalobj.rms_value:.4f}\n"
    stats_text += f"Wariancja: {signalobj.variance:.4f}\n"
    stats_text += f"Moc: {signalobj.avg_power:.4f}"

    plot_text.text(0.5, 0.6, stats_text, fontsize=10, verticalalignment='center', horizontalalignment='center')
    plot_text.axis("off") 


    plot1.grid()
    plot1.axhline(y=0, color='k', linewidth=1.5, alpha=0.3)
    plot1.plot(time, signal)
    plot1.set_xlabel("Czas [s]")
    plot1.set_ylabel("Amplituda")
    plot1.set_title("Sygnał")
    
    plot2.hist(signal, bins=bins_no)
    plot2.set_title("Histogram")
    plot2.set_xlabel("Amplituda")
    plot2.set_ylabel("Częstość")


    fig.tight_layout()
    if toplot:
        plt.show()
    plt.close()
    return fig


def plot_points(signalobj, bins_no=20, toplot=False):
    signal = signalobj.signal
    time = signalobj.time
    fig, (plot1, plot2, plot_text) = plt.subplots(3, 1, figsize=(6, 8), gridspec_kw={'height_ratios': [4, 4, 1]})

    stats_text = "Statystyki:\n"
    stats_text += f"Średnia: {signalobj.mean_value:.4f}\n"
    stats_text += f"Średnia |x|: {signalobj.abs_mean_value:.4f}\n"
    stats_text += f"RMS: {signalobj.rms_value:.4f}\n"
    stats_text += f"Wariancja: {signalobj.variance:.4f}\n"
    stats_text += f"Moc: {signalobj.avg_power:.4f}"

    plot_text.text(0.5, 0.6, stats_text, fontsize=10, verticalalignment='center', horizontalalignment='center')
    plot_text.axis("off") 

    plot1.grid()
    plot1.axhline(y=0, color='k', linewidth=1.5, alpha=0.3)
    plot1.scatter(time, signal)
    plot1.set_xlabel("Czas [s]")
    plot1.set_ylabel("Amplituda")
    plot1.set_title("Sygnał")
    
    plot2.hist(signal, bins=bins_no)
    plot2.set_title("Histogram")
    plot2.set_xlabel("Amplituda")
    plot2.set_ylabel("Częstość")

    fig.tight_layout()
    if toplot:
        plt.show()
    plt.close()
    return fig

def plot_sampling(title, original_signal, sampled_time, sampled_values, toplot=False):
    """
    Plots the original signal, sampled/quantized signal, and vertical dashed lines.

    Parameters:
        original_signal (SignalObject): The original signal object.
        sampled_time (numpy.ndarray): The time points of the sampled/quantized signal.
        sampled_values (numpy.ndarray): The values of the sampled/quantized signal.
        toplot (bool): Whether to display the plot.
    """
    signal = original_signal.signal
    time = original_signal.time

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the original signal
    ax.plot(time, signal, label="Sygnał oryginalny", linewidth=1)

    # Plot the sampled/quantized signal
    ax.scatter(sampled_time, sampled_values, label="Próbki", color="red", zorder=5)

    # Add vertical dashed lines
    for t, v in zip(sampled_time, sampled_values):
        ax.vlines(t, ymin=0, ymax=v, linestyles="dashed", colors="gray", alpha=0.7)

    # Add labels, legend, and grid
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda")
    ax.set_title(title)
    ax.legend()
    ax.grid()

    if toplot:
        plt.show()
    plt.close()
    return fig

def plot_quantization(title, original_signal, quantized_time, quantized_values, toplot=False):
    """
    Plots the original signal, quantized signal, and vertical dashed lines.

    Parameters:
        original_signal (SignalObject): The original signal object.
        quantized_time (numpy.ndarray): The time points of the quantized signal.
        quantized_values (numpy.ndarray): The values of the quantized signal.
        toplot (bool): Whether to display the plot.
    """
    signal = original_signal.signal
    time = original_signal.time

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the original signal
    ax.plot(time, signal, label="Sygnał oryginalny")

    # Plot the quantized signal
    ax.plot(quantized_time, quantized_values, label="Kwantyzacja")


    # Add labels, legend, and grid
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda")
    ax.set_title(title)
    ax.legend()
    ax.grid()

    if toplot:
        plt.show()
    plt.close()
    return fig

def plot_reconstructed_signal(title, original_signal, original_time, sampled_values, sampled_time, reconstructed_values, toplot=False):
    """
    Plots the extrapolated signal with vertical dashed lines to the points.

    Parameters:
        original_signal (SignalObject): The original signal object.
        sampled_time (numpy.ndarray): The time points of the sampled/quantized signal.
        sampled_values (numpy.ndarray): The values of the sampled/quantized signal.
        extrapolated_time (numpy.ndarray): The time points of the extrapolated signal.
        extrapolated_values (numpy.ndarray): The values of the extrapolated signal.
        toplot (bool): Whether to display the plot.
    """

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the original signal
    ax.plot(original_time, original_signal, label="Sygnał oryginalny", linewidth=1.5)

    # Plot the sampled/quantized signal
    ax.scatter(sampled_time, sampled_values, label="Próbki", color="red", zorder=5)

    # Plot the extrapolated signal as a staircase
    ax.plot(original_time, reconstructed_values,  label="Sygnał zrekonstuowany")

    # Add vertical dashed lines
    for t, v in zip(sampled_time, sampled_values):
        ax.vlines(t, ymin=0, ymax=v, linestyles="dashed", colors="gray", alpha=0.7)

    # Add labels, legend, and grid
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda")
    ax.set_title(title)
    ax.legend()
    ax.grid()

    if toplot:
        plt.show()
    plt.close()
    return fig

def plot_filters(original_signal, dirty_signal, filtered_signal):
    """
    Plots the original, noisy, and filtered signals after adjusting their time arrays
    to match the lengths of their respective signal arrays.

    Parameters:
        original_signal (SignalObject): The original signal object with `signal` and `time` attributes.
        dirty_signal (SignalObject): The noisy signal object with `signal` and `time` attributes.
        filtered_signal (SignalObject): The filtered signal object with `signal` and `time` attributes.
    """
    def adjust_time(signal_obj):
        # Generate a new time array with the same length as the signal
        return np.linspace(signal_obj.time[0], signal_obj.time[-1], len(signal_obj.signal))

    # Adjust time arrays
    original_time = adjust_time(original_signal)
    dirty_time = adjust_time(dirty_signal)
    filtered_time = adjust_time(filtered_signal)

    # Plot the signals
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(dirty_time, dirty_signal.signal, label="Noisy Signal", linewidth=1.5)
    ax.plot(original_time, original_signal.signal, label="Original Signal", linewidth=1.5)
    ax.plot(filtered_time, filtered_signal.signal, label="Filtered Signal", linewidth=1.5, color='pink')

    # Add labels, legend, and grid
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    ax.set_title("Signal Comparison")
    ax.legend()
    ax.grid()

    plt.show()
    return fig

def plot_raw_signal(signal, time=None, toplot=False, title=""):
    fig, ax = plt.subplots(figsize=(10, 6))
    if time is None:
        ax.plot(signal, label="Sygnał", marker='o', markersize=3, linestyle='--', linewidth=1)
        ax.set_xlabel("k")
    else:
        ax.plot(time, signal, label="Sygnał", marker='o', markersize=3, linestyle='--', linewidth=1)
        ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda")
    ax.set_title("Sygnał " + title)
    # ax.legend()
    ax.grid()

    if toplot:
        plt.show()
    plt.close()
    return fig

def plot_raw_points(signal, time, toplot=False):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(time, signal, label="Sygnał")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda")
    ax.set_title("Sygnał")
    # ax.legend()
    ax.grid()

    if toplot:
        plt.show()
    plt.close()
    return fig


def plot_W1(X, title="", stem=True, tofile=False):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle(title, fontsize=16)
    
    # Część rzeczywista
    if stem:
        ax1.stem(X.real, basefmt=' ', linefmt='C0-')
    else:
        ax1.plot(X.real, 'C0-', marker='o', markersize=3, linewidth=1)
    ax1.set_title("Część rzeczywista")
    ax1.set_xlabel("k")
    ax1.set_ylabel("Re{X[k]}")
    ax1.grid()

    # Część urojona
    if stem:
        ax2.stem(X.imag, basefmt=' ', linefmt='C1-')
    else:
        ax2.plot(X.imag, 'C1-', marker='o', markersize=3, linewidth=1)
    ax2.set_title("Część urojona")
    ax2.set_xlabel("k")
    ax2.set_ylabel("Im{X[k]}")
    ax2.grid()

    plt.tight_layout()
    
    if tofile==False:
        plt.show()
    plt.close()
    return fig


def plot_W2(X, title="", stem=True, tofile=False):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle(title, fontsize=16)
    
    # Moduł
    if stem:
        ax1.stem(np.abs(X), basefmt=' ', linefmt='C0-')
    else:
        ax1.plot(np.abs(X), 'C0-', marker='o', markersize=3, linestyle='--', linewidth=1)
    ax1.set_title("Moduł")
    ax1.set_xlabel("k")
    ax1.set_ylabel("|X[k]|")
    ax1.grid()

    # Argument (faza)
    if stem:
        ax2.stem(np.angle(X), basefmt=' ', linefmt='C1-')
    else:
        ax2.plot(np.angle(X), 'C1-', marker='o', markersize=3, linestyle='--', linewidth=1)
    ax2.set_title("Argument (faza)")
    ax2.set_xlabel("k")
    ax2.set_ylabel("arg(X[k]) [rad]")
    ax2.grid()

    plt.tight_layout()
    
    if tofile:
        plt.show()
    plt.close()
    return fig
