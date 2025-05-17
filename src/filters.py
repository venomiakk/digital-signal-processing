import numpy as np

class CustomSignalFilters:
    @staticmethod
    def convolve(h, x):
        n_len = len(x)
        m_len = len(h)
        y = np.zeros(n_len + m_len - 1)

        for n in range(n_len + m_len - 1):
            for k in range(m_len):
                if n - k >= 0 and n - k < n_len:
                    y[n] += h[k] * x[n - k]

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
    def hamming_window(M):
        return 0.53836 - 0.46164 * np.cos(2 * np.pi * np.arange(M) / (M - 1))

    @staticmethod
    def apply_window(h, window_func):
        w = window_func(len(h))
        return h * w

    @staticmethod
    def highpass_from_lowpass(h):
        return h * (-1) ** np.arange(len(h))

    @staticmethod
    def bandpass_from_lowpass(h):
        n = np.arange(len(h))
        s = 2 * np.sin(np.pi * (n - (len(h) - 1) // 2) / 2)  # uwzględnij przesunięcie środka
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
        h = CustomSignalFilters.apply_window(h, CustomSignalFilters.hamming_window)

        # Convolve with the signal
        return CustomSignalFilters.convolve(h, signal)

    @staticmethod
    def correlation_direct(x, h):
        N = len(x)
        M = len(h)
        result = np.zeros(N + M - 1)
        for n in range(len(result)):
            for k in range(M):
                if 0 <= n - k < N:
                    result[n] += h[k] * x[n - k]
        return result

    @staticmethod
    def correlation_via_convolution(x, h):
        x_flipped = x[::-1]  # Odbicie sygnału x
        return CustomSignalFilters.convolve(x_flipped, h)

if __name__ == "__main__":
    # Example usage
    h = np.array([1, 2, 3])
    x = np.array([4, 5, 6])
    result = CustomSignalFilters.convolve(h, x)
    print("Convolution Result:", result)