import numpy as np
from signals import SignalGenerator, SignalOperations

class CustomSignalFilters:
    @staticmethod
    def convolve(x, h):
        N = len(x)
        M = len(h)
        y = np.zeros(N + M - 1)
        for n in range(N + M - 1):
            for k in range(M):
                i = n - k
                if 0 <= i < N:
                    y[n] += x[i] * h[k]
        return y

    @staticmethod
    def ideal_lowpass_response(M, K):
        h = np.zeros(M)
        mid = (M - 1) // 2
        for n in range(M):
            if n == mid:
                h[n] = 2 / K
            else:
                h[n] = np.sin(2 * np.pi * (n - mid) / K) / (np.pi * (n - mid))
        return h

    @staticmethod
    def apply_hamming_window(signal_func):
        signal = signal_func
        N = len(signal)
        window = 0.53836 - 0.46164 * np.cos(2 * np.pi * np.arange(N) / (N - 1))
        return signal * window

    @staticmethod
    def apply_hanning_window(signal_func):
        signal = signal_func
        N = len(signal)
        window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N) / (N - 1))
        return signal * window

    @staticmethod
    def apply_blackman_window(signal_func):
        signal = signal_func
        N = len(signal)
        window = (0.42
                  - 0.5 * np.cos(2 * np.pi * np.arange(N) / (N - 1))
                  + 0.08 * np.cos(4 * np.pi * np.arange(N) / (N - 1)))
        return signal * window



    @staticmethod
    def highpass_from_lowpass(h):
        n = np.arange(len(h))
        s = (-1) ** n
        return h * s

    @staticmethod
    def bandpass_from_lowpass(h):
        n = np.arange(len(h))
        s = 2 * np.sin(np.pi * n / 2)
        return h * s
    @staticmethod
    def aplly_filter(signal, cutoff_freq, filter_order=5, filter_type='low'):
        """
        Apply a low-pass filter to the signal.

        Parameters:
            signal: numpy.ndarray - input signal
            cutoff_freq: float - cutoff frequency
            filter_order: int - order of the filter
            filter_type: str - type of filter ('low', 'high', 'band')
        """
        if filter_type == 'low':
            h = CustomSignalFilters.ideal_lowpass_response(filter_order, cutoff_freq)
        elif filter_type == 'high':
            h = CustomSignalFilters.highpass_from_lowpass(CustomSignalFilters.ideal_lowpass_response(filter_order, cutoff_freq))
        elif filter_type == 'band':
            h = CustomSignalFilters.bandpass_from_lowpass(CustomSignalFilters.ideal_lowpass_response(filter_order, cutoff_freq))
        else:
            raise ValueError("Invalid filter type. Choose 'low', 'high', or 'band'.")

        # Apply window
        h = CustomSignalFilters.apply_hamming_window(h)

        # Convolve with the signal
        return CustomSignalFilters.convolve(signal, h)

    @staticmethod
    def correlation_direct(x, h):
        N = len(x)
        M = len(h)
        h = h[::-1]  # odwrócenie h
        result = np.zeros(N + M - 1)
        for n in range(len(result)):
            for k in range(M):
                i = n - k
                if 0 <= i < N:
                    result[n] += x[i] * h[k]
        return result

    @staticmethod
    def correlation_via_convolution(x, h):
        h_flipped = h[::-1]
        return CustomSignalFilters.convolve(h_flipped, x)

if __name__ == "__main__":
    signal1 = SignalGenerator.sin_signal(A=1, T=0.1, d=0.5, sampling_rate=1000)
    signal2 = SignalGenerator.sin_signal(A=1, T=0.02, d=0.5, sampling_rate=1000)
    signal3 = SignalOperations.add_signals(signal1, signal2)
    
    # Importowanie matplotlib
    import matplotlib.pyplot as plt
    
    # Utworzenie wykresu
    plt.figure(figsize=(12, 8))
    
    # Wykres pierwszego sygnału - 10 Hz
    plt.subplot(3, 1, 1)
    plt.plot(signal1.time, signal1.signal)
    plt.title('Sygnał sinusoidalny 10 Hz')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    # Wykres drugiego sygnału - 50 Hz
    plt.subplot(3, 1, 2)
    plt.plot(signal2.time, signal2.signal)
    plt.title('Sygnał sinusoidalny 50 Hz')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    # Wykres złożenia sygnałów
    plt.subplot(3, 1, 3)
    plt.plot(signal3.time, signal3.signal)
    plt.title('Sygnał złożony (10 Hz + 50 Hz)')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Demonstracja filtrowania
    # Definiowanie parametrów filtra dolnoprzepustowego
    filter_order = 21  # Długość odpowiedzi impulsowej filtra (nieparzysta)
    cutoff_freq = 15   # Częstotliwość odcięcia w Hz
    
    # Tworzenie odpowiedzi impulsowej filtra
    lowpass_impulse = CustomSignalFilters.ideal_lowpass_response(filter_order, cutoff_freq)
    windowed_lowpass = CustomSignalFilters.apply_hamming_window(lowpass_impulse)
    
    # Filtrowanie sygnału złożonego
    filtered_signal = CustomSignalFilters.convolve(signal3.signal, windowed_lowpass)
    
    # Tworzenie odpowiedniej osi czasu dla przefiltrowanego sygnału
    time_filtered = np.linspace(
        signal3.time[0], 
        signal3.time[0] + len(filtered_signal)/signal3.sampling_rate, 
        len(filtered_signal)
    )
    
    # Wyświetlanie wyników filtrowania
    plt.figure(figsize=(12, 8))
    
    # Oryginał
    plt.subplot(2, 1, 1)
    plt.plot(signal3.time, signal3.signal)
    plt.title('Oryginalny sygnał złożony')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    # Po filtracji dolnoprzepustowej
    plt.subplot(2, 1, 2)
    plt.plot(time_filtered, filtered_signal)
    plt.title(f'Sygnał po filtracji dolnoprzepustowej (odcięcie: {cutoff_freq} Hz)')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Demonstracja różnych typów filtrów
    plt.figure(figsize=(12, 10))
    
    # Parametry filtrów
    filter_order = 51  # Długość odpowiedzi impulsowej filtra (nieparzysta)
    cutoff_freq_low = 20   # Częstotliwość odcięcia w Hz dla filtra dolnoprzepustowego
    cutoff_freq_high = 30  # Częstotliwość odcięcia w Hz dla filtra górnoprzepustowego
    
    # Filtracja z użyciem różnych typów filtrów
    signal_lowpass = CustomSignalFilters.aplly_filter(signal3.signal, cutoff_freq_low, filter_order, 'low')
    signal_highpass = CustomSignalFilters.aplly_filter(signal3.signal, cutoff_freq_high, filter_order, 'high')
    signal_bandpass = CustomSignalFilters.aplly_filter(signal3.signal, 25, filter_order, 'band')
    
    # Tworzenie odpowiednich osi czasu dla przefiltrowanych sygnałów
    time_filtered = np.linspace(
        signal3.time[0], 
        signal3.time[0] + len(signal_lowpass)/signal3.sampling_rate, 
        len(signal_lowpass)
    )
    
    # Oryginał
    plt.subplot(4, 1, 1)
    plt.plot(signal3.time, signal3.signal)
    plt.title('Oryginalny sygnał złożony (10 Hz + 50 Hz)')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    # Po filtracji dolnoprzepustowej
    plt.subplot(4, 1, 2)
    plt.plot(time_filtered, signal_lowpass)
    plt.title(f'Filtr dolnoprzepustowy (odcięcie: {cutoff_freq_low} Hz)')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    # Po filtracji górnoprzepustowej
    plt.subplot(4, 1, 3)
    plt.plot(time_filtered, signal_highpass)
    plt.title(f'Filtr górnoprzepustowy (odcięcie: {cutoff_freq_high} Hz)')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    # Po filtracji pasmowoprzepustowej
    plt.subplot(4, 1, 4)
    plt.plot(time_filtered, signal_bandpass)
    plt.title('Filtr pasmowoprzepustowy (środek pasma: 25 Hz)')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Dodatkowo: porównanie okien filtrów
    plt.figure(figsize=(12, 10))
    
    # Generowanie odpowiedzi impulsowej filtra dolnoprzepustowego
    impulse_response = CustomSignalFilters.ideal_lowpass_response(filter_order, cutoff_freq_low)
    
    # Zastosowanie różnych okien
    hamming_windowed = CustomSignalFilters.apply_hamming_window(impulse_response)
    hanning_windowed = CustomSignalFilters.apply_hanning_window(impulse_response)
    blackman_windowed = CustomSignalFilters.apply_blackman_window(impulse_response)
    
    # Oryginalna odpowiedź impulsowa (bez okna)
    plt.subplot(4, 1, 1)
    plt.stem(impulse_response, basefmt=' ')
    plt.title('Idealna odpowiedź impulsowa filtra dolnoprzepustowego')
    plt.xlabel('Próbka')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    # Z oknem Hamminga
    plt.subplot(4, 1, 2)
    plt.stem(hamming_windowed, basefmt=' ')
    plt.title('Z oknem Hamminga')
    plt.xlabel('Próbka')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    # Z oknem Hanninga
    plt.subplot(4, 1, 3)
    plt.stem(hanning_windowed, basefmt=' ')
    plt.title('Z oknem Hanninga')
    plt.xlabel('Próbka')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    # Z oknem Blackmana
    plt.subplot(4, 1, 4)
    plt.stem(blackman_windowed, basefmt=' ')
    plt.title('Z oknem Blackmana')
    plt.xlabel('Próbka')
    plt.ylabel('Amplituda')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

