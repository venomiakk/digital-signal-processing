import matplotlib.pyplot as plt


def plot_signal(signal, time):

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(time, signal)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Signal")
    plt.grid()

    #? is this correct?
    plt.subplot(1, 2, 2)
    plt.hist(signal, bins=20)
    plt.title("Histogram")
    plt.xlabel("Amplitude")
    plt.ylabel("Frequency")
    
    plt.tight_layout()
    plt.show()
