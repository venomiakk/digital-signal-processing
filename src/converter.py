from matplotlib import pyplot as plt

from signals import SignalObject, SignalGenerator
from plots import plot_signal, plot_points, plot_sampling, plot_reconstructed_signal, plot_quantization
import numpy as np


class SignalConverter:
    @staticmethod    
    def sample_signal(signal, time, fs):
        ori_sampling_rate = int(len(signal) / (time[-1] - time[0]))
        interval = int(ori_sampling_rate / fs)
        t_idxs = np.arange(0, len(signal), interval)
        sampled_time = []
        for i in range(0, len(signal), interval):
            sampled_time.append(time[i])


        sampled_values = signal[t_idxs]
        sampled_values = np.array(sampled_values)
        sampled_time = np.array(sampled_time)
        # print(len(sampled_time), len(sampled_values))
        return sampled_time, sampled_values

    @staticmethod
    def quantization_with_rounding(time, signal, n_bits):
        # 2. Kwantyzacja
        max_val = np.max(signal)
        min_val = np.min(signal)
        level = 2**n_bits - 1
        step = (max_val - min_val) / level
        # Zaokrąglanie i denormalizacja
        signal = signal - min_val  # Normalizacja
        quantized = step * np.round((signal/step))
        quantized = quantized + min_val
        
        return time, quantized

    @staticmethod
    def quantization_with_truncation(time, signal, n_bits):
        max_val = np.max(signal)
        min_val = np.min(signal)
        level = 2**n_bits - 1
        step = (max_val - min_val) / level
        # Zaokrąglanie i denormalizacja
        signal = signal - min_val  # Normalizacja
        quantized = step * np.floor((signal/step))
        quantized = quantized + min_val
        
        return time, quantized

    @staticmethod
    def zero_order_hold(ori_time, sampled_time, sampled_values):
        """
        Zwraca sygnał z próbkami i wartościami.
        """
        # Generowanie próbkowanego sygnału
        sampled_signal = np.zeros_like(ori_time)
        for i in range(len(sampled_time) - 1):
            mask = (ori_time >= sampled_time[i]) & (ori_time < sampled_time[i + 1])
            sampled_signal[mask] = sampled_values[i]
        
        return sampled_signal
    
    @staticmethod
    def first_order_hold(ori_time, sampled_time, sampled_values):
        """
        Zwraca sygnał z próbkami i wartościami.
        """
        return np.interp(ori_time, sampled_time, sampled_values)
    
    @staticmethod
    def sinc_interpolation(ori_time, sampled_time, sampled_values):
        """
        Zwraca sygnał z próbkami i wartościami.
        """
        # Generowanie próbkowanego sygnału
        sampled_signal = np.zeros_like(ori_time)
        for i in range(len(sampled_time)):
            sinc_terms = np.sinc((ori_time - sampled_time[i]) / (sampled_time[1] - sampled_time[0]))
            sampled_signal += sampled_values[i] * sinc_terms
        
        return sampled_signal

    
    @staticmethod
    def mse(x, xz):
        """(C1) Błąd średniokwadratowy"""
        return np.mean((x - xz) ** 2)

    @staticmethod
    def snr(x, xz):
        """(C2) Stosunek sygnał - szum w dB"""
        power_signal = np.sum(x ** 2)
        power_noise = np.sum((x - xz) ** 2)
        return 10 * np.log10(power_signal / power_noise)

    @staticmethod
    def psnr(x, xz):
        """(C3) Szczytowy stosunek sygnał - szum w dB"""
        mse_val = SignalConverter.mse(x, xz)
        max_signal = np.max(x)
        return 10 * np.log10((max_signal) / mse_val)

    @staticmethod
    def md(x, xz):
        """(C4) Maksymalna różnica"""
        return np.max(np.abs(x - xz))
    
    @staticmethod
    def enob(x, xz):
        """Efektywna liczba bitów"""
        snr = SignalConverter.snr(x, xz)
        return (snr - 1.76) / 6.02

if __name__ == "__main__":

    
    signal = SignalGenerator.sin_signal(A=1, T=1, t_start=0, d=2, sampling_rate=1000)
    quantized_time, quantized_values = SignalConverter.quantization_with_rounding(signal.time, signal.signal, n_bits=4)
    plot_quantization("Kwantyzacja z zaokragleniem", signal, quantized_time, quantized_values, toplot=True)
    quantized_time, quantized_values = SignalConverter.quantization_with_truncation(signal.time, signal.signal, n_bits=4)
    plot_quantization("Kwantyzacja z obcinaniem", signal, quantized_time, quantized_values, toplot=True)

    sampled_time, sampled_values = SignalConverter.sample_signal(signal.signal, signal.time, fs=10)
    plot_sampling("Próbkowanie", signal, sampled_time, sampled_values, toplot=True)

    reconstructed_signal = SignalConverter.zero_order_hold(signal.time, sampled_time, sampled_values)
    plot_reconstructed_signal("Rekonstrukcja zerowym trzymaniem", signal.signal, signal.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)
    
    reconstructed_signal = SignalConverter.first_order_hold(signal.time, sampled_time, sampled_values)
    plot_reconstructed_signal("Rekonstrukcja pierwszym trzymaniem", signal.signal, signal.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)
    
    reconstructed_signal = SignalConverter.sinc_interpolation(signal.time, sampled_time, sampled_values)
    plot_reconstructed_signal("Rekonstrukcja sinc", signal.signal, signal.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)



