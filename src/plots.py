import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot_signal(signal, time):
    fig, (plot1, plot2) = plt.subplots(1, 2, figsize=(12, 3))

    plot1.plot(time, signal)
    plot1.set_xlabel("Time [s]")
    plot1.set_ylabel("Amplitude")
    plot1.set_title("Signal")
    plot1.grid()

    plot2.hist(signal, bins=20)
    plot2.set_title("Histogram")
    plot2.set_xlabel("Amplitude")
    plot2.set_ylabel("Frequency")

    fig.tight_layout()
    return fig
