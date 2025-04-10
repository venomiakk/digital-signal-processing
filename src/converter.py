from matplotlib import pyplot as plt

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
    def quantization_with_rounding(time, signal, fs, n_bits):

        sampled_time, sampled_values = SignalConverter.sample_signal(signal, time, fs)
        # Quantization
        max_val = np.max(np.abs(sampled_values))
        step = 2 * max_val / (2 ** n_bits - 1)
        quantized_signal = np.round(sampled_values / step) * step

        return sampled_time, quantized_signal
    @staticmethod
    def quantize_with_truncation_signal(time, signal, fs, n_bits):
        sampled_time, sampled_values = SignalConverter.sample_signal(signal, time, fs)
        # Quantization
        max_val = np.max(np.abs(sampled_values))
        step = 2 * max_val / (2 ** n_bits - 1)
        quantized_signal = np.floor(sampled_values / step) * step

        return sampled_time, quantized_signal

    @staticmethod
    def zero_order_extrapolation(t_samples, x_samples):
        t_query = np.linspace(t_samples[0], t_samples[-1], num=len(t_samples))
        x_query = np.zeros_like(t_query)
        index1 = 0
        idx = x_samples[0]
        for index, i in enumerate(t_query):
            for j in t_samples:
                if i == j:
                    idx = x_samples[index1]
                    index1 += 1
            x_query[index] = idx
        return t_query, x_query

    @staticmethod
    def first_order_hold(t_samples, x_samples):

        # Generate interpolated time points
        t_query = np.linspace(t_samples[0], t_samples[-1], num=1000)

        # Perform linear interpolation
        x_recreated = np.interp(t_query, t_samples, x_samples)

        return t_query, x_recreated

    @staticmethod
    def sinc_interpolation(t_samples, x_samples):

        t_query = np.linspace(t_samples[0], t_samples[-1], num=1000)

        x_recreated = np.zeros_like(t_query)
        # Perform sinc interpolation
        for i, t in enumerate(t_query):
            sinc_terms = np.sinc((t - t_samples) / (t_samples[1] - t_samples[0]))
            x_recreated[i] = np.sum(x_samples * sinc_terms)

        return t_query, x_recreated


if __name__ == "__main__":
    print("Signal converter:")
    signal = SignalGenerator.sin_signal(A=1, T=2, t_start=0, d=3, sampling_rate=1000)
    plot_signal(signal, toplot=True)

    sampled_time, sampled_values = SignalConverter.sample_signal(signal.signal, signal.time, fs=10)
    sampled_signal = SignalObject(sampled_values, sampled_time, signal.sampling_rate, A=signal.A, T=signal.T, t_start=signal.t_start, d=signal.d)
    plot_points(sampled_signal, toplot=True)