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