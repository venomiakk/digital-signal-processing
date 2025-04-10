from signals import SignalObject, SignalGenerator
from plots import plot_signal, plot_points
import numpy as np


class SignalConverter:
    @staticmethod
    def convert(self):
        # Placeholder for conversion logic
        return self.signal

    @staticmethod    
    def sample_signal(signal, time, fs):
        Ts = 1 / fs
        sampled_time = np.arange(time[0], time[-1], Ts)
        #TODO: sample manually
        sampled_values = np.interp(sampled_time, time, signal)
        return sampled_time, sampled_values

    @staticmethod
    def quantization_with_rounding(signal, n_bits):
        max_val = np.max(np.abs(signal))
        step = 2 * max_val / (2 ** n_bits - 1)
        quantized_signal = np.round(signal / step) * step
        return quantized_signal
    @staticmethod
    def quantize_with_truncation_signal(signal, n_bits):
        max_val = np.max(np.abs(signal))
        step = 2 * max_val / (2 ** n_bits - 1)
        quantized_signal = np.floor(signal / step) * step
        return quantized_signal

    @staticmethod
    def zero_order_extrapolation(t_samples, x_samples):
        t_query = np.linspace(t_samples[0], t_samples[-1], num=len(t_samples)*1000)
        x_query = np.zeros_like(t_query)
        n = len(t_samples)

        for i, t in enumerate(t_query):
            # Znajdź ostatnią próbkę, która jest nie później niż t
            idx = np.searchsorted(t_samples, t, side='right') - 1

            # Jeśli przed pierwszą próbką, trzymaj wartość z pierwszej próbki
            if idx < 0:
                idx = 0
            # Jeśli po ostatniej próbce, trzymaj ostatnią wartość
            elif idx >= n:
                idx = n - 1

            x_query[i] = x_samples[idx]

        return x_query


if __name__ == "__main__":
    print("Signal converter:")
    signal = SignalGenerator.sin_signal(A=1, T=2, t_start=0, d=3, sampling_rate=1000)
    plot_signal(signal, toplot=True)

    sampled_time, sampled_values = SignalConverter.sample_signal(signal.signal, signal.time, fs=10)
    sampled_signal = SignalObject(sampled_values, sampled_time, signal.sampling_rate, A=signal.A, T=signal.T, t_start=signal.t_start, d=signal.d)
    plot_points(sampled_signal, toplot=True)