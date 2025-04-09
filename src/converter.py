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

    
if __name__ == "__main__":
    print("Signal converter:")
    signal = SignalGenerator.sin_signal(A=1, T=2, t_start=0, d=3, sampling_rate=1000)
    plot_signal(signal, toplot=True)

    sampled_time, sampled_values = SignalConverter.sample_signal(signal.signal, signal.time, fs=10)
    sampled_signal = SignalObject(sampled_values, sampled_time, signal.sampling_rate, A=signal.A, T=signal.T, t_start=signal.t_start, d=signal.d)
    plot_points(sampled_signal, toplot=True)