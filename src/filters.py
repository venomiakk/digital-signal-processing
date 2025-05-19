import numpy as np

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
    # Example usage
    h = np.array([1, 2, 3])
    x = np.array([4, 5, 6])
    result = CustomSignalFilters.convolve(h, x)
    print("Convolution Result:", result)