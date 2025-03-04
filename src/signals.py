import numpy as np
import matplotlib.pyplot as plt

def sin_signal():
    A = 1       # Amplituda
    T = 1       # Okres (np. 1 sekunda, co oznacza częstotliwość 1 Hz)
    t1 = 0.2    # Przesunięcie czasowe (opóźnienie)
    d = 2       # Czas trwania sygnału w sekundach
    sampling_rate = 1000  # Próbkowanie

    time = np.linspace(0, d, int(d * sampling_rate), endpoint=False)
    signal = A * np.sin(2 * np.pi * T * (time - t1))
    print(time)

    plt.plot(time, signal)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Sinusoidal signal")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    sin_signal()