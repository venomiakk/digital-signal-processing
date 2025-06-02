from signals import SignalGenerator, SignalOperations
from filesRW import FileRW
import numpy as np
from plots import plot_raw_signal, plot_raw_points
from matplotlib import pyplot as plt

class Transfomations:
    @staticmethod
    def generate_signals():
        f_pr = 16  # Hz
        T = 1 / f_pr
        N = 64  # liczba próbek 
        t = np.arange(N) * T

        S1 = 2 * np.sin(2 * np.pi * (1/2) * t + np.pi/2) + 5 * np.sin(2 * np.pi * (1/0.5) * t + np.pi/2)
        # plot_raw_signal(S1, t, toplot=True)
        # plot_raw_points(S1, t, toplot=True)
        
        S2 = 2 * np.sin(2 * np.pi * (1/2) * t) + np.sin(2 * np.pi * (1/1) * t) + 5 * np.sin(2 * np.pi * (1/0.5) * t)
        # plot_raw_signal(S2, t, toplot=True)
        # plot_raw_points(S2, t, toplot=True)
        
        S3 = 5 * np.sin(2 * np.pi * (1/2) * t) + np.sin(2 * np.pi * (1/0.25) * t)
        # plot_raw_signal(S3, t, toplot=True)
        # plot_raw_points(S3, t, toplot=True)

        return S1, S2, S3

    @staticmethod
    def dft(x):
        N = len(x)
        X = np.zeros(N, dtype=complex)
        for k in range(N):
            for n in range(N):
                X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
        return X


if __name__ == "__main__":
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T

    X_dft = Transfomations.dft(s2)
    print("DFT:", X_dft)
    # Porównanie z numpy FFT
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(np.abs(X_dft), linewidth=3)
    plt.plot(X_dft)
    plt.title("P")
    plt.xlabel("Indeks")
    plt.ylabel("Amplituda")
    plt.show()
    
    freqs = np.fft.fftfreq(N, T)[:N//2]
    print("Częstotliwości:", freqs)
    plt.figure(figsize=(12, 6))
    plt.stem(freqs, 2 * np.abs(X_dft[:N//2]) / N, linefmt='b-', markerfmt='bo', basefmt=' ')
    plt.title("Widmo amplitudowe sygnału")
    plt.xlabel("Częstotliwość [Hz]")
    plt.ylabel("Amplituda")
    plt.grid()
    plt.show()