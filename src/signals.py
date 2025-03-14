import numpy as np
from plots import plot_signal, plot_points

class SignalObject:
    def __init__(self, signal, time, sampling_rate=None, A=None, T=None, t_start=None, d=None, kw=None, n_start=None, n_spike=None, p=None):
        self.signal = signal
        self.time = time
        self.sampling_rate = sampling_rate
        self.A = A
        self.T = T
        self.t_start = t_start
        self.d = d
        self.kw = kw
        self.n_start = n_start
        self.n_spike = n_spike
        self.p = p


def uniformly_distributed_noise(A=1, t_start=0, d=2, sampling_rate=1000):
    # S1
    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = np.random.uniform(-A, A, len(time))
    
    plot_signal(signal, time)

    return signal, time

def gaussian_noise(A=1, t_start=0, d=2, sampling_rate=1000):
    # S2
    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = A * np.random.normal(0, 1, len(time))
    
    plot_signal(signal, time)

    return signal, time

def sin_signal(A=1, T=1, t_start=0, d=2, sampling_rate=1000):
    # TODO: Check if this is correct
    # S3
    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = A * np.sin(2 * np.pi * (time - t_start) / T)

    plot_signal(signal, time)

    return signal, time

def sin_half_signal(A=1, T=1, t_start=0, d=2, sampling_rate=1000):
    # S4

    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = 0.5 * A * ((np.sin(2 * np.pi * (time - t_start) / T)) + np.abs(np.sin(2 * np.pi * (time - t_start) / T)))

    plot_signal(signal, time)

    return signal, time

def sin_twohalf_signal(A=1, T=1, t_start=0, d=2, sampling_rate=1000):
    # S5
    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = A * np.abs(np.sin(2 * np.pi * (time - t_start) / T))

    plot_signal(signal, time)

    return signal, time

def square_signal(A=1, T=1, kw=0.5, t_start=0, d=2, sampling_rate=1000):
    # TODO: Check if this is correct
    # S6

    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = np.zeros_like(time)

    for i, t in enumerate(time):
        k = np.floor(t / T)  # Numer okresu
        t_mod = t - k * T  # Czas w bieżącym okresie
        
        if t_start <= t_mod < kw * T + t_start:
            signal[i] = A
        elif kw * T + t_start <= t_mod < T + t_start:
            signal[i] = 0
    
    plot_signal(signal, time)

    return signal, time

def square_symmetric_signal(A=1, T=1, kw=0.5, t_start=0, d=2, sampling_rate=1000):
    # S7
    # TODO: Check if this is correct
    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = np.zeros_like(time)

    for i, t in enumerate(time):
        k = np.floor(t / T)  # Numer okresu
        t_mod = t - k * T  # Czas w bieżącym okresie
        
        if t_start <= t_mod < kw * T + t_start:
            signal[i] = A
        elif kw * T + t_start <= t_mod < T + t_start:
            signal[i] = -A
    
    plot_signal(signal, time)

    return signal, time

def triangle_signal(A=1, T=1, t_start=0, d=2, kw=0.5, sampling_rate=1000):
    # S8
    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = np.zeros_like(time)

    for i, t in enumerate(time):
        k = np.floor(t / T)  # Numer okresu
        t_mod = t - k * T  # Czas w bieżącym okresie
        
        if t_start <= t_mod < kw * T + t_start:
            signal[i] = (A / (kw * T)) * (t_mod - t_start)
        elif kw * T + t_start <= t_mod < T + t_start:
            signal[i] = (-A / (T * (1 - kw))) * (t_mod - t_start) + A / (1 - kw)

    plot_signal(signal, time)

    return signal, time

def step_signal(A=1, t_start=0, d=2, sampling_rate=1000):
    # S9
    # Czas trwania sygnału w sekundach
    t_end = t_start + d
    t_step = t_end / 2

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = np.piecewise(time, [time < t_step, time >= t_step], [0, A])
    
    
    plot_signal(signal, time)

    return signal, time

def unit_impulse(A=1, n_start=0, n_spike = 10, sampling_rate=10, d=2):
    # S10
    time = np.linspace(0, d, int(d * sampling_rate))
    signal = np.zeros_like(time)
    if n_spike < len(signal):
        signal[n_spike] = A
    else:
        signal[-1] = A

    plot_points(signal, time)
    
    return signal, time

def impulse_noise(A=1, t_start=0, d=2, sampling_rate=30, p=0.5):
    # S11
    # TODO: Check if this is correct
    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = np.random.choice([0, A], len(time), p=[1-p, p])
    
    plot_points(signal, time)
    
    return signal, time

if __name__ == "__main__":
    # uniformly_distributed_noise()
    # gaussian_noise()
    # sin_signal()
    # sin_half_signal()
    # sin_twohalf_signal()
    # square_signal()
    square_symmetric_signal()
    # triangle_signal()
    # step_signal()
    # unit_impulse()
    # impulse_noise()