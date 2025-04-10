import matplotlib.pyplot as plt
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

def plot_converter(original_signal, sampled_time, sampled_values, toplot=False):
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
    ax.plot(time, signal, label="Original Signal", color="blue", linewidth=1.5)

    # Plot the sampled/quantized signal
    ax.scatter(sampled_time, sampled_values, label="Sampled/Quantized Signal", color="red", zorder=5)

    # Add vertical dashed lines
    for t, v in zip(sampled_time, sampled_values):
        ax.vlines(t, ymin=0, ymax=v, linestyles="dashed", colors="gray", alpha=0.7)

    # Add labels, legend, and grid
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    ax.set_title("Signal Conversion")
    ax.legend()
    ax.grid()

    if toplot:
        plt.show()
    plt.close()
    return fig

def plot_extrapolated_signal(original_signal, sampled_time, sampled_values, extrapolated_time, extrapolated_values, toplot=False):
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
    signal = original_signal.signal
    time = original_signal.time

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the original signal
    ax.plot(time, signal, label="Original Signal", color="blue", linewidth=1.5)

    # Plot the sampled/quantized signal
    ax.scatter(sampled_time, sampled_values, label="Sampled/Quantized Signal", color="red", zorder=5)

    # Plot the extrapolated signal as a staircase
    ax.step(extrapolated_time, extrapolated_values, where='post', label="Extrapolated Signal", color="green", linewidth=1.5)

    # Add vertical dashed lines
    for t, v in zip(sampled_time, sampled_values):
        ax.vlines(t, ymin=0, ymax=v, linestyles="dashed", colors="gray", alpha=0.7)

    # Add labels, legend, and grid
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    ax.set_title("Extrapolated Signal")
    ax.legend()
    ax.grid()

    if toplot:
        plt.show()
    plt.close()
    return fig