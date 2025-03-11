import numpy as np
from plots import plot_signal, plot_points


def uniformly_distributed_noise(A=1, t_start=0, d=2, sampling_rate=1000):
    # S1
    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = np.random.uniform(-A, A, len(time))
    
    plot_signal(signal, time)

    return signal, time

def gaussian_noise(A=1, t_start=0, d=2, sampling_rate=1000):
    # TODO: czy trzeba skorzystac ze wzoru na rozkald normalny czy mozna tak jak nizej?
    # S2
    # parameters
      # duration
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
    cycles = int(T * sampling_rate)
    high_cycles = int(cycles * kw)

    for k in range(int(len(time) / cycles) + 1):
        start_idx = int(k * cycles)
        end_idx = min(start_idx + high_cycles, len(time))
        signal[start_idx:end_idx] = A
        
        start_low_idx = end_idx
        end_low_idx = min(start_low_idx + (cycles - high_cycles), len(time))
        signal[start_low_idx:end_low_idx] = 0
    
    plot_signal(signal, time)

    return signal, time

def square_symmetric_signal(A=1, T=1, kw=0.5, t_start=0, d=2, sampling_rate=1000):
    # S7
    # TODO: Check if this is correct
    t_end = t_start + d

    time = np.linspace(0, t_end, int(d * sampling_rate))

    signal = np.zeros_like(time)
    cycles = int(T * sampling_rate)
    high_cycles = int(cycles * kw)

    for k in range(int(len(time) / cycles) + 1):
        start_idx = int(k * cycles)
        end_idx = min(start_idx + high_cycles, len(time))
        signal[start_idx:end_idx] = A
        
        start_low_idx = end_idx
        end_low_idx = min(start_low_idx + (cycles - high_cycles), len(time))
        signal[start_low_idx:end_low_idx] = -A
    
    plot_signal(signal, time)

    return signal, time

def triangle_signal():
    # S8
    pass

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
    square_signal()
    square_symmetric_signal()
    # triangle_signal()
    # step_signal()
    # unit_impulse()
    # impulse_noise()