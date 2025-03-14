import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot_signal(signal, time, bins_no=20):
    fig, (plot1, plot2) = plt.subplots(1, 2, figsize=(10, 3))

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
    plt.show()
    return fig


def plot_points(signal, time, bins_no=20):
    fig, (plot1, plot2) = plt.subplots(1, 2, figsize=(10, 3))

    plot1.grid()
    plot1.axhline(y=0, color='k', linewidth=1.5, alpha=0.3)
    plot1.scatter(time, signal)
    plot1.set_xlabel("Time [s]")
    plot1.set_ylabel("Amplitude")
    plot1.set_title("Signal")

    plot2.hist(signal, bins=bins_no)
    plot2.set_title("Histogram")
    plot2.set_xlabel("Amplitude")
    plot2.set_ylabel("Frequency")

    fig.tight_layout()
    plt.show()
    return fig